"""
Hierarchical agent implementation for tool-based reasoning and action.

This module provides a Hierarchical agent implementation that can
use tools to solve tasks through a cycle of thought, action, and observation.
"""

from typing import List, Dict, Any, Optional, Callable, Union, Tuple
from pydantic import Field
import logging
import re
from datetime import datetime
import os
import asyncio
import random
import traceback

from agents.storage.message import Message, Sender
from agents.storage.metadata import Metadata
from agents.storage.file import File
from agents.storage.context import Context, ContextType

from tools.models import Tool

from agents.config.models import Logging
from agents.agent.models import Agent, conditional_logging
from agents.monitor.agent_logs import AgentLog
from agents.monitor.logger import AgentLogger, AgentLogHandler

from agents.state.models import AgentState
from agents.config.models import AgentConfig

from agents.agent.hierarchical.planning_worker import PlanningWorker
from agents.agent.hierarchical.react_worker import ReActWorker
from agents.agent.react.models import ReActConfig
from agents.agent.planning.models import PlanningConfig

from agents.agent.models import Agent
from agents.agent.hierarchical.prompts import default_worker_perspectives, default_worker_divisions
from agents.agent.enums import AgentType, WorkerType, WorkerDivision, WorkerGeneration


class HierarchicalConfig(AgentConfig):
    """
    Configuration for the Hierarchical agent.
    """
    worker_count: int = Field(default = 2)
    
    worker_type: WorkerType = Field(default = WorkerType.MIXED)
    worker_generation: WorkerGeneration = Field(default = WorkerGeneration.DEFAULT)
    worker_division: WorkerDivision = Field(default = WorkerDivision.VARY_PERSPECTIVES)
    
    react_iterations: int = Field(default = 5)
    planning_iterations: int = Field(default = 1)

    synthesize_results: bool = Field(default = True)
    
    
