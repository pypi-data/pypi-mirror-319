import argparse
import asyncio
import json
import logging
import shlex
import sys

import jsonschema
import websockets

from asyncio import create_subprocess_exec, subprocess
from typing import Optional, Dict, Any

from websockets.legacy.server import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INITIALIZE_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["jsonrpc", "method", "params", "id"],
    "properties": {
        "jsonrpc": {"type": "string", "enum": ["2.0"]},
        "method": {"type": "string", "enum": ["initialize"]},
        "params": {
            "type": "object",
            "required": ["protocolVersion", "clientInfo", "capabilities"],
            "properties": {
                "protocolVersion": {"type": "string"},
                "clientInfo": {
                    "type": "object",
                    "required": ["name", "version"],
                    "properties": {
                        "name": {"type": "string"},
                        "version": {"type": "string"}
                    }
                },
                "capabilities": {"type": "object"}
            }
        },
        "id": {"type": ["string", "number"]}
    }
}

class McpWebSocketBridge:
    def __init__(self, command: str, port: int = 3000):
        self.command = command
        self.port = port
        self.process: Optional[subprocess.Process] = None
        self.websocket: Optional[WebSocketServerProtocol] = None
        self.pending_requests: Dict[str, asyncio.Future] = {}


    async def start_mcp_process(self):
        """Start the stdio MCP server process"""
        args = shlex.split(self.command)

        self.process = await create_subprocess_exec(
            *args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if not self.process.stdin or not self.process.stdout:
            raise RuntimeError("Failed to create process pipes")

        logger.info(f"Started MCP process: {self.command}")
        return self.process

    async def handle_stderr(self):
        """Handle stderr output from the process"""
        while True:
            if not self.process or not self.process.stderr:
                break

            try:
                line = await self.process.stderr.readline()
                if not line:
                    break
                logger.info(f"Process stderr: {line.decode().strip()}")
            except Exception as e:
                logger.error(f"Error handling stderr: {e}")
                break

    async def handle_process_output(self):
        """Read and handle output from the MCP process"""
        while True:
            if not self.process or not self.process.stdout:
                break

            try:
                line = await self.process.stdout.readline()
                if not line:
                    logger.info("Process stdout closed")
                    break

                line_str = line.decode().strip()
                logger.debug(f"Process stdout: {line_str}")

                if not line_str:
                    continue

                try:
                    message = json.loads(line_str)

                    if "id" in message and message["id"] in self.pending_requests:
                        future = self.pending_requests.pop(message["id"])
                        future.set_result(message)

                    if self.websocket and self.websocket.state == websockets.protocol.State.OPEN:
                        await self.websocket.send(json.dumps(message))
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {line_str}")
                    logger.error(f"JSON error: {e}")

            except Exception as e:
                logger.error(f"Error handling process output: {e}")
                continue  # Continue instead of break to keep the loop running

        logger.info("Process output handling ended")


    async def handle_client(self, websocket: WebSocketServerProtocol):
        self.websocket = websocket
        logger.info("WebSocket client connected")

        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    logger.debug(f"Received message: {data}")

                    # Validate initialize request
                    if data.get("method") == "initialize":
                        try:
                            jsonschema.validate(instance=data, schema=INITIALIZE_REQUEST_SCHEMA)
                        except jsonschema.exceptions.ValidationError as e:
                            error_response = {
                                "jsonrpc": "2.0",
                                "id": data.get("id"),
                                "error": {
                                    "code": -32600,
                                    "message": f"Invalid initialize request: {str(e)}"
                                }
                            }
                            await websocket.send(json.dumps(error_response))
                            continue

                    # Rest of the message handling...
                    if "id" in data:
                        self.pending_requests[data["id"]] = asyncio.Future()

                    if self.process and self.process.stdin:
                        message_bytes = f"{json.dumps(data)}\n".encode()
                        self.process.stdin.write(message_bytes)
                        await self.process.stdin.drain()
                        logger.debug(f"Sent to process: {data}")

                        if "id" in data:
                            try:
                                response = await asyncio.wait_for(
                                    self.pending_requests[data["id"]],
                                    timeout=10.0
                                )
                                await websocket.send(json.dumps(response))
                            except asyncio.TimeoutError:
                                error_response = {
                                    "jsonrpc": "2.0",
                                    "id": data["id"],
                                    "error": {
                                        "code": -32000,
                                        "message": "Request timed out"
                                    }
                                }
                                await websocket.send(json.dumps(error_response))

                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    if "id" in data:
                        error_response = {
                            "jsonrpc": "2.0",
                            "id": data["id"],
                            "error": {
                                "code": -32000,
                                "message": str(e)
                            }
                        }
                        await websocket.send(json.dumps(error_response))

        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket client disconnected")
        finally:
            self.websocket = None

    async def cleanup(self):
        """Clean up resources"""
        if self.process:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()  # Force kill if it doesn't terminate
            self.process = None

        for future in self.pending_requests.values():
            if not future.done():
                future.cancel()
        self.pending_requests.clear()

    async def serve(self):
        """Start the WebSocket server and MCP process"""
        try:
            await self.start_mcp_process()

            # Start both stdout and stderr handlers
            stdout_task = asyncio.create_task(self.handle_process_output())
            stderr_task = asyncio.create_task(self.handle_stderr())

            # Start WebSocket server
            async with websockets.serve(self.handle_client, "localhost", self.port):
                logger.info(f"WS-MCP bridge running on ws://localhost:{self.port}")

                # Wait for either process to end or forever
                try:
                    await asyncio.gather(stdout_task, stderr_task)
                except Exception as e:
                    logger.error(f"Error in message handling: {e}")

                await asyncio.Future()  # run forever

        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            await self.cleanup()

def parse_args():
    parser = argparse.ArgumentParser(
        description='Bridge a stdio-based MCP server to WebSocket',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --command "uv tool run --from wcgw@latest --python 3.12 wcgw_mcp" --port 3000
  %(prog)s --command "node path/to/mcp-server.js" --port 3001
        """
    )

    parser.add_argument(
        '--command',
        type=str,
        required=True,
        help='Command to start the MCP server (in quotes)'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=3000,
        help='Port for the WebSocket server (default: 3000)'
    )

    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level (default: INFO)'
    )

    return parser.parse_args()

async def execute():
    args = parse_args()

    # Set log level from arguments
    logging.getLogger().setLevel(args.log_level)

    bridge = McpWebSocketBridge(args.command, args.port)
    await bridge.serve()

def main():
    asyncio.run(execute())

if __name__ == "__main__":
    main()
