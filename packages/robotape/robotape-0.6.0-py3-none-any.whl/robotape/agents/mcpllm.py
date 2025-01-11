"""MCPLLMAgent implementation."""
from typing import Optional, Dict, Any, List
from contextlib import AsyncExitStack
import json
from ..llm import LLMConfig, create_llm, BaseLLM
from ..models.steps import StepResult
from ..tape import Step
from ..utils.logging import get_logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = get_logger(__name__)

class MCPLLMAgent:
    """Agent that combines LLM and MCP capabilities."""
    
    def __init__(
        self, 
        name: str, 
        llm_config: LLMConfig,
        mcp_config: Dict[str, Any]
    ):
        # Initialize the name and LLM
        self.name = name
        self.llm = create_llm(llm_config)
        
        # Initialize MCP config and client
        self.mcp_config = mcp_config
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.available_tools: Dict[str, Any] = {}
        
        logger.debug(f"Initialized MCPLLMAgent: {name}")

    async def connect(self):
        """Connect to MCP server and initialize resources."""
        try:
            # Set up MCP client
            server_params = StdioServerParameters(
                command=self.mcp_config["command"],
                args=self.mcp_config["args"],
                env=self.mcp_config.get("env")
            )
            
            # Create and connect client
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
            
            # Initialize the session
            await self.session.initialize()
            
            # Get available tools
            response = await self.session.list_tools()
            self.available_tools = {tool.name: tool for tool in response.tools}
            
            logger.info(f"Connected to MCP server with {len(self.available_tools)} tools")
            
        except Exception as e:
            logger.error(f"Error connecting to MCP server: {str(e)}")
            await self.cleanup()
            raise

    async def think(self, context: Dict[str, Any]) -> StepResult:
        """Generate thoughts using LLM and available MCP tools."""
        try:
            # Prepare tool descriptions for LLM
            tool_descriptions = "\n".join([
                f"- {name}: {tool.description}\n  Parameters: {tool.inputSchema}"
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
            logger.error(f"Error during thinking step: {str(e)}")
            return StepResult(success=False, error=str(e))

    async def act(self, thought: Step) -> StepResult:
        """Execute action using selected MCP tool based on LLM thought."""
        try:
            if not self.session:
                raise RuntimeError("Not connected to MCP server")
            
            # Parse LLM thought to get tool selection
            thought_content = thought.content
            if isinstance(thought_content, str):
                try:
                    thought_content = json.loads(thought_content)
                except json.JSONDecodeError:
                    return StepResult(
                        success=False,
                        error="Invalid JSON in thought content"
                    )

            tool_name = thought_content.get("tool_name")
            parameters = thought_content.get("parameters", {})
            
            if not tool_name or tool_name not in self.available_tools:
                return StepResult(
                    success=False,
                    error=f"Invalid tool selection: {tool_name}"
                )
            
            logger.debug(f"Executing tool {tool_name} with parameters: {parameters}")
            
            # Execute the selected tool
            raw_result = await self.session.call_tool(tool_name, parameters)
            
            # Convert result to dictionary with "result" key
            if hasattr(raw_result, 'content') and raw_result.content:
                # If we have content array with text
                if len(raw_result.content) > 0 and hasattr(raw_result.content[0], 'text'):
                    try:
                        parsed = json.loads(raw_result.content[0].text)
                        result = {"result": parsed}
                    except json.JSONDecodeError:
                        result = {"result": raw_result.content[0].text}
                else:
                    result = {"result": str(raw_result.content)}
            else:
                result = {"result": str(raw_result)}
            
            return StepResult(
                success=True,
                output=result,
                metadata={
                    "tool": tool_name,
                    "parameters": parameters,
                    "reasoning": thought_content.get("reasoning")
                }
            )
            
        except Exception as e:
            logger.error(f"Error during action step: {str(e)}")
            return StepResult(success=False, error=str(e))

    async def observe(self, action: Step) -> StepResult:
        """Analyze action results using LLM."""
        try:
            # Create prompt for analyzing the action result
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
            logger.error(f"Error during observation step: {str(e)}")
            return StepResult(success=False, error=str(e))

    async def cleanup(self):
        """Clean up resources."""
        try:
            logger.debug("Starting cleanup")
            
            if self.llm:
                await self.llm.close()
                
            await self.exit_stack.aclose()
            logger.debug("Cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise