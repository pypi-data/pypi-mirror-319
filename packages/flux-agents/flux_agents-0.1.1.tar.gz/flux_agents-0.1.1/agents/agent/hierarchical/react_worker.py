"""
Planning agent implementation for tool-based reasoning and action.

This module provides a Planning agent implementation that can
use tools to solve tasks through a cycle of thought, action, and observation.
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import Field
import logging
import re
from datetime import datetime
import os
import traceback

from agents.storage.message import Message, Sender, MessageType
from agents.storage.metadata import Metadata
from agents.storage.file import File
from agents.storage.context import Context, ContextType

from tools.models import Tool, InternalParameterType

from agents.config.models import Logging
from agents.agent.models import Agent, conditional_logging, AgentType
from agents.monitor.agent_logs import AgentLog
from agents.monitor.logger import AgentLogger, AgentLogHandler

from agents.state.models import AgentState
from agents.agent.react.models import ReActConfig

from agents.agent.utils import evaluate_parameter


class ReActWorker(Agent):
    """
    ReAct worker agent that executes specific reactive tasks.
    
    :ivar type: Type identifier for the agent
    :type type: AgentType
    :ivar tools: List of available tools
    :type tools: Dict[str, Tool]
    :ivar state: State of the agent
    :type state: Optional[AgentState]
    :ivar config: Configuration for the agent
    :type config: ReActConfig
    """
    type: AgentType = Field(default = AgentType.WORKER)
    tools: Dict[str, Tool] = Field(default_factory = dict)
    
    state: Optional[AgentState] = Field(default = None)
    config: ReActConfig = Field(default_factory = ReActConfig)
    
    
    def __init__(self, *args, **kwargs):
        state = kwargs.pop('state', None)
        tools = kwargs.pop('tools', {})
        
        # Initialize pydantic model first
        super().__init__(*args, **kwargs)
        
        # Then set state and tools
        if state:
            self.state = state
        if tools:
            self.tools = tools
            
        # Setup logging
        if self.logging:
            self.agent_log = AgentLog(
                session_id = self.session_id,
                agent_name = self.name,
                agent_type = self.type,
                agent_description = self.description,
                llm = self.llm,
                source_agents = [a.name for a in self.source_agents],
                target_agents = [a.name for a in self.target_agents]
            )
            
            self.logger = AgentLogger(self.name)
            self.logger.agent_handler = AgentLogHandler(self.agent_log)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            self.logger.agent_handler.setFormatter(formatter)
            self.logger.addHandler(self.logger.agent_handler)
        else:
            self.logger = logging.getLogger(self.name)
    
    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"
    
    @property
    def tool_summary(self) -> str:
        """
        Get a summary of all tools.
        """
        tools_context = "\n".join([
            f"[{i}] {tool.text()}" for i, tool in enumerate(self.tools.values(), start=1)
        ])
        
        return tools_context
    
    
    def parse_tool_parameters(
        self,
        params_string: str,
        metadata: Optional[List[Metadata]] = None,
        files: Optional[List[File]] = None
    ) -> Dict[str, Any]:
        params = {}
        if not params_string.strip():
            return params
            
        param_pattern = r'(\w+)\s*=\s*((?:\[[^\]]*\]|\{[^\}]*\}|[^,]+))'
        param_matches = re.finditer(param_pattern, params_string)
        
        for match in param_matches:
            param_name = re.sub(r'[\n\r\t]', '', match.group(1).strip())
            param_value = match.group(2)
            
            # Lookup in metadata/files or evaluate as literal
            if metadata and param_value in [m.name for m in metadata]:
                param_value = next(m.data for m in metadata if m.name == param_value)
            elif files and param_value in [f.name for f in files]:
                param_value = next(f for f in files if f.name == param_value)
            else:
                param_value = evaluate_parameter(param_value.strip())
                
            params[param_name] = param_value
            
        return params

    
    async def call_tool(
        self, 
        response: str,
        metadata: Optional[List[Metadata]] = None,
        files: Optional[List[File]] = None
    ) -> tuple[List[Metadata], List[File], str, str, List[str]]:
        """
        Parse a response containing an Action into tool name and parameters.
        
        :param response: Full response string containing "Thought: reasoning\nAction: tool_name(param1=value1, param2=value2)"
        :type response: str
        :param metadata: List of metadata to use as parameters
        :type metadata: Optional[List[Metadata]]
        :param files: List of files to use as parameters
        :type files: Optional[List[File]]
        :return: Tuple of (metadata_list, files_list, action_string, thought, observations)
        :rtype: tuple[List[Metadata], List[File], str, str, List[str]]
        """
        # Extract thought and action using regex
        thought_match = re.search(r'Thought:\s*(.+?)(?=\nAction:|$)', response, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else ""
        
        # Extract the action line
        action_match = re.search(r'Action:\s*(.+?)(?:\n|$)', response)
        if not action_match:
            raise ValueError(f"No Action found in response: {response}")
        
        action_string = action_match.group(1).strip()
        
        # Match tool name and parameters section
        tool_match = re.match(r'(\w+)\s*\((.*)\)', action_string)
        if not tool_match:
            raise ValueError(f"Invalid tool call format: {action_string}")
        
        tool_name = tool_match.group(1)
        params_string = tool_match.group(2)

        params = self.parse_tool_parameters(
            params_string = params_string,
            metadata = metadata,
            files = files
        )
        
        chosen_tool = self.tools.get(tool_name)
        
        # Adds internal parameters to params
        if chosen_tool._has_internal_params:
            for param in chosen_tool.internal_parameters:
                match param.type:
                    case InternalParameterType.AGENT_STATE:
                        params[param.name] = self.state
                    case InternalParameterType.AGENT_CONFIG:
                        params[param.name] = self.config
                    case InternalParameterType.EMBEDDING:
                        params[param.name] = self.state.embedding_function
                    case InternalParameterType.LLM:
                        params[param.name] = self.llm
      
        tool_response = await chosen_tool(**params)
       
        response_metadata = []
        response_files = []
        observations = []
        
        def process_single_output(value: Any, name: str):
            if isinstance(value, str):
                observations.append(value)
            elif isinstance(value, File):
                response_files.append(value)
            else:
                response_metadata.append(Metadata(
                    name = name,
                    data = value,
                    agent_name = self.name
                ))
            
        # Handle different response types
        if isinstance(tool_response, dict):
            for i, (key, value) in enumerate(tool_response.items()):
                # Get return name from tool if available, otherwise use key
                return_name = chosen_tool.return_names[i] if i < len(chosen_tool.return_names) else key
                process_single_output(value, return_name)
                    
        elif isinstance(tool_response, (list, tuple)):
            for i, value in enumerate(tool_response):
                # Get return name from tool if available
                return_name = chosen_tool.return_names[i] if i < len(chosen_tool.return_names) else f"{tool_name}_{i}"
                process_single_output(value, return_name)
                    
        else:
            # Single return value - use first return name if available
            return_name = chosen_tool.return_names[0] if chosen_tool.return_names else f"{tool_name}_result"
            process_single_output(tool_response, return_name)
        
        if len(observations) > 0:
            observations = "\n".join(observations)
        else:
            observations = ""
            
        return response_metadata, response_files, action_string, thought, observations
    
    
    async def get_message_context(
        self,
        message_content: str
    ) -> Tuple[str, List[File], List[Metadata]]:
        context_text = ""
        if self.config.search_context:
            context_entries = await self.state.get_context(
                query = message_content,
                limit = self.config.context_config.item_count
            )
            if context_entries:
                context_text = "\n".join(
                    f" - {c.type.value}:\n{c.content}"
                    for c in context_entries
                )
                self.logger.info(f"Retrieved context:\n{context_text}")
                
        potential_files = await self.state.obtain_file_context(
            query = message_content,
            context_config = self.state.context_config
        )
            
        potential_metadata = await self.state.obtain_metadata_context(
            query = message_content,
            context_config = self.state.context_config
        )
        
        return context_text, potential_files, potential_metadata

 
    def format_prompt_context(
        self,
        prompt: str,
        available_metadata: Optional[List[Metadata]] = None,
        available_files: Optional[List[File]] = None,
    ) -> str:
        if available_metadata:
            metadata_summary = '\n'.join([
                metadata.content for metadata in available_metadata
            ])
        else:
            metadata_summary = ""
        
        if available_files:
            file_summary = '\n'.join([
                file.content for file in available_files
            ])
        else:
            file_summary = ""
            
        if file_summary or metadata_summary:
            prompt += f"\nAVAILABLE DATA (metadata and files can be used as tool inputs):\n"
            if file_summary:
                prompt += f"[FILES]:\n{file_summary}\n"
            if metadata_summary:
                prompt += f"[METADATA]:\n{metadata_summary}\n\n"

        prompt += f"TOOLS:\n{self.tool_summary}\n"
        
        return prompt
    
    
    def generate_react_prompt(
        self, 
        input_prompt: str,
        available_metadata: Optional[List[Metadata]] = None,
        available_files: Optional[List[File]] = None,
        runtime_context: str = ""
    ) -> str:

        input_prompt = self.format_prompt_context(
            prompt = input_prompt,
            available_metadata = available_metadata,
            available_files = available_files
        )
        
        if not os.environ.get('REACT_AGENT_PROMPT'):
            input_prompt += """RESPONSE FORMAT
