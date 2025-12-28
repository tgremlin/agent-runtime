"""Agent and AgentVersion models."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Agent(BaseModel):
    """A logical AI capability definition."""

    id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "from_attributes": True,
    }


class AgentVersion(BaseModel):
    """Immutable configuration of an agent."""

    id: UUID = Field(default_factory=uuid4)
    agent_id: UUID
    version: str = Field(..., min_length=1, max_length=50)
    config: dict[str, Any] = Field(default_factory=dict)
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "from_attributes": True,
    }
