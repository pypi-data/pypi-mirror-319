"""
Planning agent implementation for tool-based reasoning and action.

This module provides a Planning agent implementation that can
use tools to solve tasks through a cycle of thought, action, and observation.
"""

from typing import List, Dict, Any, Optional, Callable, get_type_hints, Union, Tuple
from pydantic import Field
import logging
import re
from datetime import datetime
import ast
import os
import traceback

from agents.storage.message import Message, Sender, MessageType
from agents.storage.metadata import Metadata
from agents.storage.file import File
from agents.storage.context import Context, ContextType

from tools.models import Tool, ToolParameter, InternalParameterType

from agents.config.models import Logging
from agents.agent.models import Agent, conditional_logging
from agents.monitor.agent_logs import AgentLog
from agents.monitor.logger import AgentLogger, AgentLogHandler

from agents.state.models import AgentState
from agents.agent.planning.models import PlanningConfig
from agents.agent.enums import AgentType


class PlanningWorker(Agent):
    """
    Planning worker agent that executes specific planning tasks.
    
    :ivar type: Type identifier for the agent
    :type type: AgentType
    :ivar tools: List of available tools
    :type tools: Dict[str, Tool]
    :ivar config: Configuration for the agent
    :type config: PlanningConfig
    :ivar state: State of the agent
    :type state: Optional[AgentState]
    """
    type: AgentType = Field(default = AgentType.WORKER)
    tools: Dict[str, Tool] = Field(default_factory = dict)
    config: PlanningConfig = Field(default_factory = PlanningConfig)
    state: Optional[AgentState] = Field(default = None)
    
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
                session_id=self.session_id,
                agent_name=self.name,
                agent_type=self.type,
                agent_description=self.description,
                llm=self.llm,
                source_agents=[a.name for a in self.source_agents],
                target_agents=[a.name for a in self.target_agents]
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
    
    
    def parse_plan(self, plan_string: str) -> Dict[str, List[Dict[str, Any]]]:
        try:
            plan_match = re.search(r'Plan:\s*(.*?)(?=\n3\. Output Names:|$)', plan_string, re.DOTALL)
            if not plan_match:
                return {}

            plan_content = plan_match.group(1).strip()
            
            # Updated regex to handle indented key-value pairs
            step_pattern = re.compile(
                r'\[(\d+)\]\s*Step:\s*(.*?)\n'          # Step number and name
                r'\s*Tool:\s*(.*?)\n'                   # Tool name
                r'\s*Inputs:\s*(.*?)\n\s*Outputs:'      # Inputs (multiline)
                r'\s*(.*?)\n\s*Purpose:\s*(.*?)'        # Outputs and Purpose
                r'(?=\n\s*\[\d+\]|\Z)',                 # Look ahead for next step or end
                re.DOTALL
            )

            step_matches = step_pattern.finditer(plan_content)
            steps = {}

            for step_num, match in enumerate(step_matches, start=1):
                step_number = int(match.group(1))
                step_name = match.group(2).strip()
                tool_name = match.group(3).strip()
                
                # Parse indented inputs
                inputs_raw = match.group(4).strip()
                inputs = {}
                for line in inputs_raw.split('\n'):
                    line = line.strip()
                    if line and '"' in line:
                        key = line.split('"')[1]
                        if ':' in line:
                            value = line.split(':')[1].strip().strip('",')
                            inputs[key] = value

                # Parse indented outputs
                outputs_raw = match.group(5).strip()
                outputs = {}
                for line in outputs_raw.split('\n'):
                    line = line.strip()
                    if line and '"' in line:
                        key = line.split('"')[1]
                        if ':' in line:
                            value = line.split(':')[1].strip().strip('",')
                            outputs[key] = value

                purpose = match.group(6).strip()

                steps[step_number] = {
                    "step_number": step_number,
                    "step_name": step_name,
                    "tool_name": tool_name,
                    "inputs": inputs,
                    "outputs": outputs,
                    "purpose": purpose
                }
            return steps, plan_content
            
        except Exception as e:
            self.logger.warning(f"Error parsing plan: {e}")
            return {}


    async def execute_plan(
        self, 
        plan: Dict[str, List[Dict[str, Any]]],
        metadata: Optional[List[Metadata]] = None,
        files: Optional[List[File]] = None
    ):
        output_mapping = {}
        
        for step_number, step_details in plan.items():
            tool_name = step_details['tool_name']
            inputs = step_details['inputs']
            outputs = step_details['outputs']
            
            for input_name, input_value in inputs.items():
                if metadata and input_value in [m.name for m in metadata]:
                    inputs[input_name] = next(m.data for m in metadata if m.name == input_value)
                elif files and input_value in [f.name for f in files]:
                    inputs[input_name] = next(f for f in files if f.name == input_value)
                elif isinstance(input_value, str) and input_value in output_mapping:
                    inputs[input_name] = output_mapping[input_value]
                   
            tool_output = await self.call_tool(
                tool_name = tool_name,
                params = inputs,
                output_names = list(outputs.keys())
            )
            output_mapping.update(tool_output)

        return output_mapping
    

    async def call_tool(
        self, 
        tool_name: str,
        params: Dict[str, Any],
        output_names: List[str]
    ) -> tuple[List[Metadata], List[File], List[str]]:
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
        chosen_tool = self.tools.get(tool_name)
        
        # Adds internal parameters to params
        if chosen_tool._has_internal_params:
            for param in chosen_tool.internal_parameters:
                if param.type == InternalParameterType.AGENT_STATE:
                    params[param.name] = self.state
                elif param.type == InternalParameterType.AGENT_CONFIG:
                    params[param.name] = self.config
                elif param.type == InternalParameterType.EMBEDDING:
                    params[param.name] = self.state.embedding_function
                elif param.type == InternalParameterType.LLM:
                    params[param.name] = self.llm
      
        tool_response = await chosen_tool(**params)
       
        response_mapping = {}
        if isinstance(tool_response, tuple):
            for i, value in enumerate(tool_response):
                output_name = output_names[i]
                response_mapping[output_name] = value
        else:
            response_mapping[output_names[0]] = tool_response

        return response_mapping
    
    
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

    
    def extract_plan_results(
        self,
        plan_results: Dict[str, Any],
        llm_response: str
    ) -> str:
      
        output_names_match = re.search(r'Output Names:\s*\[(.*?)\]', llm_response, re.DOTALL)
        if output_names_match:
            output_names = output_names_match.group(1).strip()
            output_names = ast.literal_eval(f'[{output_names}]')
        else:
            raise ValueError(f"No output names found in the LLM response!")
      
        captured_metadata = []
        captured_files = []
        results_summary = []
        
        for output_name in output_names:
            output_value = plan_results.get(output_name)
            if isinstance(output_value, str):
                results_summary.append(output_value)
            elif isinstance(output_value, File):
                captured_files.append(output_value)
                results_summary.append(output_value.content)
            else:
                metadata = Metadata(
                    name = output_name,
                    data = output_value,
                    agent_name = self.name
                )
                captured_metadata.append(metadata)
                results_summary.append(metadata.content)
                
        results_summary = 'PLAN RESULTS:\n'.join(results_summary)

        return results_summary, captured_metadata, captured_files
   
   
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
    
    
    def generate_planning_prompt(
        self, 
        input_prompt: str,
        available_metadata: Optional[List[Metadata]] = None,
        available_files: Optional[List[File]] = None,
    ) -> str:

        input_prompt = self.format_prompt_context(
            prompt = input_prompt,
            available_metadata = available_metadata,
            available_files = available_files
        )
        
        if not os.environ.get('PLANNING_AGENT_PROMPT'):
            input_prompt += """RESPONSE FORMAT:
1. First, analyze the task and provide your reasoning:
 - IF YOU CANNOT USE THE TOOLS TO PERFORM THE TASK:
    Reasoning: {explain why the tools cannot perform the task}
    Final Response: {Ask for user reformatting of the task}
    <end response>
    **IMPORTANT: If the tools cannot perform the task, DO NOT generate a plan. Only provide the Final Response.**
 - IF YOU CAN USE THE TOOLS TO SOLVE THE TASK:
    Reasoning: {explain your understanding of the task and how you'll break it down}

2. Then, create a detailed plan using this strict format:
Plan:
[1] Step: {descriptive name for this step}
    Tool: {tool_name}
    Inputs: {
        "param1": "value1",
        ...
    }
    Outputs: {
        "output_name1": "description of what this output represents",
        ...
    }
    Purpose: {explain why this step is necessary}

[2] Step: {next step name}
    Tool: {tool_name}
    Inputs: {
        "param1": "output_name1",  # Reference outputs from previous steps using output name
        "param2": "value1", # Can be metadata/file name or a direct value
        ...
    }
    Outputs: {
        "output_name": "description"
        ...
    }
    Purpose: {explanation}

... additional steps as needed ...

3. Finally, LIST the output names from any steps that must be captured for the final response
Output Names: [output_name1, output_name2, ...]
"""
        else:
            input_prompt += os.environ.get('PLANNING_AGENT_PROMPT')
            
        return input_prompt
    
    
    async def final_response(
        self,
        results_summary: str,
        plan: str,
        input_message: Message
    ) -> str:
        summary_prompt = "You are an intelligent planning agent that has just executed a plan and obtained results."
        if self.config.task_prompt:
            summary_prompt += f"\n{self.config.task_prompt}"
        summary_prompt += f'\nINPUT QUERY:\n{input_message.content}'
        summary_prompt += f"\nEXECUTED PLAN:\n{plan}\n"
        if not results_summary:
            summary_prompt += f"\nPLAN RESULTS:\nThe generated plan failed to produce any results."
        else:
            summary_prompt += f"\nPLAN RESULTS:\n{results_summary}\n"
            
        if not os.environ.get('PLANNING_FINAL_PROMPT'):
            summary_prompt += """
INSTRUCTIONS:
- Provide a informative final answer.
- If answering a question, provide a direct answer.
- If generating a report, format as a report.
- Emphasize key information; avoid redundancy.
- If no plan/results, indicate task failure with suggestions to improve user query.
"""
        else: 
            summary_prompt += os.environ.get('PLANNING_FINAL_PROMPT')
        
        final_response = await self.llm(summary_prompt)
        return final_response
    
    
    @conditional_logging()
    async def send_planning_message(
        self,
        input_message: Message
    ) -> Message:
        """
        Process a message using the ReAct cycle of thought, action, and observation.
        
        :param content: Message content to process
        :type content: Union[str, Message]
        :param sender: Entity sending the message
        :type sender: Sender
        :param max_iterations: Maximum number of planning cycles
        :type max_iterations: int
        :param metadata: Additional metadata for the message
        :return: Final response message
        :rtype: Message
        """
        context_text, potential_files, potential_metadata = await self.get_message_context(
            message_content = input_message.content
        )
  
        # Build input prompt
        input_prompt = f"SYSTEM\nYour task is to create a detailed execution plan that breaks down the request into a series of tool executions.\n"
        if self.config.task_prompt:
            input_prompt += f"{self.config.task_prompt}\n"
        
        input_prompt += f"\nREQUEST: {input_message.content}\n"
            
        if self.config.search_context:
            input_prompt += f'\nPREVIOUS INTERACTIONS:\n{context_text}\n'
            
        planning_prompt = self.generate_planning_prompt(
            input_prompt = input_prompt,
            available_metadata = potential_metadata,
            available_files = potential_files
        )
        #self.logger.info(f'LLM prompt: {planning_prompt}')
      
        # Restrict token output to prevent multiple steps
        iterations = 0
        context_flag = False
        final_metadata, final_files = [], []
        retry_planning_prompt = None
        
        while iterations < self.config.max_iterations:
            try:
                if retry_planning_prompt:
                    llm_response = await self.llm(
                        retry_planning_prompt
                    )
                else:
                    planning_prompt = self.generate_planning_prompt(
                        input_prompt = input_prompt,
                        available_metadata = potential_metadata,
                        available_files = potential_files
                    )
                    llm_response = await self.llm(
                        planning_prompt
                    )
           
                if 'Plan:' not in llm_response and "{" not in llm_response:
                    final_response_match = re.search(r'Final Response:\s*(.*?)(?:\s*<end response>)?\s*$', llm_response, re.DOTALL)
                    final_response = final_response_match.group(1).strip()
                    break
                else:
                    # Obtains plan
                    plan_reasoning = re.search(r'Reasoning:\s*(.*?)(?=\s*(?:2\. Then,|Plan:)|$)', llm_response, re.DOTALL).group(1).strip()
                    if self.config.logging in [Logging.LANGFUSE, Logging.ENABLED]:
                        self.agent_log.log_plan(plan = plan_reasoning)
                    print(f'LLM response: {llm_response}')
                    
                    # Runs plan
                    plan, plan_content = self.parse_plan(llm_response)
    
                    plan_results = await self.execute_plan(
                        plan = plan,
                        metadata = potential_metadata,
                        files = potential_files
                    )
                    results_summary, final_metadata, final_files = self.extract_plan_results(
                        plan_results = plan_results,
                        llm_response = llm_response
                    )
                    
                    # Obtains results
                    if self.config.plan_sythesis:
                        final_response = await self.final_response(
                            results_summary = results_summary,
                            plan = plan_content,
                            input_message = input_message
                        )
                    else:
                        final_response = results_summary
                    break

            except:
                error = traceback.format_exc()
                self.logger.error(f'Error in Planning cycle: {error}')
                self.agent_log.log_error(
                    error_message = Message(
                        content = error,
                        sender = Sender.AI,
                        type = MessageType.ITERATION_ERROR
                    )
                )
                retry_prompt = f'The previous response, {llm_response} was not valid!\nPlease try again. \nError: {error}'   
                retry_planning_prompt = f'{planning_prompt}\n{retry_prompt}'
                final_response = f'Planning agent failed -> {error}'
            retry_planning_prompt = None
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
        
        
        return await self.send_planning_message(
            input_message = message,
            **metadata
        )
    