Choose exactly ONE:

[1] USE TOOL
Thought: {clear reasoning for tool choice and usage}
Action: tool_name(param1=value1, param2=value2, ...)

[2] HAVE FINAL RESPONSE
Final Response: {synthesize a complete answer that:
- Summarizes key findings and context
- IF the the user query is not relevant to the toolkit then respond explaining what is needed}
Final Metadata: {metadata/file names ONLY if generated and relevant to the final response}


**CRITICAL RULES:**
1. Use a SINGLE TOOL at a time! Tools may not be parameters.
"""
        else:
            input_prompt += os.environ.get('REACT_AGENT_PROMPT')
            
        if runtime_context:
            input_prompt += f"\n{runtime_context}\n"
            
        return input_prompt
    
    
    def format_action(self, action: str) -> str:
        """
        Format an action string into a readable format.
        :param action: Action string to format
        :type action: str
        :return: Formatted action string
        :rtype: str
        """
        # Use regex to extract the tool name and parameters
        tool_match = re.match(r'(\w+)\s*\((.*)\)', action)
        if not tool_match:
            raise ValueError(f"Invalid action format: {action}")

        tool_name = tool_match.group(1)
        params_string = tool_match.group(2)

        # Parse parameters string into a readable format
        params = []
        if params_string.strip():
            param_pattern = r'(\w+)\s*=\s*((?:\[[^\]]*\]|\{[^\}]*\}|[^,]+))'
            param_matches = re.finditer(param_pattern, params_string)

            for match in param_matches:
                param_name = match.group(1).strip()
                param_value = match.group(2).strip()
                params.append(f"{param_name}={param_value}")

        formatted_params = ", ".join(params)
        return f"Thought: Using tool '{tool_name}' with parameters: {formatted_params}\n"
    
    
    def format_runtime_context(self, 
            runtime_context: str,
            iterations: int,
            thought: str,
            action_string: str,
            observations: str,
            tool_metadata: List[Metadata],
            tool_files: List[File],
        ) -> str:
        """
        Format the runtime context into a readable format.
        """
        if iterations == 0:
            runtime_context += "\nEXECUTION HISTORY:\n"

        runtime_context += f"Step {iterations + 1}:\n> Thought: {thought}\n> Action: {action_string}\n> Results:\n"
        if observations:
            runtime_context += f"  - Observations: {observations}\n  - Generated:"

        if tool_metadata or tool_files:
            if tool_metadata:
                metadata_summary = '\n'.join([
                    metadata.content for metadata in tool_metadata
                ])
                runtime_context += f"  * Metadata:\n\t{metadata_summary}\n"
                    
            if tool_files:
                file_summary = '\n'.join([
                    file.content for file in tool_files
                ])
                runtime_context += f"\n  * Files:\n\t{file_summary}\n"

        return runtime_context
    
    
    @conditional_logging()
    async def send_react_message(
        self,
        input_message: Message
    ) -> Message:
        """
        Process a message using the ReAct cycle of thought, action, and observation.
        
        :param content: Message content to process
        :type content: Union[str, Message]
        :param sender: Entity sending the message
        :type sender: Sender
        :param max_iterations: Maximum number of ReAct cycles
        :type max_iterations: int
        :param metadata: Additional metadata for the message
        :return: Final response message
        :rtype: Message
        """
        context_text, potential_files, potential_metadata = await self.get_message_context(
            message_content = input_message.content
        )
  
        # Build input prompt
        input_prompt = f"SYSTEM\nYou are an AI ReAct agent that uses tools to solve tasks through reasoning and action.\n"
        if self.config.task_prompt:
            input_prompt += f"{self.config.task_prompt}\n"
        
        input_prompt += f"\nREQUEST: {input_message.content}\n"
            
        if self.config.search_context:
            input_prompt += f'\nPREVIOUS INTERACTIONS:\n{context_text}\n'
            
        react_prompt = self.generate_react_prompt(
            input_prompt = input_prompt,
            available_metadata = potential_metadata,
            available_files = potential_files
        )
        #self.logger.info(f'LLM prompt: {react_prompt}')
      
        # Restrict token output to prevent multiple steps
        iterations = 0
        context_flag = False
        generated_metadata_names = []
        final_metadata, final_files = [], []
        retry_react_prompt = None
        runtime_context = ""
        
        # Main agent loop
        while iterations < self.config.max_iterations:
            try:
                if retry_react_prompt:
                    llm_response = await self.llm(
                        retry_react_prompt
                    )
                else:
                    react_prompt = self.generate_react_prompt(
                        input_prompt = input_prompt,
                        available_metadata = potential_metadata,
                        available_files = potential_files,
                        runtime_context = runtime_context
                    )
                    llm_response = await self.llm(
                        react_prompt
                    )
            
                self.logger.info(f'LLM response: {llm_response}')
               
                if 'Action:' in llm_response:
                    (
                        tool_metadata, 
                        tool_files, 
                        action_string, 
                        thought, 
                        observations
                    ) = await self.call_tool(
                        response = llm_response,
                        metadata = potential_metadata,
                        files = potential_files
                    )
                    potential_files.extend(tool_files)
                    potential_metadata.extend(tool_metadata)
                    
                    generated_metadata_names.extend([i.name for i in tool_metadata])
                    generated_metadata_names.extend([i.name for i in tool_files])

                    if self.config.logging in [Logging.LANGFUSE, Logging.ENABLED]:
                        self.agent_log.log_action(
                            action = self.format_action(action_string),
                            thought = thought,
                            metadata = tool_metadata,
                            observations = observations
                        )
                    runtime_context = self.format_runtime_context(
                        runtime_context = runtime_context,
                        iterations = iterations,
                        thought = thought,
                        action_string = action_string,
                        observations = observations,
                        tool_metadata = tool_metadata,
                        tool_files = tool_files,
                    )
            
                elif "Final Response:" in llm_response:
                    final_response_match = re.search(r'Final Response:\s*(.*?)\s*(?:Final Metadata:|$)', llm_response, re.DOTALL)
                    if final_response_match:
                        final_response = final_response_match.group(1).strip()
                        
                        # Extract metadata if present
                        metadata_match = re.search(r'Final Metadata:\s*(.*)', llm_response)
                        
                        if metadata_match:
                            final_metadata_names = metadata_match.group(1).strip().split(',')
                            final_metadata = [item for item in potential_metadata if item.name in final_metadata_names]
                            final_files = [item for item in potential_files if item.name in final_metadata_names]
                    
                    context_flag = True
                    break
                
            except:
                error_trace = traceback.format_exc()
                self.logger.error(f'Error in ReAct cycle: {error_trace}')
                self.agent_log.log_error(
                    error_message = Message(
                        content = error_trace,
                        sender = Sender.AI,
                        type = MessageType.ITERATION_ERROR
                    )
                )
                retry_prompt = f'The previous response, {llm_response} was not valid!\nPlease try again. Error: {error_trace}'   
                retry_react_prompt = f'{react_prompt}\n{retry_prompt}'
        
            retry_react_prompt = None
            iterations += 1
 
        if self.config.search_context and context_flag:
            process_context = Context(
                type = ContextType.PROCESS,
                content = f"Input: {input_message.content}\nOutput: {final_response}",
                sender = Sender.AI,
                agent = self.name,
                context_type = "response",
                date = datetime.now()
            )
            await self.state.add_context(process_context)
            
        return Message(
            content = final_response,
            sender = Sender.AI,
            metadata = final_metadata,
            files = final_files
        )
    

    async def __call__(
        self, 
        message: str,
        **metadata
    ) -> Message:
        
        
        return await self.send_react_message(
            input_message = message,
            **metadata
        )
    