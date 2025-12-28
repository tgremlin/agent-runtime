# agent-runtime-api

Control plane API for Agent Runtime. FastAPI-based REST API that manages agents and triggers Temporal workflows.

## Installation

```bash
uv sync
```

## Running

```bash
uv run uvicorn agent_runtime_api.main:app --reload
```

## Endpoints

- `POST /runs` - Start a new agent run
- `GET /runs/{id}` - Get run status
- `GET /agents` - List agents
