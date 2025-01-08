"""MCP resource implementation."""

from typing import Any

class MCPResource:
    """Resource exposed by MCP server."""
    
    def __init__(self, mcp_client, resource_uri: str):
        """Initialize MCP resource.
        
        Args:
            mcp_client: MCP client instance
            resource_uri: URI of the resource
        """
        self.mcp_client = mcp_client
        self.resource_uri = resource_uri

    async def read(self) -> Any:
        """Read the resource content.
        
        Returns:
            Content of the resource
        """
        return await self.mcp_client.read_resource(self.resource_uri)

    def __str__(self) -> str:
        return f"MCPResource({self.resource_uri})"

    def __repr__(self) -> str:
        return self.__str__()
