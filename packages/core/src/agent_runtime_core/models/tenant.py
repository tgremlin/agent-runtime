"""Tenant model - isolated organizational boundary."""

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Tenant(BaseModel):
    """A tenant represents an isolated organizational boundary."""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=63, pattern=r"^[a-z0-9-]+$")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "from_attributes": True,
    }
