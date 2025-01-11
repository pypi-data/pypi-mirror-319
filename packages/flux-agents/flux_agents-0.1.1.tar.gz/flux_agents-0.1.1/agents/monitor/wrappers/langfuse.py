"""
Langfuse integration wrapper for agent functions.

This module provides a wrapper that integrates Langfuse monitoring and tracing
functionality into agent functions, enabling detailed tracking and analysis of
agent operations through the Langfuse platform.
"""
from functools import wraps
import traceback

import langfuse

from agents.config.models import AgentStatus

from agents.storage.message import Message
from agents.storage.message import Message, Sender, MessageType
from agents.agent.enums import AgentType
    

from langfuse import Langfuse
langfuse = Langfuse()


def langfuse_agent_wrapper(func):
    """
    Wrapper that adds Langfuse monitoring to agent functions.
    
    Provides comprehensive monitoring including:
    - Input/output message tracking
    - Execution timing
    - Error logging
    - Session tracking
    - Agent metadata collection
    - Langfuse trace generation
    
    :param func: Agent function to wrap
    :type func: Callable
    :return: Wrapped function with Langfuse monitoring
    :rtype: Callable
    """
    
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        """
        Wrapper implementation that handles Langfuse monitoring and message flow.
        
        :param self: Agent instance
        :param args: Positional arguments for the agent function
        :param kwargs: Keyword arguments for the agent function
        :return: Response message or error message
        :rtype: Message
        """
        try:
            input_message = kwargs.get('input_message') or args[0]
            if not isinstance(input_message, Message):
                raise ValueError("Input Message class is required for agent!")
                
            self.agent_status = AgentStatus.RUNNING
            
            # Ingests data from messages
            if self.type != AgentType.WORKER:
                await self.state.ingest_message_data(input_message)
                
            self.agent_log.log_input(input_message)
         
            # Execute main function
            result = await func(self, *args, **kwargs)

            if not isinstance(result, Message):
                raise ValueError("Output Message class is required for agent!")
            
            self.agent_log.log_output(result)
            
            self.agent_status = AgentStatus.COMPLETED
            
            return result
            
        except:
            error = traceback.format_exc()
            error_message = Message(
                content = f'Error: {error}',
                sender = Sender.AI,
                type = MessageType.ERROR
            )
            self.agent_log.log_error(error_message)
            self.agent_status = AgentStatus.FAILED
            
            return error_message
        
        finally:
            # Add Langfuse trace
            input_text = self.agent_log.input_text()
            output_text = self.agent_log.output_text()
            
            langfuse.trace(
                name = f"{self.name}:{func.__name__}",
                input = input_text,
                output = output_text,
                session_id = self.session_id,
                metadata = {
                    "agent_type": self.type
                }
            )
            if self.agent_status == AgentStatus.FAILED:
                self.logger.error(error) 
        
    return wrapper