# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Runtime is a durable, portable AI agent execution platform. It provides a clean separation between control plane (API) and execution plane (Worker), using Temporal for workflow orchestration. Supports both local (Docker Compose) and AWS cloud deployments with minimal divergence.

## Build & Development Commands

### Start Infrastructure
```bash
# Core services (Postgres, Redis, MinIO, Temporal, Kong, Keycloak)
docker compose -f docker/docker-compose.yml up -d

# With LangFuse observability
docker compose -f docker/docker-compose.yml -f docker/docker-compose.langfuse.yml up -d
```

### Install Dependencies (uses uv)
```bash
cd packages/core && uv sync
cd services/api && uv sync
cd services/worker && uv sync
```

### Run Services (Development Mode)
```bash
# API (Control Plane) - Terminal 1
cd services/api && uv run uvicorn agent_runtime_api.main:app --reload

# Worker (Execution Plane) - Terminal 2
cd services/worker && uv run python -m agent_runtime_worker.worker
```

### Run Migrations
```bash
python scripts/migrate.py
```

### Run Tests
```bash
# All tests in a service
cd services/api && pytest
cd services/worker && pytest

# Single test file
cd services/api && pytest tests/test_runs.py

# Single test
cd services/api && pytest tests/test_runs.py::test_create_run
```

## Architecture

```
Client → Kong (8000) → API (8002) → Temporal (7233) → Worker
                                         ↓
                           Postgres / Redis / MinIO
```

**Three Python packages:**
- `packages/core` (`agent_runtime_core`) - Shared models, DB session, utilities
- `services/api` (`agent_runtime_api`) - FastAPI control plane, starts Temporal workflows
- `services/worker` (`agent_runtime_worker`) - Temporal activities (LLM calls, tool execution)

**Key patterns:**
- API creates Run records, then starts `AgentRunWorkflow` in Temporal
- Worker executes activities defined in `services/worker/src/agent_runtime_worker/activities/`
- All services share models from `packages/core` via editable install (`tool.uv.sources`)

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Tenant** | Isolated organizational boundary |
| **Agent** | Logical AI capability definition |
| **Agent Version** | Immutable configuration of an agent |
| **Run** | Single execution of an agent version |

## Service Ports (Local)

| Service | Port | Purpose |
|---------|------|---------|
| Kong Proxy | 8000 | API Gateway |
| Kong Admin | 8001 | Gateway management |
| API | 8002 | Control plane direct access |
| Keycloak | 8080 | Identity provider |
| Temporal | 7233 | Workflow engine |
| Temporal UI | 8088 | Workflow visualization |
| Postgres | 5432 | System of record |
| Redis | 6379 | Cache |
| MinIO API | 9000 | Object storage |
| MinIO Console | 9001 | Storage UI |

## Environment Variables

Key variables (set in `docker/.env`):
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `TEMPORAL_ADDRESS` - Temporal server
- `S3_ENDPOINT` - MinIO/S3 endpoint
- `OIDC_ISSUER` - Keycloak issuer URL
- `LANGFUSE_HOST` - LangFuse server (optional)

Code never branches on "local vs cloud" — only on env vars.

## Technology Versions

All technology versions are pinned and documented in `VERSIONS.md`. This includes:
- Docker image versions (Postgres, Redis, Temporal, Kong, Keycloak, etc.)
- Python dependency versions (FastAPI, Pydantic, SQLAlchemy, etc.)
- Documentation links for each technology

When updating dependencies, update both the source files and `VERSIONS.md`.

## Adding New Features

**New Temporal Activity:**
1. Add activity in `services/worker/src/agent_runtime_worker/activities/`
2. Register in workflow at `services/worker/src/agent_runtime_worker/workflows/agent_run.py`

**New API Endpoint:**
1. Add route in `services/api/src/agent_runtime_api/routes/`
2. Register router in `services/api/src/agent_runtime_api/main.py`

**New Shared Model:**
1. Add to `packages/core/src/agent_runtime_core/models/`
2. Export from `packages/core/src/agent_runtime_core/models/__init__.py`
