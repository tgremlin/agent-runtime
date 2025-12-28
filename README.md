# Agent Runtime

A durable, portable, and offline-capable AI agent execution platform.

## Overview

Agent Runtime is the core execution kernel for running AI agents with full durability and resumability. It provides a clean separation between control plane and execution plane, supporting both local (Docker Compose) and AWS cloud deployments with minimal divergence.

## Features

- **Durable Execution**: Agent runs survive full stack restarts via Temporal workflows
- **Portable Deployment**: Same architecture runs locally and in AWS
- **Offline-Capable**: Full functionality without internet connectivity
- **Agent Agnostic**: Supports PydanticAI, CrewAI, LangChain, and custom agents
- **Observable**: LangFuse integration for LLM/agent tracing

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│    Kong     │────▶│     API     │
└─────────────┘     │  (Gateway)  │     │  (Control)  │
                    └─────────────┘     └──────┬──────┘
                                               │
                    ┌─────────────┐     ┌──────▼──────┐
                    │   Worker    │◀────│  Temporal   │
                    │ (Execution) │     │  (Durable)  │
                    └──────┬──────┘     └─────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Postgres │     │  Redis   │     │  MinIO   │
   │  (SoR)   │     │ (Cache)  │     │ (S3/Obj) │
   └──────────┘     └──────────┘     └──────────┘
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Tenant** | Isolated organizational boundary |
| **Agent** | A logical AI capability definition |
| **Agent Version** | Immutable configuration of an agent |
| **Run** | A single execution of an agent version |

## Repository Structure

```
agent-runtime/
├── docs/                  # Architecture, PRD, diagrams
├── packages/
│   └── core/              # Shared Python package (models, db, utils)
├── services/
│   ├── api/               # Control plane (FastAPI)
│   └── worker/            # Execution plane (Temporal workers)
├── gateway/               # Kong declarative config
├── auth/                  # Keycloak realm config
├── docker/                # Docker Compose files
├── infra/                 # AWS deployment (ECS/OpenTofu)
├── scripts/               # Dev and deployment utilities
└── .github/               # CI/CD workflows
```

## Tech Stack

### Core (MVP)
- **Gateway**: Kong (DB-less mode)
- **Identity**: Keycloak (OIDC)
- **Orchestration**: Temporal
- **Database**: PostgreSQL
- **Cache**: Redis
- **Object Storage**: MinIO (S3-compatible)
- **Agent Observability**: LangFuse

### Application
- **Language**: Python 3.11+
- **Package Manager**: [uv](https://docs.astral.sh/uv/) (fast pip alternative)
- **Build Backend**: Hatchling
- **API Framework**: FastAPI
- **Validation**: Pydantic
- **Agent Frameworks**: PydanticAI, CrewAI (agent-agnostic)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager

### Installing uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip (any platform)
pip install uv
```

### Local Development

```bash
# 1. Clone and setup
git clone <repo-url>
cd agent-runtime

# 2. Start infrastructure
docker compose -f docker/docker-compose.yml up -d

# 3. (Optional) Start LangFuse for agent observability
docker compose -f docker/docker-compose.yml -f docker/docker-compose.langfuse.yml up -d

# 4. Install dependencies
cd packages/core && uv sync && cd ../..
cd services/api && uv sync && cd ../..
cd services/worker && uv sync && cd ../..

# 5. Run migrations
python scripts/migrate.py

# 6. Start services (development mode)
# Terminal 1: API
cd services/api && uv run uvicorn agent_runtime_api.main:app --reload

# Terminal 2: Worker
cd services/worker && uv run python -m agent_runtime_worker.worker
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp docker/.env.example docker/.env
```

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `TEMPORAL_ADDRESS` - Temporal server address
- `S3_ENDPOINT` - MinIO/S3 endpoint
- `OIDC_ISSUER` - Keycloak issuer URL
- `LANGFUSE_HOST` - LangFuse server URL

## Documentation

- [Product Requirements (PRD)](docs/PRD.md)
- [Technology Stack](docs/technology-stack.md)
- [Technology Versions](VERSIONS.md) - Pinned versions & documentation links
- [MVP Sequence Diagram](docs/mvp-sequence-diagram.md)
- [Repository Layout](docs/repository-layout.md)

## Development

### Package Structure

The `packages/core` package contains shared code used by both API and Worker:

```python
from agent_runtime_core.models import Run, Agent, Tenant
from agent_runtime_core.db import get_session
```

### Running Tests

```bash
# Specific service (using uv)
cd services/api && uv run pytest
cd services/worker && uv run pytest

# Or activate the venv first
cd services/api
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pytest
```

### Common uv Commands

```bash
# Sync dependencies (creates .venv if needed)
uv sync

# Run a command in the virtual environment
uv run <command>

# Add a new dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Update lock file
uv lock
```

## Deployment

### Local (Docker Compose)
See [Quick Start](#quick-start) above.

### AWS (ECS)
See `infra/aws/` for OpenTofu/Terraform configurations.

## License

[TBD]
