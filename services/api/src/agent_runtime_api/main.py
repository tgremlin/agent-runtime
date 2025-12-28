"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent_runtime_core.utils import get_settings

from .routes import health, runs, agents, tenants


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown."""
    # Startup
    settings = get_settings()
    print(f"Starting Agent Runtime API (debug={settings.debug})")
    yield
    # Shutdown
    print("Shutting down Agent Runtime API")


app = FastAPI(
    title="Agent Runtime API",
    description="Control plane API for Agent Runtime",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(runs.router, prefix="/runs", tags=["runs"])
