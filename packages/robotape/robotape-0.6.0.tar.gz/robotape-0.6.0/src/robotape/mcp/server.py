"""MCP server implementation."""

from typing import Callable, Any
from mirascope.mcp import MCPServer as MirascopeMCPServer

class MCPServer:
    """Server for exposing tools, resources, and prompts via MCP."""
    
    def __init__(self, name: str):
        """Initialize MCP server.
        
        Args:
            name: Name of the server instance
        """
        self.name = name
        self.server = MirascopeMCPServer(name)

    def register_tool(self, tool: Callable):
        """Register a tool with the MCP server.
        
        Args:
            tool: Tool function to register
        """
        self.server.tool()(tool)

    def register_resource(self, uri: str, name: str, mime_type: str, handler: Callable):
        """Register a resource with the MCP server.
        
        Args:
            uri: Resource URI
            name: Resource name
            mime_type: MIME type of the resource
            handler: Resource handler function
        """
        self.server.resource(uri=uri, name=name, mime_type=mime_type)(handler)

    def register_prompt(self, prompt: Callable):
        """Register a prompt with the MCP server.
        
        Args:
            prompt: Prompt function to register
        """
        self.server.prompt()(prompt)

    async def run(self):
        """Start the MCP server."""
        await self.server.run()

    async def stop(self):
        """Stop the MCP server."""
        if self.server:
            await self.server.stop()
