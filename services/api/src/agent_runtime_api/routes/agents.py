"""Agent management endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from agent_runtime_core.models import Agent, AgentVersion

router = APIRouter()


@router.get("/")
async def list_agents(tenant_id: UUID | None = None) -> list[Agent]:
    """List all agents, optionally filtered by tenant."""
    # TODO: Implement database query
    return []


@router.post("/", status_code=201)
async def create_agent(agent: Agent) -> Agent:
    """Create a new agent."""
    # TODO: Implement database insert
    return agent


@router.get("/{agent_id}")
async def get_agent(agent_id: UUID) -> Agent:
    """Get an agent by ID."""
    # TODO: Implement database query
    raise HTTPException(status_code=404, detail="Agent not found")


@router.get("/{agent_id}/versions")
async def list_agent_versions(agent_id: UUID) -> list[AgentVersion]:
    """List all versions of an agent."""
    # TODO: Implement database query
    return []


@router.post("/{agent_id}/versions", status_code=201)
async def create_agent_version(agent_id: UUID, version: AgentVersion) -> AgentVersion:
    """Create a new version of an agent."""
    # TODO: Implement database insert
    return version
