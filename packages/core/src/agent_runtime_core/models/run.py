"""Run model - a single execution of an agent version."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    """Status of an agent run."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Run(BaseModel):
    """A single execution of an agent version with defined input."""

    id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    agent_id: UUID
    agent_version_id: UUID
    status: RunStatus = Field(default=RunStatus.PENDING)
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] | None = None
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Temporal workflow reference
    workflow_id: str | None = None
    workflow_run_id: str | None = None

    model_config = {
        "from_attributes": True,
    }


class RunEvent(BaseModel):
    """An event emitted during a run."""

    id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    event_type: str
    data: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "from_attributes": True,
    }
