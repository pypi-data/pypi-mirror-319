from enum import Enum


class AgentType(Enum):
    BASE = "base"
    HIERARCHICAL = "hierarchical"
    PLANNING = "planning"
    REACT = "react"
    WORKER = "worker"
    
    
class WorkerType(str, Enum):
    REACT = "react"
    PLANNING = "planning"
    MIXED = "mixed"

class WorkerDivision(str, Enum):
    VARY_PERSPECTIVES = "vary_perspectives"
    DIVISION_OF_LABOR = "division_of_labor"    
    REPLICA = "replica"
    
class WorkerGeneration(str, Enum):
    DEFAULT = "default"
    AUTO = "auto"
    