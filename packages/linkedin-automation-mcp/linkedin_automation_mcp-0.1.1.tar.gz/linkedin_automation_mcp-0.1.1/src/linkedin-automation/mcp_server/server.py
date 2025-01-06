#!/usr/bin/env python3
import asyncio
import json
import sys
import logging
from typing import Dict, Any, Callable

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class McpServer:
    """Base class for MCP (Message Communication Protocol) server implementation."""
    
    def __init__(self, server_name: str, protocol_version: str) -> None:
        self.server_name = server_name
        self.protocol_version = protocol_version
        self._handlers: Dict[str, Callable] = {
            "initialize": self._handle_initialize,
            "resources/list": self._handle_list_resources,
            "resources/templates/list": self._handle_list_resource_templates,
            "notifications/initialized": self._handle_notification,
            "cancelled": self._handle_cancelled,
        }

    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request."""
        client_protocol_version = params.get('protocolVersion', self.protocol_version)
        return {
            'protocolVersion': client_protocol_version,
            'serverInfo': {
                'name': self.server_name,
                'version': self.protocol_version
            },
            'capabilities': {
                'tools': {
                    'available': True
                },
                'resources': {
                    'available': False
                },
                'resourceTemplates': {
                    'available': False
                }
            }
        }

    def _handle_list_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resources listing request."""
        return {'resources': []}

    def _handle_list_resource_templates(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resource templates listing request."""
        return {'resourceTemplates': []}

    def _handle_notification(self, params: Dict[str, Any]) -> None:
        """Handle notifications."""
        logger.info(f"Received notification with params: {params}")
        return None

    def _handle_cancelled(self, params: Dict[str, Any]) -> None:
        """Handle cancellation notifications."""
        logger.info(f"Received cancellation with params: {params}")
        return None

    def register_handler(self, method: str, handler: Callable) -> None:
        """Register a new handler for a method."""
        self._handlers[method] = handler

    async def _handle_message(self, message: str) -> None:
        """Handle a single JSON-RPC message."""
        try:
            logger.info(f"Received message: {message}")
            request = json.loads(message)
            method = request.get("method")
            params = request.get("params", {})

            logger.info(f"Processing method: {method}")

            if method not in self._handlers:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Unknown method: {method}",
                    },
                }
            else:
                handler = self._handlers[method]
                # Check if handler is async or sync
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(params)
                else:
                    result = handler(params)

                if result is None:
                    return

                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }

            logger.info(f"Sending response: {response}")
            print(json.dumps(response), flush=True)

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}", exc_info=True)
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if "request" in locals() else None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response), flush=True)

    async def run(self) -> None:
        """Run the MCP server."""
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)

        logger.info(f"Starting {self.server_name}")
        
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    logger.info("Received EOF, shutting down server")
                    break
                
                await self._handle_message(line.strip())
        except Exception as e:
            logger.error(f"Server error: {str(e)}", exc_info=True)
            raise 