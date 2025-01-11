"""MCP tool implementation."""

from typing import Dict, Any

class MCPTool:
    """Tool exposed by MCP server."""
    
    def __init__(self, mcp_client, tool_name: str):
        """Initialize MCP tool.
        
        Args:
            mcp_client: MCP client instance
            tool_name: Name of the tool
        """
        self.mcp_client = mcp_client
        self.tool_name = tool_name

    async def execute(self, args: Dict[str, Any]) -> Any:
        """Execute the MCP-enabled tool.
        
        Args:
            args: Tool arguments
            
        Returns:
            Tool execution result
        """
        return await self.mcp_client.execute_tool(self.tool_name, **args)

    def __str__(self) -> str:
        return f"MCPTool({self.tool_name})"

    def __repr__(self) -> str:
        return self.__str__()