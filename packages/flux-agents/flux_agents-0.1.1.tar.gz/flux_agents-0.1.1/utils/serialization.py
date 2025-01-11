"""
Serialization utilities for handling various data types and formats.

This module provides functionality for serializing and deserializing different data types
including polars DataFrames, numpy arrays, Plotly figures, PIL Images, and more.
"""

from enum import Enum, auto
from functools import lru_cache
from typing import Any, Dict, Set, Type, List, Tuple
import base64
import json
import msgpack
import pickle
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
import pyarrow as pa
import plotly.graph_objects as go
import zstandard as zstd 
from PIL import Image
import io
import os
import threading
import polars as pl

# TODO - Centralize, remove elsewhere
logger = logging.getLogger(__name__)

# Thread-safe compressor instances
_compression_lock = threading.Lock()  # Lock for thread-safe compressor access
_compressor = None  # Global ZStandard compressor instance
_decompressor = None  # Global ZStandard decompressor instance


def get_compressor():
    """
    Get or create a thread-safe ZStandard compressor instance.

    :return: A compressor instance with compression level 3
    :rtype: zstd.ZstdCompressor
    """
    global _compressor
    with _compression_lock:
        if _compressor is None:
            _compressor = zstd.ZstdCompressor(level=3)
        return _compressor


def get_decompressor():
    """
    Get or create a thread-safe ZStandard decompressor instance.

    :return: A decompressor instance
    :rtype: zstd.ZstdDecompressor
    """
    global _decompressor
    with _compression_lock:
        if _decompressor is None:
            _decompressor = zstd.ZstdDecompressor()
        return _decompressor


class SerializationType(Enum):
    """
    Enumeration of supported serialization types.
    
    :cvar ARROW: Apache Arrow serialization for polars DataFrames
    :cvar PLOTLY: Plotly figure serialization
    :cvar MSGPACK: MessagePack serialization for basic Python types
    :cvar PICKLE: Python pickle serialization (fallback)
    :cvar NUMPY: NumPy array serialization
    :cvar IMAGE: PIL Image serialization
    :cvar PARQUET: Apache Parquet serialization
    :cvar JSON: JSON serialization
    :cvar NONE: No serialization needed
    """
    ARROW = auto()
    PLOTLY = auto()
    MSGPACK = auto()
    PICKLE = auto()
    NUMPY = auto()
    IMAGE = auto()
    PARQUET = auto()
    JSON = auto()
    NONE = auto()


JSON_COMPATIBLE_TYPES = frozenset([type(None), bool, int, float, str])
"""
Set of types that are JSON-compatible and don't need serialization.

:ivar JSON_COMPATIBLE_TYPES: Set of Python types that can be directly serialized to JSON
:type JSON_COMPATIBLE_TYPES: frozenset
"""

TYPE_SERIALIZATION_MAP = {
    pl.DataFrame: SerializationType.ARROW,
    go.Figure: SerializationType.PLOTLY,
    dict: SerializationType.MSGPACK,
    list: SerializationType.MSGPACK,
    tuple: SerializationType.MSGPACK,
    np.ndarray: SerializationType.NUMPY,
    Image.Image: SerializationType.IMAGE,
    bytes: SerializationType.MSGPACK,
    set: SerializationType.JSON,
    frozenset: SerializationType.JSON
}
"""
Mapping of Python types to their corresponding serialization methods.

:ivar TYPE_SERIALIZATION_MAP: Dictionary mapping Python types to SerializationType enums
:type TYPE_SERIALIZATION_MAP: Dict[Type, SerializationType]
"""


# Thread-local storage for executors
class ExecutorManager:
    """
    Singleton manager for thread and process pool executors.
    
    This class manages thread-local and process-wide executor pools for
    parallel serialization operations.
    
    :cvar _instance: Singleton instance
    :type _instance: ExecutorManager
    :cvar _lock: Lock for thread-safe singleton creation
    :type _lock: threading.Lock
    :ivar _thread_executor: Thread pool executor instance
    :type _thread_executor: ThreadPoolExecutor
    :ivar _process_executor: Process pool executor instance
    :type _process_executor: ProcessPoolExecutor
    :ivar _thread_local: Thread-local storage
    :type _thread_local: threading.local
    """
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        """
        Initialize a new ExecutorManager instance.
        
        :ivar _thread_executor: Thread pool executor instance
        :type _thread_executor: ThreadPoolExecutor
        :ivar _process_executor: Process pool executor instance
        :type _process_executor: ProcessPoolExecutor
        :ivar _thread_local: Thread-local storage
        :type _thread_local: threading.local
        """
        self._thread_executor = None
        self._process_executor = None
        self._thread_local = threading.local()
    
    @classmethod
    def get_instance(cls):
        """
        Get or create the singleton instance of ExecutorManager.
        
        :return: The singleton ExecutorManager instance
        :rtype: ExecutorManager
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def get_thread_pool(self):
        """
        Get or create a thread pool executor for the current thread.
        
        :return: Thread pool executor instance
        :rtype: ThreadPoolExecutor
        """
        if not hasattr(self._thread_local, 'thread_pool'):
            self._thread_local.thread_pool = ThreadPoolExecutor(
                max_workers=min(32, (os.cpu_count() or 1) + 4),
                thread_name_prefix='serializer'
            )
        return self._thread_local.thread_pool
    
    def get_process_pool(self):
        """
        Get or create a process pool executor.
        
        :return: Process pool executor instance
        :rtype: ProcessPoolExecutor
        """
        if self._process_executor is None:
            with self._lock:
                if self._process_executor is None:
                    self._process_executor = ProcessPoolExecutor(
                        max_workers=max(1, os.cpu_count() - 1)
                    )
        return self._process_executor
    
    def cleanup(self):
        """
        Clean up thread and process pool executors.
        
        Shuts down all executor pools and removes thread-local storage.
        """
        if hasattr(self._thread_local, 'thread_pool'):
            self._thread_local.thread_pool.shutdown(wait=False)
            delattr(self._thread_local, 'thread_pool')
        
        if self._process_executor:
            with self._lock:
                if self._process_executor:
                    self._process_executor.shutdown(wait=False)
                    self._process_executor = None


@lru_cache(maxsize = 128)
def _get_type_category(cls: Type) -> SerializationType:
    """
    Get the serialization type for a given class.

    :param cls: The class type to get serialization type for
    :type cls: Type
    :return: The appropriate serialization type enum value
    :rtype: SerializationType
    """
    return TYPE_SERIALIZATION_MAP.get(cls, SerializationType.PICKLE)


def _needs_serialization(item: Any, _seen: Set = None) -> bool:
    """
    Check if an item needs serialization.
    
    :param item: Item to check
    :type item: Any
    :param _seen: Set of already seen object IDs for cycle detection
    :type _seen: Set, optional
    :return: True if the item needs serialization, False otherwise
    :rtype: bool
    """
    if _seen is None:
        _seen = set()
        
    item_id = id(item)
    if item_id in _seen:
        return True
    _seen.add(item_id)

    item_type = type(item)
    if item_type in JSON_COMPATIBLE_TYPES:
        return False
        
    if isinstance(item, (list, tuple)):
        return any(_needs_serialization(x, _seen) for x in item)
        
    if isinstance(item, dict):
        return any(_needs_serialization(v, _seen) for v in item.values())
        
    return True


def _get_serialization_type(item: Any) -> SerializationType:
    """
    Determine the serialization type for a given item.

    :param item: The item to get serialization type for
    :type item: Any
    :return: The appropriate serialization type enum value
    :rtype: SerializationType
    """
    return _get_type_category(type(item))


def _serialize_item(item: Any) -> Any:
    """
    Serialize a single item based on its type.

    :param item: The item to serialize
    :type item: Any
    :return: The serialized item or None if serialization fails
    :rtype: Any
    """
    if not _needs_serialization(item):
        return item
        
    ser_type = _get_serialization_type(item)
    manager = ExecutorManager.get_instance()
    
    try:
        match ser_type:
            case SerializationType.ARROW:
                if len(item) < 10000:
                    def serialize_arrow():
                        return item.to_arrow().serialize().to_pybytes()
                    
                    arrow_bytes = serialize_arrow()
                else:
                    def serialize_parquet():
                        buffer = io.BytesIO()
                        item.write_parquet(buffer, compression="zstd")
                        return buffer.getvalue()
                    
                    arrow_bytes = serialize_parquet()
                
                return {
                    'type': 'arrow',
                    'data': base64.b64encode(arrow_bytes).decode('ascii')
                }
                
            case SerializationType.NUMPY:
                def serialize_numpy():
                    buffer = io.BytesIO()
                    np.save(buffer, item, allow_pickle=False)
                    return buffer.getvalue()
                
                numpy_bytes = serialize_numpy()
                
                return {
                    'type': 'numpy',
                    'data': base64.b64encode(numpy_bytes).decode('ascii')
                }
                
            case SerializationType.IMAGE:
                def serialize_image():
                    buffer = io.BytesIO()
                    item.save(buffer, format='PNG', optimize=True)
                    return buffer.getvalue()
                
                image_bytes = serialize_image()
                
                return {
                    'type': 'image',
                    'data': base64.b64encode(image_bytes).decode('ascii')
                }
                
            case SerializationType.PLOTLY:
                def serialize_plotly():
                    fig_dict = item.to_dict()
                    return get_compressor().compress(json.dumps(fig_dict))
                
                plotly_bytes = serialize_plotly()
                
                return {
                    'type': 'plotly',
                    'data': base64.b64encode(plotly_bytes).decode('ascii')
                }
                
            case SerializationType.MSGPACK:
                def serialize_msgpack():
                    packed = msgpack.packb(item, use_bin_type=True)
                    return get_compressor().compress(packed)
                
                msgpack_bytes = serialize_msgpack()
                
                return {
                    'type': 'msgpack',
                    'data': base64.b64encode(msgpack_bytes).decode('ascii')
                }
                
            case SerializationType.PICKLE:
                def serialize_pickle():
                    pickled = pickle.dumps(item, protocol=5)
                    return get_compressor().compress(pickled)
                
                pickle_bytes = serialize_pickle()
                
                return {
                    'type': 'pickle',
                    'data': base64.b64encode(pickle_bytes).decode('ascii')
                }
            
    except Exception as e:
        logger.warning(f"Failed to serialize item of type {type(item)}: {str(e)}")
        return None


def serialize_metadata(
    response_metadata: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Serialize metadata dictionary containing various data types.
    
    :param response_metadata: Dictionary containing metadata to serialize
    :type response_metadata: Dict[str, Any]
    :param end_state: Whether this is the final state
    :type end_state: bool, optional
    :return: Dictionary containing serialized data
    :rtype: Dict[str, Any]
    """
    serialized_data = {}
    
    try:
        items_to_process = [
            (key, value) for key, value in response_metadata.items()
            if _needs_serialization(value)
        ]
        
        if items_to_process:
            results = [
                _serialize_item(value) for _, value in items_to_process
            ]
            
            for (key, _), result in zip(items_to_process, results):
                if result is not None:
                    serialized_data[key] = result
                    
    except Exception as e:
        logger.error(f"Failed to serialize items: {str(e)}")
        
    return serialized_data


