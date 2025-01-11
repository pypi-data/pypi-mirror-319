"""
Logging wrapper implementation for agent functions.

This module provides a wrapper that adds comprehensive logging functionality
to agent functions, including input/output tracking, timing, and error logging.
"""

from datetime import datetime
from functools import wraps
import traceback

from agents.config.models import AgentStatus
from agents.storage.message import Message, Sender, MessageType
from agents.agent.enums import AgentType


def logging_agent_wrapper(func):
    """Wrapper for logging agent execution"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            start_time = datetime.now()
            
            input_message = kwargs.get('input_message') or args[0]
            if not isinstance(input_message, Message):
                raise ValueError("Input Message class is required for agent!")
                
            self.agent_status = AgentStatus.RUNNING
            
            # Ingests data from message
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
            self.agent_status = AgentStatus.FAILED
            error = traceback.format_exc()
            error_message = Message(
                content = f'Error: {error}', 
                sender = Sender.AI, 
                type = MessageType.ERROR
            )
            self.agent_log.log_error(error_message)
            return error_message
        finally:
            if self.agent_status == AgentStatus.FAILED:
                self.logger.error(error_message)
            
    return wrapper