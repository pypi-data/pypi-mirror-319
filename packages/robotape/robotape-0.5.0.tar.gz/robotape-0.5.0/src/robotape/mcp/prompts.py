"""MCP prompt implementation."""

class MCPPrompt:
    """Prompt template exposed by MCP server."""
    
    def __init__(self, mcp_client, prompt_name: str):
        """Initialize MCP prompt.
        
        Args:
            mcp_client: MCP client instance
            prompt_name: Name of the prompt template
        """
        self.mcp_client = mcp_client
        self.prompt_name = prompt_name

    async def generate(self, **kwargs) -> str:
        """Generate a prompt with the given parameters.
        
        Args:
            **kwargs: Parameters for the prompt template
            
        Returns:
            Generated prompt text
        """
        return await self.mcp_client.generate_prompt(self.prompt_name, **kwargs)

    def __str__(self) -> str:
        return f"MCPPrompt({self.prompt_name})"

    def __repr__(self) -> str:
        return self.__str__()