def _unserialize_item(item: Any) -> Any:
    """
    Unserialize a single item based on its type.

    :param item: The serialized item to unserialize
    :type item: Any
    :return: The unserialized item or None if unserialization fails
    :rtype: Any
    """
    if not isinstance(item, dict) or 'type' not in item or 'data' not in item:
        return item
            
    try:
        binary_data = base64.b64decode(item['data'])
        manager = ExecutorManager.get_instance()
        
        match item['type']:
            case 'arrow':
                def unserialize_arrow():
                    if len(binary_data) < 1_000_000:
                        return pl.from_arrow(pa.ipc.read_message(binary_data).body)
                    else:
                        return pl.read_parquet(io.BytesIO(binary_data))
                
                return unserialize_arrow()
                
            case 'plotly':
                def unserialize_plotly():
                    return go.Figure(
                        json.loads(
                            get_decompressor().decompress(binary_data)
                        )
                    )
                
                return unserialize_plotly()
                
            case 'msgpack':
                def unserialize_msgpack():
                    return msgpack.unpackb(
                        get_decompressor().decompress(binary_data),
                        raw=False
                    )
                
                return unserialize_msgpack()
                
            case 'pickle':
                def unserialize_pickle():
                    return pickle.loads(
                        get_decompressor().decompress(binary_data)
                    )
                
                return unserialize_pickle()
                
            case 'numpy':
                def unserialize_numpy():
                    return np.load(io.BytesIO(binary_data), allow_pickle=False)
                
                return unserialize_numpy()
                
            case 'image':
                def unserialize_image():
                    return Image.open(io.BytesIO(binary_data))
                
                return unserialize_image()
            
    except Exception as e:
        logger.error(f"Failed to unserialize item: {str(e)}")
        return None
    
    return item


