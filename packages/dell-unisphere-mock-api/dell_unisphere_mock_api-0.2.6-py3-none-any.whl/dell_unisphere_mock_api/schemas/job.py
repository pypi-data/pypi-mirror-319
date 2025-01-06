from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class JobState(str, Enum):
    """Possible states of a job."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class JobTask(BaseModel):
    """Represents a single task within a job."""

    name: str
    object: str
    action: str
    parametersIn: Dict
    description: Optional[str] = None
    descriptionArg: Optional[str] = None


class JobCreate(BaseModel):
    """Schema for creating a new job."""

    description: str
    tasks: List[JobTask]
    timeout: Optional[int] = None


class Job(BaseModel):
    """Schema for a job instance."""

    id: str
    state: JobState
    description: str
    tasks: List[JobTask]
    progressPct: Optional[float] = None
    errorMessage: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "job_123",
                "state": "COMPLETED",
                "description": "Create pool and LUN",
                "tasks": [
                    {
                        "name": "CreatePool",
                        "object": "pool",
                        "action": "create",
                        "parametersIn": {"name": "test_pool", "type": 1, "sizeTotal": 1000000000},
                    }
                ],
                "progressPct": 100.0,
            }
        }
    )
