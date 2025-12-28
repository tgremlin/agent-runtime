"""Run management endpoints."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agent_runtime_core.models import Run, RunStatus

router = APIRouter()


class CreateRunRequest(BaseModel):
    """Request body for creating a new run."""

    agent_version_id: UUID
    input: dict[str, Any] = {}


@router.get("/")
async def list_runs(
    tenant_id: UUID | None = None,
    agent_id: UUID | None = None,
    status: RunStatus | None = None,
) -> list[Run]:
    """List runs with optional filters."""
    # TODO: Implement database query
    return []


@router.post("/", status_code=202)
async def create_run(request: CreateRunRequest, tenant_id: UUID) -> Run:
    """
    Create and start a new agent run.

    Returns 202 Accepted as the run is started asynchronously.
    """
    # TODO: Implement:
    # 1. Validate tenant, agent, version
    # 2. Create Run record in database
    # 3. Start Temporal workflow
    # 4. Return run with workflow IDs
    run = Run(
        tenant_id=tenant_id,
        agent_id=UUID("00000000-0000-0000-0000-000000000000"),  # Placeholder
        agent_version_id=request.agent_version_id,
        input=request.input,
        status=RunStatus.PENDING,
    )
    return run


@router.get("/{run_id}")
async def get_run(run_id: UUID) -> Run:
    """Get a run by ID."""
    # TODO: Implement database query
    raise HTTPException(status_code=404, detail="Run not found")


@router.post("/{run_id}/cancel", status_code=202)
async def cancel_run(run_id: UUID) -> dict:
    """Cancel a running execution."""
    # TODO: Implement Temporal workflow cancellation
    return {"status": "cancellation_requested", "run_id": str(run_id)}


@router.post("/{run_id}/signal")
async def signal_run(run_id: UUID, signal_name: str, payload: dict[str, Any] = {}) -> dict:
    """Send a signal to a running execution (e.g., pause/resume)."""
    # TODO: Implement Temporal workflow signaling
    return {"status": "signal_sent", "run_id": str(run_id), "signal": signal_name}
