"""Tenant management endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from agent_runtime_core.models import Tenant

router = APIRouter()


@router.get("/")
async def list_tenants() -> list[Tenant]:
    """List all tenants."""
    # TODO: Implement database query
    return []


@router.post("/", status_code=201)
async def create_tenant(tenant: Tenant) -> Tenant:
    """Create a new tenant."""
    # TODO: Implement database insert
    return tenant


@router.get("/{tenant_id}")
async def get_tenant(tenant_id: UUID) -> Tenant:
    """Get a tenant by ID."""
    # TODO: Implement database query
    raise HTTPException(status_code=404, detail="Tenant not found")