class HierarchicalAgent(Agent):
    """
    Hierarchical agent that combines reasoning and acting through tool use.
    
    :ivar type: Type identifier for the agent
    :type type: str
    :ivar tools: List of available tools
    :type tools: List[Tool]
    """
    type: AgentType = Field(default = AgentType.HIERARCHICAL)
    tools: Dict[str, Tool] = Field(default_factory = dict)
    
    config: HierarchicalConfig = Field(default_factory = HierarchicalConfig)
    agent_pattern: Agent = Field(default = None)
    
    
    def __init__(self, *args, **kwargs):
        # Extract embedding function before super init
        embedding_function = kwargs.get('embedding_function')
        
        # If embedding function provided, create state with it
        if embedding_function:
            kwargs['state'] = AgentState(embedding_function = embedding_function)
        
        super().__init__(*args, **kwargs)
        
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
       

    async def add_tool(
        self,
        tool: Union[Tool, Callable]
    ) -> Tool:
        """
        Add a tool to the agent's available tools.
        
        :param tool: Tool to add
        :type tool: Union[Tool, Callable]
        :return: Created tool
        :rtype: Tool
        """

        self.tools[tool.name] = tool

    
    @property
    def tool_summary(self) -> str:
        """
        Get a summary of all tools.
        """
        tools_context = "\n".join([
            f"[{i}] {tool.text()}" for i, tool in enumerate(self.tools.values(), start=1)
        ])
        
        return tools_context
        
    
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
    
    
    def format_perspective_prompt(
        self,
        input_message: Message,
        context_text: Optional[str] = None,
        potential_metadata: Optional[List[Metadata]] = None,
        potential_files: Optional[List[File]] = None
    ) -> str:
        """Format prompt for varying perspectives worker generation."""
        
        perspective_prompt = f"""You are a perspective generation agent. Your task is to create {self.config.worker_count} DIFFERENT VIEWPOINTS or ANGLES from which to analyze and approach the following query. Each perspective should offer a unique way of thinking about the ENTIRE problem.

**IMPORTANT**: Do NOT divide the task into subtasks. Instead, create distinct perspectives that will each examine the FULL problem through different lenses.

QUERY TO ANALYZE:
{input_message.content}

AVAILABLE RESOURCES:"""

        perspective_prompt += self.format_prompt_context(
            prompt = perspective_prompt,
            available_metadata = potential_metadata,
            available_files = potential_files
        )

        if context_text:
            perspective_prompt += f"\nPAST CONTEXT:\n{context_text}\n"

        perspective_prompt += """

RESPONSE FORMAT:
For each perspective, provide:

[1] Worker: {descriptive name that reflects the perspective}
Perspective: {detailed description of how this viewpoint approaches the problem}
Focus Areas: {
    "area1": "how this perspective examines this aspect",
    "area2": "how this perspective examines another aspect",
    ...
}
Value: {explain how this perspective contributes unique insights}

    ...additional perspectives as needed...

CRITICAL RULES:
1. Each perspective must analyze the ENTIRE problem, not a subset
2. Perspectives should be complementary but independent
3. Focus on different ways of THINKING about the problem, not different PARTS of the problem
4. Avoid task division - every worker should consider the complete problem
"""
        
        return perspective_prompt
               
    
    def parse_perspectives(self, perspective_string: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse the LLM response containing worker perspectives.
        
        :param perspective_string: Full response string containing perspectives
        :return: Dictionary of parsed worker perspectives
        """
        try:
            perspectives_match = re.search(r'Perspectives:\s*(.*?)(?=\n3\. Finally|$)', perspective_string, re.DOTALL)
            if not perspectives_match:
                return {}

            perspective_content = perspectives_match.group(1).strip()
            
            # Regex pattern for parsing worker perspectives
            worker_pattern = re.compile(
                r'\[(\d+)\]\s*Worker:\s*(.*?)\n'          # Worker number and name
                r'\s*Perspective:\s*(.*?)\n'               # Perspective description
                r'\s*Focus Areas:\s*(.*?)\n'              # Focus areas (multiline)
                r'\s*Approach:\s*(.*?)\n'                 # Approach
                r'\s*Value:\s*(.*?)'                      # Value
                r'(?=\n\s*\[\d+\]|\Z)',                  # Look ahead for next worker or end
                re.DOTALL
            )

            worker_matches = worker_pattern.finditer(perspective_content)
            perspectives = {}

            for match in worker_matches:
                worker_number = int(match.group(1))
                worker_name = match.group(2).strip()
                
                # Parse focus areas
                focus_areas_raw = match.group(4).strip()
                focus_areas = {}
                for line in focus_areas_raw.split('\n'):
                    line = line.strip()
                    if line and '"' in line:
                        key = line.split('"')[1]
                        if ':' in line:
                            value = line.split(':')[1].strip().strip('",')
                            focus_areas[key] = value

                perspectives[worker_number] = {
                    "worker_name": worker_name,
                    "perspective": match.group(3).strip(),
                    "focus_areas": focus_areas,
                    "approach": match.group(5).strip(),
                    "value": match.group(6).strip()
                }

            return perspectives
            
        except Exception as e:
            self.logger.warning(f"Error parsing perspectives: {e}")
            return {}
    
    
    def format_division_prompt(
        self,
        input_message: Message,
        context_text: Optional[str] = None,
        potential_metadata: Optional[List[Metadata]] = None,
        potential_files: Optional[List[File]] = None
    ) -> str:
        """Format prompt for division of labor worker generation.
        
        :param input_message: Input message to process
        :type input_message: Message
        :param potential_metadata: Potential metadata to use
        :type potential_metadata: Optional[List[Metadata]]
        :param potential_files: Potential files to use
        :type potential_files: Optional[List[File]]
        :return: Formatted division prompt
        :rtype: str
        """
        division_prompt = f"""You are a task decomposition agent designed to break down a complex query into {self.config.worker_count} distinct subtasks.
    Each worker will handle a specific part of the solution, working together to create a comprehensive answer.

    AVAILABLE RESOURCES:"""

        division_prompt += self.format_prompt_context(
            prompt = division_prompt,
            available_metadata = potential_metadata,
            available_files = potential_files
        )
        
        if self.config.task_prompt:
            division_prompt += f"\nMAIN OBJECTIVE:\n{self.config.task_prompt}\n"
                
        division_prompt += f"\nQUERY TO DECOMPOSE:\n{input_message.content}\n"
        
        if context_text:
            division_prompt += f"\nPAST CONTEXT:\n{context_text}\n"
        
        division_prompt += """
RESPONSE FORMAT:
1. First, analyze the task and provide your decomposition strategy:
Task Analysis: {explain how this task can be broken down into discrete subtasks}

2. Then, define each worker's responsibilities using this format:
Workers:
[1] Worker: {descriptive name for this worker}
    Subtask: {clear description of this worker's specific responsibility}
    Input Requirements: {
        "requirement1": "what this worker needs to start their task",
        "requirement2": "another prerequisite",
        ...
    }
    Expected Output: {
        "output1": "what this worker will produce",
        "output2": "another deliverable",
        ...
    }
    Success Criteria: {how to determine if this subtask is completed successfully}

... additional workers as needed ...

3. Finally, describe the integration strategy:
Integration Plan: {explain how the individual worker outputs will be combined into the final solution}
"""

        return division_prompt
    
    
    def parse_division(self, division_string: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse the LLM response containing worker divisions.
        
        :param division_string: Full response string containing task divisions
        :return: Dictionary of parsed worker divisions
        """
        try:
            # Extract workers section
            workers_match = re.search(r'Workers:\s*(.*?)(?=\n3\. Finally|$)', division_string, re.DOTALL)
            if not workers_match:
                return {}

            worker_content = workers_match.group(1).strip()
            
            # Regex pattern for parsing worker divisions
            worker_pattern = re.compile(
                r'\[(\d+)\]\s*Worker:\s*(.*?)\n'              # Worker number and name
                r'\s*Subtask:\s*(.*?)\n'                      # Subtask description
                r'\s*Input Requirements:\s*(.*?)\n'           # Input requirements (multiline)
                r'\s*Expected Output:\s*(.*?)\n'              # Expected output (multiline)
                r'\s*Success Criteria:\s*(.*?)'               # Success criteria
                r'(?=\n\s*\[\d+\]|\Z)',                      # Look ahead for next worker or end
                re.DOTALL
            )

            worker_matches = worker_pattern.finditer(worker_content)
            divisions = {}

            for match in worker_matches:
                worker_number = int(match.group(1))
                worker_name = match.group(2).strip()
                
                # Parse input requirements
                input_reqs_raw = match.group(4).strip()
                input_requirements = {}
                for line in input_reqs_raw.split('\n'):
                    line = line.strip()
                    if line and '"' in line:
                        key = line.split('"')[1]
                        if ':' in line:
                            value = line.split(':')[1].strip().strip('",')
                            input_requirements[key] = value
                            
                # Parse expected outputs
                outputs_raw = match.group(5).strip()
                expected_outputs = {}
                for line in outputs_raw.split('\n'):
                    line = line.strip()
                    if line and '"' in line:
                        key = line.split('"')[1]
                        if ':' in line:
                            value = line.split(':')[1].strip().strip('",')
                            expected_outputs[key] = value

                divisions[worker_number] = {
                    "worker_name": worker_name,
                    "subtask": match.group(3).strip(),
                    "input_requirements": input_requirements,
                    "expected_outputs": expected_outputs,
                    "success_criteria": match.group(7).strip()
                }

            integration_match = re.search(r'Integration Plan:\s*(.*?)(?=\Z)', division_string, re.DOTALL)
            if integration_match:
                divisions['integration_plan'] = integration_match.group(1).strip()
                
            return divisions
                
        except Exception as e:
            self.logger.warning(f"Error parsing divisions: {e}")
            return {}
        
    
    def format_worker_task_prompt(
        self,
        worker_data: Dict[str, Any],
        division_type: WorkerDivision
    ) -> str:
        """
        Format worker data into a task prompt that will be used as the worker's system prompt.
        
        :param worker_data: Dictionary containing worker configuration
        :param division_type: Type of worker division (VARY_PERSPECTIVES or DIVISION_OF_LABOR)
        :return: Formatted task prompt
        """
        task_prompt = ""
        match division_type:
            case WorkerDivision.VARY_PERSPECTIVES:
                task_prompt = f"""
ROLE AND PERSPECTIVE:
Role: {worker_data['worker_name']}
Primary Perspective: {worker_data['perspective']}
Key Focus Areas: {worker_data['focus_areas']}
"""
                if "constraints" in worker_data:
                    task_prompt += f"""
OPERATING CONSTRAINTS:
{worker_data['constraints']}"""

                task_prompt += """

APPROACH GUIDELINES:
1. Always analyze problems through your assigned perspective
2. Provide insights that leverage your unique viewpoint
3. Acknowledge when issues fall outside your perspective's scope"""

            case WorkerDivision.DIVISION_OF_LABOR:
                task_prompt = f"""
ROLE INFO
Role: {worker_data['worker_name']}
Primary Responsibility: {worker_data['subtask']}

REQUIREMENTS:
Input Requirements:
{chr(10).join(f'- {key}: {value}' for key, value in worker_data['input_requirements'].items())}

Expected Outputs:
{chr(10).join(f'- {key}: {value}' for key, value in worker_data['expected_outputs'].items())}

Success Criteria: {worker_data['success_criteria']}"""

                task_prompt += """
            
WORKER GUIDELINES:
1. Focus on your assigned subtask
2. Produce outputs that match the specified format
3. Validate results against success criteria
4. Signal if requirements are unclear"""

                task_prompt += """

            COLLABORATION PROTOCOL
            -------------------
            - Stay within your defined scope
            - Maintain clear input/output interfaces
            - Flag any blockers or dependencies
            - Optimize for integration with other workers
            """

            case WorkerDivision.REPLICA:
                task_prompt = ""
            
        return task_prompt.strip()


    async def format_workers(
        self, 
        input_message: Message,
        context_text: Optional[str] = None,
        potential_metadata: Optional[List[Metadata]] = None,
        potential_files: Optional[List[File]] = None
    ) -> str:
        """
        Format and generate worker agents based on perspectives.
        
        :param input_message: Input message to process
        :type input_message: Message
        :param context_text: Context text to use
        :type context_text: Optional[str]
        :param potential_metadata: Potential metadata to use
        :type potential_metadata: Optional[List[Metadata]]
        :param potential_files: Potential files to use
        :type potential_files: Optional[List[File]]
        :return: Formatted plan text incorporating worker perspectives
        """
        
        match self.config.worker_division:
            case WorkerDivision.VARY_PERSPECTIVES:
                if self.config.worker_generation == WorkerGeneration.DEFAULT:
                    worker_data = {key:value for i, (key, value) in enumerate(default_worker_perspectives.items()) if i + 1 <= self.config.worker_count}
                            
                elif self.config.worker_generation == WorkerGeneration.AUTO:
                    if os.environ.get('LLM_PERSPECTIVE_PROMPT'):
                        worker_perspective_prompt = os.environ.get('LLM_PERSPECTIVE_PROMPT')
                    else:
                        worker_perspective_prompt = self.format_perspective_prompt(
                            input_message = input_message,
                            context_text = context_text,
                            potential_metadata = potential_metadata,
                            potential_files = potential_files
                        ) 
                    
                    worker_prompt = await self.llm(worker_perspective_prompt)
                    self.logger.info(f'Worker prompt:\n{worker_prompt}')
                  
                    worker_data = self.parse_perspectives(worker_prompt)
                   
            case WorkerDivision.DIVISION_OF_LABOR:
                if self.config.worker_generation == WorkerGeneration.DEFAULT:
                    worker_data = {key:value for i, (key, value) in enumerate(default_worker_divisions.items()) if i + 1 <= self.config.worker_count}
                elif self.config.worker_generation == WorkerGeneration.AUTO:
                    if os.environ.get('LLM_DIVISION_PROMPT'):
                        worker_division_prompt = os.environ.get('LLM_DIVISION_PROMPT')
                    else:
                        worker_division_prompt = self.format_division_prompt(
                            input_message = input_message,
                            context_text = context_text,
                            potential_metadata = potential_metadata,
                            potential_files = potential_files
                        )
                    worker_prompt = await self.llm(worker_division_prompt)
                    self.logger.info(f'Worker prompt:\n{worker_prompt}')
                    worker_data = self.parse_division(worker_prompt)
            case WorkerDivision.REPLICA:
                worker_data = {key:{} for key in range(self.config.worker_count)}
                
            case _:
                raise ValueError(f"Invalid LLM worker generation: {self.config.worker_generation}")
            
        if self.config.worker_type == WorkerType.REACT:
            for key in worker_data:
                worker_data[key]['worker_type'] = WorkerType.REACT
                
        elif self.config.worker_type == WorkerType.PLANNING:
            for key in worker_data:
                worker_data[key]['worker_type'] = WorkerType.PLANNING
        elif self.config.worker_type == WorkerType.MIXED:
            react_count = self.config.worker_count // 2
            planning_count = self.config.worker_count - react_count
            worker_types = [WorkerType.REACT] * react_count + [WorkerType.PLANNING] * planning_count
            random.shuffle(worker_types)
            for key, worker_type in zip(worker_data.keys(), worker_types):
                worker_data[key]['worker_type'] = worker_type
                    
        worker_prompts = {}
        for key, value in worker_data.items():
            worker_prompts[key] = self.format_worker_task_prompt(
                worker_data = value,
                division_type = self.config.worker_division
            )
            
        return worker_prompts, worker_data
        
    
    async def final_response(
        self,
        results_summary: str,
        plan: str,
        input_message: Message
    ) -> str:
        summary_prompt = "You are an intelligent planning agent that has just executed a plan and obtained results."
        if self.config.task_prompt:
            summary_prompt += f"\nSYSTEM PROMPT:\n{self.config.task_prompt}"
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


    async def execute_workers(
        self,
        input_message: Message,
        worker_agents: List[Union[ReActWorker, PlanningWorker]],
        **kwargs
    ) -> Dict[str, Optional[Message]]:
        """
        Execute all workers concurrently with no dependencies between them.
        
        :param input_message: Input message to process
        :param worker_agents: List of worker agents to execute
        :return: Dictionary of worker responses, with None for failed workers
        """
        async def run_worker(worker: Union[ReActWorker, PlanningWorker]) -> Tuple[str, Optional[Message]]:
            response = await worker(input_message, **kwargs)
            return worker.name, response

        # Create and gather all tasks simultaneously
        tasks = [run_worker(worker) for worker in worker_agents]
        results = await asyncio.gather(*tasks, return_exceptions = True)
        
        agent_results = {}
        for worker, (_, output_message) in zip(worker_agents, results):
            if 'Error:' not in output_message.content:
                agent_results[worker.name] = output_message
        self.logger.info(f'{len(agent_results)}/{len(worker_agents)} workers yielded results!')
        
        return agent_results


    async def llm_response_synthesis(
        self,
        input_message: Message,
        agent_results: Dict[str, Optional[Message]]
    ) -> Message:
        """
        Synthesize worker responses using LLM and extract specific metadata/files.
        
        :param input_message: Original input message
        :param agent_results: Dictionary of worker responses
        :return: Synthesized message with selected metadata and files
        """
        metadata_check = any(result.metadata for result in agent_results.values())
        files_check = any(result.files for result in agent_results.values())
        
        synthesize_prompt = f"""SYSTEM
You are an intelligent synthesis agent responsible for synthesizing the responses of multiple agent workers.

INPUT QUERY: {input_message.content}

WORKER RESPONSES:
    """
        # Add worker responses and their metadata/files
        for worker_name, result in agent_results.items():
            synthesize_prompt += f"\n[{worker_name}]:\n{result.content}\n"
            if result.metadata:
                synthesize_prompt += "METADATA:\n"
                for metadata in result.metadata:
                    synthesize_prompt += f"- {metadata.name}: {metadata.content}\n"
            if result.files:
                synthesize_prompt += "FILES:\n"
                for file in result.files:
                    synthesize_prompt += f"- {file.name}: {file.content}\n"
                    
        if not any((metadata_check, files_check)):
            final_metadata = []
            final_files = []
            synthesize_prompt += """
INSTRUCTIONS:
1. Synthesize the worker responses into a coherent answer, using what is relevant to the input query.
"""     
            final_content = await self.llm(synthesize_prompt)
        else:
            synthesize_prompt += """
INSTRUCTIONS:
1. Synthesize the worker responses into a coherent answer, using what is relevant to the input query.
2. List selected metadata and files using EXACTLY this format:

RESPONSE FORMAT:
FINAL METADATA: [...]
FINAL FILES: [...]
SYNTHESIZED RESPONSE: <your synthesized response here>
"""
            response = await self.llm(synthesize_prompt)
            
            # Extract metadata and file names using regex
            metadata_pattern = r'FINAL METADATA:\s*\[(.*?)\]'
            files_pattern = r'FINAL FILES:\s*\[(.*?)\]'
            
            metadata_match = re.search(metadata_pattern, response, re.DOTALL)
            files_match = re.search(files_pattern, response, re.DOTALL)
            
            # Process metadata selections
            final_metadata = []
            if metadata_match:
                metadata_names = [
                    name.strip().strip('"\'').strip('`') 
                    for name in metadata_match.group(1).split(',') 
                    if name.strip()
                ]
               
                # Get actual metadata objects
                for name in metadata_names:
                    for result in agent_results.values():
                        for metadata in result.metadata:
                            if metadata.name == name:
                                final_metadata.append(metadata)
                                break
                                
            # Process file selections
            final_files = []
            if files_match:
                file_names = [
                    name.strip().strip('"\'') 
                    for name in files_match.group(1).split(',') 
                    if name.strip()
                ]
                # Get actual file objects
                for name in file_names:
                    for result in agent_results.values():
                        for file in result.files:
                            if file.name == name:
                                final_files.append(file)
                                break
            
            # Remove the selection lists from the response
            final_content = re.sub(r'FINAL (?:METADATA|FILES):\s*\[.*?\]\s*', '', response, flags=re.DOTALL)
            if 'SYNTHESIZED RESPONSE:' in final_content:
                final_content = final_content.split('SYNTHESIZED RESPONSE:', 1)[1].strip()
    
        return final_content.strip(), final_metadata, final_files
        
        
    async def synthesize_results(
        self,
        agent_results: Dict[str, Optional[Message]],
        input_message: Message
    ) -> Tuple[str, List[Metadata], List[File]]:
        """
        Synthesize results from multiple workers by combining metadata and files.
        
        :param agent_results: Dictionary of worker responses
        :return: Tuple of (final_metadata, final_files)
        """
    
        # Process each worker's results
        if self.config.synthesize_results:
            final_content, final_metadata, final_files = await self.llm_response_synthesis(
                agent_results = agent_results,
                input_message = input_message
            )
            
        else:
            final_content = ""
            final_metadata = {}  
            final_files = {}      
        
            for worker_name, result in agent_results.items():
                if not result:
                    continue
                
                final_content += f"{worker_name}:\n{result.content}\n"
                
                # Process metadata
                for metadata in result.metadata:
                    if not metadata:
                        continue

                    if metadata.name in final_metadata:
                        existing_size = len(str(final_metadata[metadata.name].content))
                        new_size = len(str(metadata.content))
                        
                        if new_size > existing_size:
                            content_exists = any(
                                str(m.content) == str(metadata.content)
                                for m in final_metadata.values()
                                if m.name != metadata.name
                            )
                            if not content_exists:
                                final_metadata[metadata.name] = metadata
                    else:
                        content_exists = any(
                            str(m.content) == str(metadata.content)
                            for m in final_metadata.values()
                        )
                        if not content_exists:
                            final_metadata[metadata.name] = metadata
                        
                # Process files
                for file in result.files:
                    if not file:
                        continue
                    
                    if file.name in final_files:
                        existing_size = len(str(final_files[file.name].data))
                        new_size = len(str(file.data))
                        
                        if new_size > existing_size:
                            data_exists = any(
                                str(f.data) == str(file.data)
                                for f in final_files.values()
                                if f.name != file.name
                            )
                            if not data_exists:
                                final_files[file.name] = file
                    else:
                        data_exists = any(
                            str(f.data) == str(file.data)
                            for f in final_files.values()
                        )
                        if not data_exists:
                            final_files[file.name] = file
                
        return final_content, final_metadata, final_files
    
    
    @conditional_logging()
    async def send_hierarchical_message(
        self,
        input_message: Message
    ) -> Message:
        """
        Process a message using the ReAct cycle of thought, action, and observation.
        
        :param content: Message content to process
        :type content: Union[str, Message]
        :param sender: Entity sending the message
        :type sender: Sender
        :param metadata: Additional metadata for the message
        :return: Final response message
        :rtype: Message
        """
        context_text, potential_files, potential_metadata = await self.get_message_context(
            message_content = input_message.content
        )
  
        # Obtains worker prompts
        worker_prompts, worker_data = await self.format_workers(
            input_message = input_message,
            context_text = context_text,
            potential_metadata = potential_metadata,
            potential_files = potential_files
        )
        
        # Creates agent workers
        worker_agents = []
        for num, (worker_prompt, worker_data) in enumerate(zip(worker_prompts.values(), worker_data.values())):
        
            if worker_data['worker_type'] == WorkerType.REACT:
                worker = ReActWorker(
                    name = worker_data.get('worker_name', str(num)),
                    session_id = self.session_id,
                    tools = self.tools,
                    llm = self.llm,
                    state = self.state,
                    config = ReActConfig(
                        logging = self.config.logging,
                        task_prompt = worker_prompt if worker_prompt else "",
                        max_iterations = self.config.react_iterations
                    )
                )
            elif worker_data['worker_type'] == WorkerType.PLANNING:
                worker = PlanningWorker(
                    name = worker_data.get('worker_name', str(num)),
                    tools = self.tools,
                    session_id = self.session_id,
                    llm = self.llm,
                    state = self.state,
                    config = PlanningConfig(
                        logging = self.config.logging,
                        task_prompt = worker_prompt if worker_prompt else "",
                        max_iterations = self.config.planning_iterations
                    )
                )
            worker_agents.append(worker)
        
        # Executes workers
        worker_responses = await self.execute_workers(
            input_message = input_message,
            worker_agents = worker_agents
        )

        final_content, final_metadata, final_files = await self.synthesize_results(
            agent_results = worker_responses,
            input_message = input_message
        )
      
        if self.config.search_context:
            process_context = Context(
                type = ContextType.PROCESS,
                content = f"Input: {input_message.content}\nOutput: {final_content}",
                sender = Sender.AI,
                agent = self.name,
                context_type = "response",
                date = datetime.now()
            )
            await self.state.add_context(process_context)
            
        return Message(
            content = final_content,
            sender = Sender.AI,
            metadata = final_metadata,
            files = final_files
        )
    

    async def __call__(
        self, 
        message: str,
        **metadata
    ) -> Message:
        
        
        return await self.send_hierarchical_message(
            input_message = message,
            **metadata
        )
