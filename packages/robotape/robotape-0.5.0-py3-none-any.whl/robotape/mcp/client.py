"""MCP client implementation."""

from typing import List, Any, Dict
from mirascope.mcp.client import create_mcp_client, StdioServerParameters
from .resources import MCPResource
from .prompts import MCPPrompt
from .tools import MCPTool

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
        tools = await self.client.list_tools()
        return [MCPTool(self, tool.name) for tool in tools]

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool by name with the given parameters."""
        tools = await self.list_tools()
        tool = next((t for t in tools if t.name == tool_name), None)
        if tool:
            return await tool.execute(kwargs)
        raise ValueError(f"Tool {tool_name} not found")

    async def list_resources(self) -> List[MCPResource]:
        """List all available resources exposed by the MCP server."""
        resources = await self.client.list_resources()
        return [MCPResource(self, resource.uri) for resource in resources]

    async def read_resource(self, resource_uri: str) -> Any:
        """Read the content of a resource by its URI."""
        return await self.client.read_resource(resource_uri)

    async def list_prompts(self) -> List[MCPPrompt]:
        """List all available prompts exposed by the MCP server."""
        prompts = await self.client.list_prompts()
        return [MCPPrompt(self, prompt.name) for prompt in prompts]

    async def generate_prompt(self, prompt_name: str, **kwargs) -> str:
        """Generate a prompt by name with the given parameters."""
        prompt_template = await self.client.get_prompt_template(prompt_name)
        return await prompt_template(**kwargs)

    async def close(self):
        """Close the MCP client connection."""
        if self.client:
            await self.client.close()
