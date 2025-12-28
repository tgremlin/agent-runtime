# agent-runtime-worker

Execution plane worker for Agent Runtime. Temporal worker that executes agent activities.

## Installation

```bash
uv sync
```

## Running

```bash
uv run python -m agent_runtime_worker.worker
```

## Activities

- LLM calls via Pydantic-AI
- Tool execution
- Artifact storage (S3/MinIO)
