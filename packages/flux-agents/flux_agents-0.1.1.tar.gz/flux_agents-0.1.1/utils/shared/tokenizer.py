"""
Shared tokenizer instance for text processing.

This module provides a shared tokenizer instance using the cl100k_base encoding
from tiktoken, which is compatible with most modern language models. It also
provides async-safe encoding and decoding functions to prevent event loop blocking.
"""

import asyncio
from typing import List, Union
from enum import Enum

import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")


def encode(text: str) -> List[int]:
    """
    Encode text into tokens.
    
    :param text: The text to encode into tokens
    :type text: str
    :return: List of integer tokens representing the encoded text
    :rtype: List[int]
    """
    return tokenizer.encode(text)


def decode(tokens: Union[List[int], bytes]) -> str:
    """
    Decode tokens back into text.
    
    :param tokens: List of integer tokens or bytes to decode
    :type tokens: Union[List[int], bytes]
    :return: Decoded text string
    :rtype: str
    """
    return tokenizer.decode(tokens)


def batch_token_lengths(texts: List[str]) -> List[int]:
    """
    Get token counts for multiple texts.
    
    :param texts: List of texts to get token counts for
    :type texts: List[str]
    :return: List of token counts corresponding to each text
    :rtype: List[int]
    """
    return [len(encode(text)) for text in texts]


class SliceType(str, Enum):
    """
    Types of slicing to apply to item content
    
    :cvar START: Truncate the start of the message
    :cvar END: Truncate the end of the message
    :cvar MIDDLE: Truncate the middle of the message
    """
    START = "start"
    END = "end"
    MIDDLE = "middle"
    

def slice_text(
    text: str, 
    slice_type: SliceType,
    max_tokens: int
    
) -> str:
    """
    Slice text to a maximum number of tokens.
    
    :param text: Text to slice
    :type text: str
    :param slice_type: Type of slice to apply
    :type slice_type: SliceType 
    :param max_tokens: Maximum number of tokens
    :type max_tokens: int
    :return: Truncated text
    :rtype: str
    """
    
    tokens = encode(text)
    
    if len(tokens) <= max_tokens:
        return text
    
    max_tokens -= 3 # For slice explanation
    if slice_type == SliceType.START:
        truncated_tokens = tokens[max_tokens:]
        truncated_text = decode(truncated_tokens) 
        truncated_text = "[...TRUNCATED START] " + truncated_text
    
    elif slice_type == SliceType.END:
        truncated_tokens = tokens[:max_tokens]
        truncated_text = decode(truncated_tokens) + " [TRUNCATED END...]"
    
    elif slice_type == SliceType.MIDDLE:
        start_tokens = tokens[:max_tokens // 2]
        end_tokens = tokens[-max_tokens // 2:]
        start_text = decode(start_tokens)
        end_text = decode(end_tokens)
        truncated_text = start_text + " [...TRUNCATED MIDDLE...] " + end_text
    
    else:
        raise ValueError(f"Invalid slice type: {slice_type}")
        
    return truncated_text