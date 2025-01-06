#!/usr/bin/env python3
import os
import sys
import logging
from dotenv import load_dotenv
from mcp_server import McpServer
from tools import (
    LinkedInTools,
    PostScraperTool,
    ConnectionTool,
    ProfileInfoTool,
    PostContentToLinkedinTool,
    ToolsList
)
from prompts import list_prompts, get_prompt
from typing import Dict, Any, List

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Constants
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
PROTOCOL_VERSION = "0.1.0"
SERVER_NAME = "linkedin-automation"

try:
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        raise ValueError("Required environment variables LINKEDIN_EMAIL and LINKEDIN_PASSWORD are not set")
except Exception as e:
    logger.error(f"Environment configuration error: {str(e)}")
    sys.exit(1)

class LinkedInAutomationServer(McpServer):
    """LinkedIn automation server implementation."""
    
    def __init__(self) -> None:
        """Initialize the LinkedIn automation server."""
        super().__init__(SERVER_NAME, PROTOCOL_VERSION)
        
        # Initialize LinkedIn tools
        self.linkedin_tools = LinkedInTools(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
        
        # Register handlers
        self.register_handler("tools/list", self._handle_list_tools)
        self.register_handler("tools/call", self._handle_call_tool)
        self.register_handler("prompts/list", self._handle_list_prompts)
        self.register_handler("prompts/get", self._handle_get_prompt)

    async def _handle_list_tools(self, _) -> dict:
        """Handle listing available tools."""
        tools_list = ToolsList(
            tools=[
                PostScraperTool(),
                ConnectionTool(),
                ProfileInfoTool(),
                PostContentToLinkedinTool()
            ]
        )
        return tools_list.model_dump()

    async def _handle_call_tool(self, params: dict) -> dict:
        """Handle tool execution requests."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        tool_handlers = {
            "scrape_posts": self.linkedin_tools.scrape_posts,
            "send_connections": self.linkedin_tools.send_connections,
            "get_profile_info": self.linkedin_tools.get_profile_info,
            "post_content_to_linkedin": self.linkedin_tools.post_content
        }

        handler = tool_handlers.get(tool_name)
        if not handler:
            raise Exception(f"Unknown tool: {tool_name}")

        return await handler(arguments)

    async def _handle_list_prompts(self, _) -> Dict[str, List[Dict[str, Any]]]:
        """Handle listing available prompts."""
        return list_prompts()

    async def _handle_get_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle retrieving a specific prompt."""
        prompt_name = params.get("name")
        arguments = params.get("arguments", {})
        return get_prompt(prompt_name, arguments)

    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Override initialize to add prompts capability."""
        response = super()._handle_initialize(params)
        response["capabilities"]["prompts"] = {"available": True}
        return response

if __name__ == "__main__":
    server = LinkedInAutomationServer()
    try:
        import asyncio
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        sys.exit(1)
