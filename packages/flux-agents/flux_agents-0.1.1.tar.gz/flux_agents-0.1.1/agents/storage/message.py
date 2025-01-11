"""
Message models and types for agent communication.

This module defines the core message types and models used for agent-to-agent 
and agent-to-user communication, including support for attachments and metadata.
"""
import os
from pydantic import BaseModel, Field, PrivateAttr
from enum import Enum
from datetime import datetime
from typing import Dict, Any, List, Optional
from functools import lru_cache
import asyncio    
import json
import base64

from utils.shared.tokenizer import encode 
from utils.shared.tokenizer import slice_text, SliceType

from agents.storage.models import IDFactory


class Sender(str, Enum):
    """
    Enumeration of possible message senders.
    
    :cvar USER: Message from a user
    :cvar AI: Message from an AI agent
    """
    USER = 'user'
    AI = 'ai'
    

class MessageType(str, Enum):
    """
    Enumeration of possible message types.
    """
    INPUT = 'input'
    OUTPUT = 'output'
    ERROR = 'error'
    INTERMEDIATE = 'intermediate'
    CONTEXT = 'context'
    ITERATION_ERROR = 'iteration_error'

class Message(BaseModel):
    """
    Base message class for agent communication.
    
    Represents a single message in an agent conversation with support
    for content, metadata, and file attachments.
    
    :ivar sender: Entity that sent the message
    :type sender: Sender
    :ivar agent_name: Name of the sending agent 
    :type agent_name: str
    :ivar date: Timestamp of the message
    :type date: datetime
    :ivar content: Main message content
    :type content: str
    :ivar metadata_ids: Optional message metadata identifiers
    :type metadata_ids: List[Union[int, str]]
    :ivar file_ids: Optional message file identifiers
    :type file_ids: List[Union[int, str]]
    :ivar annotations: Configuration and state annotations
    :type annotations: Dict[str, Any]
    """
    id: int = Field(default_factory=lambda: IDFactory.next_id(Message))
    sender: Sender = Field(default = Sender.AI)
    agent_name: str = Field(default = "default_agent")
    date: datetime = Field(default_factory = datetime.now)
    content: str = Field(default = "")
    type: MessageType = Field(default = MessageType.INTERMEDIATE)
    
    # Direct storage of metadata and files (can be objects or serialized data)
    metadata: List[Any] = Field(default_factory=list)
    files: List[Any] = Field(default_factory=list)
    
    annotations: Dict[str, Any] = Field(default_factory=dict)
    score: int = Field(default = 0)

    _tokens: Optional[List[int]] = PrivateAttr(default=None)
    
    def to_json(self) -> str:
        """
        Convert message to JSON string.
        
        :return: JSON string representation
        :rtype: str
        """
        json_data = {
            'sender': self.sender.value,
            'date': self.date.isoformat(),             
        }
        return json.dumps(json_data)
        
        
    def read_json(self, json_str: str) -> None:
        """
        Update message from JSON string.
        
        :param json_str: JSON string containing message data
        :type json_str: str
        """
        data = json.loads(json_str)
        self.sender = Sender(data['sender'])
        self.date = datetime.fromisoformat(data['date'])
        

    def __hash__(self) -> int:
        """Make Message hashable for caching"""
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        """Define equality for hashing"""
        if not isinstance(other, Message):
            return False
        return self.id == other.id

    def tokens(self) -> List[int]:
        """Get tokenized content with caching"""
        if self._tokens is None:
            self._tokens = encode(self.content)
        return self._tokens
    
    def token_length(self) -> int:
        """Get the token length"""
        if self._tokens is None:
            self._tokens = encode(self.content)
        return len(self._tokens)
    
    
    def __len__(self) -> int:
        """
        Get the length of the message content
        """
        return len(self.content)


    def text(self) -> str:
        return self.content
    

    @property
    def content(self) -> str:
        """Get the message content
        
        :return: Message content
        :rtype: str
        """
        return self._content


    @content.setter
    def content(self, value: str) -> None:
        """
        Set message content and clear length cache if content changes
        
        :param value: New message content
        :type value: str
        """
        if not hasattr(self, '_content') or self._content != value:
            self.__len__.cache_clear()
        self._content = value


    def clear_caches(self):
        """Clear all caches"""
        self.__len__.cache_clear()
      
    
    @lru_cache(maxsize = 1)
    def truncate(
        self,
        max_tokens: int,
        slice_type: SliceType = SliceType.START
    ) -> str:
        """
        Truncate the message content to a maximum number of tokens.
        
        :param max_tokens: Maximum number of tokens
        :type max_tokens: int
        """
        return slice_text(
            text = self.content,
            slice_type = slice_type,
            max_tokens = max_tokens
        )


    def __bool__(self) -> bool:
        """
        Verifies existance of object
        """
        return bool(self.content)


    def serialize(self) -> str:
        """
        Serialize message to a string representation.
        
        :return: Serialized message string
        :rtype: str
        """
        data = {
            'id': self.id,
            'sender': self.sender.value,
            'agent_name': self.agent_name,
            'date': self.date.isoformat(),
            'content': self.content,
            'type': self.type.value,
            'metadata_ids': list(self.metadata_ids),
            'file_ids': list(self.file_ids),
            'annotations': self.annotations,
            'score': self.score
        }

        # Convert any bytes objects in annotations to base64
        if self.annotations:
            data['annotations'] = self._encode_bytes_in_dict(self.annotations)
        
        return json.dumps(data)
    
    
    def _encode_bytes_in_dict(self, d: Dict) -> Dict:
        """Helper to encode bytes in dictionary values"""
        encoded = {}
        for k, v in d.items():
            if isinstance(v, bytes):
                encoded[k] = {
                    'type': 'bytes',
                    'data': base64.b64encode(v).decode('ascii')
                }
            elif isinstance(v, dict):
                encoded[k] = self._encode_bytes_in_dict(v)
            else:
                encoded[k] = v
        return encoded

    def _decode_bytes_in_dict(self, d: Dict) -> Dict:
        """Helper to decode bytes in dictionary values"""
        decoded = {}
        for k, v in d.items():
            if isinstance(v, dict) and v.get('type') == 'bytes':
                decoded[k] = base64.b64decode(v['data'])
            elif isinstance(v, dict):
                decoded[k] = self._decode_bytes_in_dict(v)
            else:
                decoded[k] = v
        return decoded


    @classmethod
    async def deserialize(cls, serialized_data: str) -> 'Message':
        """
        Create Message instance from serialized string.
        
        :param serialized_data: Serialized message data
        :type serialized_data: str
        :return: New Message instance
        :rtype: Message
        """
        # Use json for deserialization
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, json.loads, serialized_data)
        
        # Convert strings back to proper types
        data['sender'] = Sender(data['sender'])
        data['type'] = MessageType(data['type'])
        data['date'] = datetime.fromisoformat(data['date'])
        data['metadata_ids'] = set(data['metadata_ids'])
        data['file_ids'] = set(data['file_ids'])

        # Decode any bytes in annotations
        if data.get('annotations'):
            data['annotations'] = cls._decode_bytes_in_dict(data['annotations'])
        
        return cls(**data)


    # For langchain compatibility
    def to_react_format(self) -> str:
        """Convert message to ReAct format"""
        role = "Human" if self.sender == Sender.USER else "AI"
        return f"{role}: {self.content}"
    
    @staticmethod
    def format_chat_history(messages: List["Message"]) -> str:
        """Format messages for ReAct agent"""
        return "\n".join(msg.to_react_format() for msg in messages)