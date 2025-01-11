import os
from pydantic import BaseModel, Field, PrivateAttr
from datetime import datetime
from typing import Any, List, Optional, Union
import sys
import numpy as np
import pandas as pl
import numpy as np
import torch
import base64
import msgpack
import io
import pyarrow as pa

from utils.shared.tokenizer import slice_text, SliceType

from utils.summarization import MetadataType
from utils.serialization import get_compressor, get_decompressor, SerializationType
from utils.shared.tokenizer import encode
from agents.storage.models import IDFactory



class Metadata(BaseModel):
    """
    Model for metadata attachments in messages.
    
    :ivar id: Unique identifier
    :type id: str
    :ivar date: Creation timestamp
    :type date: datetime
    :ivar description: Optional description
    :type description: str
    :ivar agent_name: Name of agent that created metadata
    :type agent_name: str
    :ivar name: Optional metadata name
    :type name: str
    :ivar type: Metadata type
    :type type: MetadataType
    """
    id: int = Field(default_factory=lambda: IDFactory.next_id(Metadata))
    date: datetime = Field(default_factory = datetime.now)
    description: str = Field(default = None)
    agent_name: str = Field(default = "base")
    name: str = Field(default = None)
    type: MetadataType = Field(default = MetadataType.UNKNOWN)
    
    # For vector-based retrieval
    score: int = Field(default = 0, description = "Score of the file")

    # Store data reference directly
    stored_data: Any = Field(default=None, alias='data')
    content_cache: Optional[str] = Field(default=None, exclude=True)

    _tokens: Optional[List[int]] = PrivateAttr(default=None)

    class Config:
        arbitrary_types_allowed = True
        copy_on_model_validation = False

    def __init__(self, **data):
        super().__init__(**data)
        # Store reference to data without copying
        if 'stored_data' in data:
            self.stored_data = data['stored_data']
        elif 'data' in data:
            self.stored_data = data['data']
       
        # Initialize type and content if we have data
        if self.stored_data is not None:
            handler, inferred_type = MetadataType.get_handler(self.stored_data, self.name)
            self.type = inferred_type
            if not self.name:
                self.name = f"{self.type.value}_{self.id}"
            
            content = handler(self.stored_data, self.name)
            
            if self.description:
                content = f"{content} (Description: {self.description})"
            self.content_cache = content


    @property
    def data(self) -> Any:
        """Get metadata content reference"""
        return self.stored_data


    @data.setter 
    def data(self, value: Any) -> None:
        """Set metadata content reference and regenerate content cache if changed"""
        needs_update = False
        
        # Special handling for different types
        match value:
            case pl.DataFrame():
                needs_update = id(self.stored_data) != id(value)
            case np.ndarray():
                needs_update = id(self.stored_data) != id(value)
            case torch.Tensor():
                needs_update = id(self.stored_data) != id(value)
            case _:
                needs_update = self.stored_data is not value

        if needs_update:
            self.stored_data = value
            self._tokens = None  # Clear token cache
            
            # Regenerate content cache if we have data
            if value is not None:
                handler, inferred_type = MetadataType.get_handler(value)
                
                if self.type == MetadataType.UNKNOWN:
                    self.type = inferred_type
                   
                content = handler(value, name = self.name)
        
                if self.description:
                    content = f"{content} (Description: {self.description})"
                self.content_cache = content
            else:
                self.content_cache = None


    @property
    def content(self) -> str:
        """
        Get summarized string representation of metadata content.
        Uses summary handler to generate concise description.
        
        :return: Summary string of metadata content
        :rtype: str
        """
        # Content was already generated during init or last data update
        if self.content_cache is not None:
            return self.content_cache
            
        # If we get here, it means data was set to None
        return "No data!"


    def tokens(self) -> List[int]:
        """Get tokenized content with caching"""
        if self._tokens is None:
            self._tokens = encode(str(self.stored_data))
        return self._tokens
    
    
    def __len__(self) -> int:
        """
        Get token count of metadata summary content.
        
        :return: Number of tokens
        :rtype: int
        """
        return len(self.tokens())


    def clear_caches(self) -> None:
        """Clear all caches."""
        self.tokens.cache_clear()
        self.content_cache = None

    
    def __len__(self) -> int:
        """
        Get token count of metadata summary content.
        
        :return: Number of tokens
        :rtype: int
        """
        return len(self.tokens())


    def truncate(self, 
        max_tokens: int,
        slice_type: SliceType = SliceType.END
    ) -> str:

        truncated = slice_text(
            text = self.content,
            max_tokens = max_tokens,
            slice_type = slice_type
        )
        return truncated


    def serialize(self) -> str:
        """
        Serialize metadata to a string representation.
        
        :return: Serialized metadata string
        :rtype: str
        """
        # Create base data dictionary with basic types
        data = {
            'id': self.id,
            'date': self.date.isoformat(),
            'description': self.description,
            'agent_name': self.agent_name,
            'name': self.name,
            'type': self.type.value,
            'score': self.score
        }

        # Handle the data field separately since it may contain non-JSON serializable types
        if self.data is not None:
            match self.data:
                case pl.DataFrame():
                    arrow_table = self.data.to_arrow()
                    sink = pa.BufferOutputStream()
                    with pa.ipc.new_stream(
                        sink,
                        arrow_table.schema,
                        options=pa.ipc.IpcWriteOptions(compression='zstd')
                    ) as writer:
                        writer.write_table(arrow_table)
                    data['data'] = {
                        'type': 'polars_ipc',
                        'schema': arrow_table.schema.serialize().to_pybytes(),
                        'data': sink.getvalue().to_pybytes()
                    }
                    # Use msgpack for the wrapper since it handles bytes efficiently
                    packed = msgpack.packb(data, use_bin_type=True)
                    compressed = get_compressor().compress(packed)
                    return base64.b64encode(compressed).decode('ascii')
            
                case np.ndarray():
                    # Use numpy's efficient binary format
                    buffer = io.BytesIO()
                    np.save(buffer, self.data, allow_pickle=False)
                    data['data'] = {
                        'type': 'numpy',
                        'data': buffer.getvalue()
                    }
                    # Use msgpack for binary data
                    packed = msgpack.packb(data, use_bin_type=True)
                    compressed = get_compressor().compress(packed)
                    return base64.b64encode(compressed).decode('ascii')
                
                case torch.Tensor():
                    # Convert to numpy and use its efficient format
                    tensor_data = self.data.detach().cpu().numpy()
                    buffer = io.BytesIO()
                    np.save(buffer, tensor_data, allow_pickle=False)
                    data['data'] = {
                        'type': 'tensor',
                        'data': buffer.getvalue()
                    }
                    packed = msgpack.packb(data, use_bin_type=True)
                    compressed = get_compressor().compress(packed)
                    return base64.b64encode(compressed).decode('ascii')
         
            # For other types, use msgpack directly
            packed = msgpack.packb(data, use_bin_type=True)
            compressed = get_compressor().compress(packed)
            return base64.b64encode(compressed).decode('ascii')

        # If no data field, use msgpack for consistency
        packed = msgpack.packb(data, use_bin_type=True)
        compressed = get_compressor().compress(packed)
        
        return base64.b64encode(compressed).decode('ascii')


    @classmethod
    def deserialize(cls, serialized_data: str) -> 'Metadata':
        """
        Create Metadata instance from serialized string.
        
        :param serialized_data: Serialized metadata data
        :type serialized_data: str
        :return: New Metadata instance
        :rtype: Metadata
        """
        # Decompress and unpack base data
        compressed = base64.b64decode(serialized_data)
        decompressed = get_decompressor().decompress(compressed)
        data = msgpack.unpackb(decompressed, raw=False)
        
        # Handle special data types
        match data.get('data'):
            case dict() if 'type' in data['data']:
                match data['data']['type']:
                    case 'polars_ipc':
                        # Reconstruct DataFrame from Arrow IPC stream
                        schema = pa.ipc.read_schema(pa.py_buffer(data['data']['schema']))
                        reader = pa.ipc.open_stream(
                            pa.py_buffer(data['data']['data']),
                            schema=schema
                        )
                        data['data'] = pl.from_arrow(reader.read_all())
                        
                    case 'numpy':
                        buffer = io.BytesIO(data['data']['data'])
                        data['data'] = np.load(buffer, allow_pickle=False)
                        
                    case 'tensor':
                        buffer = io.BytesIO(data['data']['data'])
                        arr = np.load(buffer, allow_pickle=False)
                        data['data'] = torch.from_numpy(arr)
        
        # Convert basic types
        data['type'] = MetadataType(data['type'])
        data['date'] = datetime.fromisoformat(data['date'])
        
        return cls(**data)

    
    def __aenter__(self) -> 'Metadata':
        """Async context manager entry."""
        return self


    def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit with cleanup."""
        self.clear_caches()
        if hasattr(self, 'raw_data'):
            del self.raw_data
            

    @property
    def size(self) -> int:
        """
        Get approximate memory size of metadata.
        
        :return: Size in bytes
        :rtype: int
        """
        return sys.getsizeof(self.data)

    @property
    def type_name(self) -> str:
        """
        Get human-readable type name.
        
        :return: Type name string
        :rtype: str
        """
        return self.type.value.title()
            
            
    def __bool__(self) -> bool:
        """
        Verifies existance of object
        """
        return bool(self.data)

    def __hash__(self) -> int:
        """Make Metadata hashable for caching"""
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        """Define equality for hashing"""
        if not isinstance(other, Metadata):
            return False
        return self.id == other.id