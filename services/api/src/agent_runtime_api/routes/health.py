"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Basic health check."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check() -> dict:
    """Readiness check - verifies dependencies are available."""
    # TODO: Add checks for Postgres, Redis, Temporal connectivity
    return {"status": "ready"}
