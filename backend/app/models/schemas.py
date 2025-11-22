from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class PriorityEnum(str, Enum):
    HIGH = "HIGH"
    LOW = "LOW"

class TaskInput(BaseModel):
    id: int
    arrival_time: float
    processing_time: float
    priority: PriorityEnum
    deadline: float

class SimulationRequest(BaseModel):
    algorithm: str
    num_machines: int
    tasks: List[TaskInput]
    alpha: Optional[float] = 0.7  # For DPE

class LogEntry(BaseModel):
    time: float
    event: str
    task_id: Optional[int] = None
    machine_id: Optional[int] = None
    message: str
    completion_time: Optional[float] = None

class TaskResult(BaseModel):
    id: int
    priority: str
    arrival_time: float
    start_time: Optional[float]
    completion_time: Optional[float]
    deadline: float
    meets_deadline: bool

class PriorityStats(BaseModel):
    total: int
    met_deadline: int

class SimulationResult(BaseModel):
    makespan: float
    total_tasks: int
    high_priority_stats: PriorityStats
    low_priority_stats: PriorityStats
    tasks: List[TaskResult]
    logs: List[LogEntry]

class AlgorithmInfo(BaseModel):
    id: str
    name: str
    description: str

class ScenarioInfo(BaseModel):
    id: str
    name: str
    description: str
    num_machines: int
    tasks: List[TaskInput]
