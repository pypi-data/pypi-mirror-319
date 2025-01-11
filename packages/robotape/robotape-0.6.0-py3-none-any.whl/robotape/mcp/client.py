"""MCP client implementation."""
from typing import List, Any, Dict
from mcp.client.stdio import StdioServerParameters
import mcp.types as types
from .tools import MCPTool
from .mcp import create_mcp_client

class MCPClient:
    """Client for interacting with MCP server."""
    
    def __init__(self, server_params: StdioServerParameters):
        """Initialize MCP client.
        
        Args:
            server_params: Parameters for connecting to MCP server
        """
        self.server_params = server_params
        self.client = None

    async def connect(self):
        """Connect to the MCP server."""
        self.client = await create_mcp_client(self.server_params)

    async def list_tools(self) -> List[MCPTool]:
        """List all available tools exposed by the MCP server."""
        if not self.client:
            raise RuntimeError("Not connected to MCP server")
            
        tools = await self.client.list_tools()
        return [MCPTool(self, tool) for tool in tools]

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool by name with the given parameters."""
        if not self.client:
            raise RuntimeError("Not connected to MCP server")
            
        return await self.client.call_tool(tool_name, kwargs)

    async def list_resources(self) -> List[types.Resource]:
        """List all available resources exposed by the MCP server."""
        if not self.client:
            raise RuntimeError("Not connected to MCP server")
            
        result = await self.client.list_resources()
        return result.resources if hasattr(result, 'resources') else []

    async def read_resource(self, uri: str) -> Any:
        """Read the content of a resource by its URI."""
        if not self.client:
            raise RuntimeError("Not connected to MCP server")
            
        result = await self.client.read_resource(uri)
        return result.content if hasattr(result, 'content') else None

    async def list_prompts(self) -> List[types.Prompt]:
        """List all available prompts exposed by the MCP server."""
        if not self.client:
            raise RuntimeError("Not connected to MCP server")
            
        result = await self.client.list_prompts()
        return result.prompts if hasattr(result, 'prompts') else []

    async def generate_prompt(self, name: str, **kwargs) -> str:
        """Generate a prompt by name with the given parameters."""
        if not self.client:
            raise RuntimeError("Not connected to MCP server")
            
        result = await self.client.get_prompt(name, kwargs)
        return result.content if hasattr(result, 'content') else None

    async def close(self):
        """Close the MCP client connection."""
        if self.client:
            await self.client.close()