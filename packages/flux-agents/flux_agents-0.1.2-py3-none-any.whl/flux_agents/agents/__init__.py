"""
Agent system initialization.

Provides easy access to core agent components and utilities.
"""

# Base Agent Classes
from flux_agents.agents.agent.models import Agent
from flux_agents.agents.state.models import AgentState

# Agent Implementations
from flux_agents.agents.agent.react.models import ReActAgent
from flux_agents.agents.agent.planning.models import PlanningAgent
from flux_agents.agents.agent.hierarchical.models import HierarchicalAgent

# Worker Implementations
from flux_agents.agents.agent.hierarchical.react_worker import ReActWorker
from flux_agents.agents.agent.hierarchical.planning_worker import PlanningWorker

# Core Enums
from flux_agents.agents.agent.enums import (
    AgentType,
    WorkerDivision,
    WorkerGeneration
)

# Configuration Models
from flux_agents.agents.config.models import (
    AgentConfig,
    ContextConfig,
    Logging
)

# Storage Models
from flux_agents.agents.storage.message import Message, MessageType, Sender
from flux_agents.agents.storage.metadata import Metadata
from flux_agents.agents.storage.file import File, FileType
from flux_agents.agents.storage.context import Context, ContextType

# Vector Store Components
from flux_agents.agents.vectorstore.default.store import HNSWStore
from flux_agents.agents.config.models import (
    RetrievalType,
    TruncationType,
    SliceType
)

__all__ = [
    # Base Classes
    'Agent',
    'AgentState',
    
    # Agent Implementations
    'ReActAgent',
    'PlanningAgent', 
    'HierarchicalAgent',
    
    # Worker Implementations
    'ReActWorker',
    'PlanningWorker',
    
    # Core Enums
    'AgentType',
    'WorkerDivision',
    'WorkerGeneration',
    
    # Configs
    'AgentConfig',
    'ContextConfig',
    'Logging',
    
    # Storage Models
    'Message',
    'MessageType',
    'Sender',
    'Metadata',
    'File',
    'FileType',
    'Context',
    'ContextType',
    
    # Vector Store Components
    'HNSWStore',
    'RetrievalType',
    'TruncationType', 
    'SliceType'
]