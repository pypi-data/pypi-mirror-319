"""
Default agent wrapper implementation.

This module provides a basic wrapper for agent functions that handles message
tracking, state management, and error handling without additional logging.
"""

from datetime import datetime   


from agents.config.models import AgentStatus
from agents.storage.message import Message, Sender, MessageType
from agents.agent.enums import AgentType


def default_agent_wrapper(func):
    """
    Default wrapper for agent functions.
    
    Provides basic message tracking, state management, and error handling.
    Does not include additional logging or monitoring.
    
    :param func: Agent function to wrap
    :type func: Callable
    :return: Wrapped function
    :rtype: Callable
    """
    async def wrapper(self, *args, **kwargs):
        """
        Wrapper implementation that handles message flow and state.
        
        :param self: Agent instance
        :param args: Positional arguments for the agent function
        :param kwargs: Keyword arguments for the agent function
        :return: Response message or error message
        :rtype: Message
        """
        start_time = datetime.now()
        
        input_message = kwargs.get('input_message') or args[0]
        if not isinstance(input_message, Message):
            raise ValueError("Input Message class is required for agent!")
                
        try:
            self.agent_status = AgentStatus.RUNNING
            
            # Ingests data from message 
            if self.type != AgentType.WORKER:
                await self.state.ingest_message_data(input_message)

            # Execute main function
            result = await func(self, *args, **kwargs)

            if not isinstance(result, Message):
                raise ValueError("Output Message class is required for agent!")
            
            self.agent_status = AgentStatus.COMPLETED
            return result
            
        except:
            import traceback
            error = traceback.format_exc()
        
            self.agent_status = AgentStatus.FAILED
            return Message(
                content = f'Error: {error}', 
                sender = Sender.AI, 
                type = MessageType.ERROR
            )
        finally:
            if self.agent_status == AgentStatus.FAILED:
                self.logger.error(error)
        
    return wrapper