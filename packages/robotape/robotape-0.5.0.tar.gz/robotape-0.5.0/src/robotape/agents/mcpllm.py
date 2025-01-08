# src/robotape/agents/mcpllm.py
from typing import Optional, Dict, Any
from ..llm import LLMConfig, create_llm, BaseLLM
from ..models.steps import StepResult
from ..tape import Step, Tape
from ..utils.logging import get_logger
from ..mcp import MCPClient
from ..utils.mcp import StdioServerParameters

logger = get_logger(__name__)

class MCPLLMAgent:
    """Agent that combines LLM and MCP capabilities."""
    
    def __init__(
        self, 
        name: str, 
        llm_config: LLMConfig,
        mcp_config: Dict[str, Any]
    ):
        # Initialize the name attribute directly
        self.name = name
        
        # Initialize LLM
        self.llm = create_llm(llm_config)
        
        # Initialize MCP config
        self.mcp_config = mcp_config
        self.mcp_client: Optional[MCPClient] = None
        self.available_tools: Dict[str, Any] = {}

    async def connect(self):
        """Connect to MCP server and initialize resources."""
        try:
            # Set up MCP client
            server_params = StdioServerParameters(
                command=self.mcp_config["command"],
                args=self.mcp_config["args"],
                env=self.mcp_config.get("env")
            )
            self.mcp_client = MCPClient(server_params)
            await self.mcp_client.connect()
            
            # Get available tools
            tools = await self.mcp_client.list_tools()
            self.available_tools = {
                tool.tool_name: tool for tool in tools
            }
            
            logger.info(f"Connected to MCP server with {len(self.available_tools)} tools")
            
        except Exception as e:
            logger.error(f"Error connecting to MCP server: {str(e)}")
            raise

    async def think(self, context: Dict[str, Any]) -> StepResult:
        """Generate thoughts using LLM and available MCP tools."""
        try:
            # Prepare tool descriptions for LLM
            tool_descriptions = "\n".join([
                f"- {name}: {str(tool)}"
                for name, tool in self.available_tools.items()
            ])
            
            # Create prompt for LLM
            prompt = f"""Given the context: {context}
            Available tools:
            {tool_descriptions}
            
            What tool should be used next and why? Respond in JSON format with:
            - tool_name: selected tool name
            - parameters: tool parameters
            - reasoning: explanation for this choice"""
            
            # Get LLM response
            llm_response = await self.llm.generate(prompt)
            
            return StepResult(
                success=True,
                output=llm_response.text,
                metadata={
                    "model": llm_response.model,
                    "available_tools": list(self.available_tools.keys())
                }
            )
            
        except Exception as e:
            return StepResult(success=False, error=str(e))

    async def act(self, thought: Step) -> StepResult:
        """Execute action using selected MCP tool based on LLM thought."""
        try:
            # Parse LLM thought to get tool selection
            thought_content = thought.content
            tool_name = thought_content.get("tool_name")
            parameters = thought_content.get("parameters", {})
            
            if not tool_name or tool_name not in self.available_tools:
                return StepResult(
                    success=False,
                    error=f"Invalid tool selection: {tool_name}"
                )
            
            # Execute the selected tool
            tool = self.available_tools[tool_name]
            result = await tool.execute(parameters)
            
            return StepResult(
                success=True,
                output=result,
                metadata={
                    "tool": tool_name,
                    "parameters": parameters
                }
            )
            
        except Exception as e:
            return StepResult(success=False, error=str(e))

    async def observe(self, action: Step) -> StepResult:
        """Analyze action results using LLM and MCP resources."""
        try:
            # In our simplified implementation, we'll just have the LLM analyze the action result
            prompt = f"""Analyze the following action result:
            Action: {action.content}
            
            Provide an analysis of the results and any important observations."""
            
            # Get LLM analysis
            llm_response = await self.llm.generate(prompt)
            
            return StepResult(
                success=True,
                output=llm_response.text,
                metadata={
                    "model": llm_response.model,
                    "action_analyzed": action.metadata.id
                }
            )
            
        except Exception as e:
            return StepResult(success=False, error=str(e))

    async def cleanup(self):
        """Clean up both LLM and MCP resources."""
        try:
            if self.llm:
                await self.llm.close()
            if self.mcp_client:
                await self.mcp_client.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")