def unserialize_metadata(response_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unserialize metadata dictionary containing various data types.
    
    :param response_metadata: Dictionary containing serialized metadata
    :type response_metadata: Dict[str, Any]
    :return: Dictionary containing unserialized data
    :rtype: Dict[str, Any]
    """
    try:
        items_to_process = [
            (key, value) for key, value in response_metadata.items()
            if isinstance(value, dict) and 'type' in value and 'data' in value
        ]
        
        if items_to_process:
            results = [
                _unserialize_item(value) for _, value in items_to_process
            ]
            
            return {
                key: result if result is not None else value
                for (key, value), result in zip(items_to_process, results)
            }
            
        return response_metadata
                    
    except Exception as e:
        logger.error(f"Failed to unserialize items: {str(e)}")
        return {}


def _deserialize_item(serialized_data: Dict[str, Any]) -> Any:
    """
    Deserialize a single item based on its type tag.
    
    :param serialized_data: Dictionary containing type and serialized data
    :type serialized_data: Dict[str, Any]
    :return: Deserialized object
    :rtype: Any
    :raises ValueError: If deserialization fails
    """
    if not isinstance(serialized_data, dict) or 'type' not in serialized_data or 'data' not in serialized_data:
        return serialized_data
            
    try:
        binary_data = base64.b64decode(serialized_data['data'])
        
        match serialized_data['type']:
            case 'arrow':
                def deserialize_arrow():
                    if len(binary_data) < 1_000_000:
                        # For smaller datasets, use Arrow IPC
                        table = pa.ipc.read_message(binary_data).body
                        return pl.from_arrow(table)
                    else:
                        # For larger datasets, use Parquet
                        buffer = io.BytesIO(binary_data)
                        return pl.read_parquet(buffer)
                
                return deserialize_arrow()
                
            case 'plotly':
                def deserialize_plotly():
                    decompressed = get_decompressor().decompress(binary_data)
                    fig_dict = json.loads(decompressed)
                    return go.Figure(fig_dict)
                
                return deserialize_plotly()
                
            case 'numpy':
                def deserialize_numpy():
                    buffer = io.BytesIO(binary_data)
                    return np.load(buffer, allow_pickle=False)
                
                return deserialize_numpy()
                
            case 'image':
                def deserialize_image():
                    buffer = io.BytesIO(binary_data)
                    return Image.open(buffer)
                
                return deserialize_image()
                
            case 'msgpack':
                def deserialize_msgpack():
                    decompressed = get_decompressor().decompress(binary_data)
                    return msgpack.unpackb(decompressed, raw=False)
                
                return deserialize_msgpack()
                
            case 'pickle':
                def deserialize_pickle():
                    decompressed = get_decompressor().decompress(binary_data)
                    return pickle.loads(decompressed)
                
                return deserialize_pickle()
                
            case _:
                raise ValueError(f"Unknown serialization type: {serialized_data['type']}")
            
    except Exception as e:
        raise ValueError(f"Failed to deserialize {serialized_data['type']} data: {str(e)}")


def deserialize_metadata(serialized_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deserialize metadata dictionary containing various data types.
    
    :param serialized_data: Dictionary containing serialized metadata
    :type serialized_data: Dict[str, Any]
    :return: Dictionary containing deserialized data
    :rtype: Dict[str, Any]
    """
    try:
        items_to_process = [
            (key, value) for key, value in serialized_data.items()
            if isinstance(value, dict) and 'type' in value and 'data' in value
        ]
        
        if items_to_process:
            results = [
                _deserialize_item(value) for _, value in items_to_process
            ]
            
            return {
                key: result if result is not None else value
                for (key, value), result in zip(items_to_process, results)
            }
            
        return serialized_data
                    
    except Exception as e:
        logger.error(f"Failed to deserialize items: {str(e)}")
        return {}


def serialize_and_compress(data: Any) -> bytes:
    """
    Serialize and compress data in a format-aware way.
    
    :param data: Data to serialize and compress
    :type data: Any
    :return: Compressed serialized data
    :rtype: bytes
    """

    if isinstance(data, pl.DataFrame):
        return data.to_arrow().serialize().to_pybytes()
    
    else:
        return get_compressor().compress(
            msgpack.packb(data, use_bin_type=True)
        )


def decompress_and_deserialize(
    data: bytes, 
    expected_type: Type = None
) -> Any:
    """
    Decompress and deserialize data with type checking.
    
    :param data: Compressed serialized data
    :type data: bytes
    :param expected_type: Expected type of deserialized data
    :type expected_type: Type, optional
    :return: Deserialized data
    :rtype: Any
    """
    
    if expected_type == pl.DataFrame:
        return pl.from_arrow(pa.ipc.read_message(data).body)
    
    # Default msgpack deserialization
    decompressed = get_decompressor().decompress(data)
    result = msgpack.unpackb(decompressed, raw=False)
    
    if expected_type and not isinstance(result, expected_type):
        raise TypeError(f"Expected {expected_type}, got {type(result)}")
        
    return result
