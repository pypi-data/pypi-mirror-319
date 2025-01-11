"""
Configuration models for the flux_agents package.
"""
from enum import Enum


class TruncationType(str, Enum):
    """
    Types of text truncation strategies.
    
    :cvar TOKEN_LIMIT: Simple truncation at token limit
    :cvar TRIM_MAX: Trim to maximum allowed tokens
    :cvar PRESERVE_CONTEXT: Keep context from start and end
    """
    TOKEN_LIMIT = 'token_limit'
    TRIM_MAX = 'trim_max'
    PRESERVE_CONTEXT = 'preserve_context' 