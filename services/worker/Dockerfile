FROM python:3.11.10-slim

WORKDIR /app

# Install uv for faster dependency resolution
RUN pip install uv

# Copy shared package first
COPY packages/core /app/packages/core

# Copy worker service
COPY services/worker /app/services/worker

# Install dependencies
WORKDIR /app/services/worker
RUN uv pip install --system -e /app/packages/core
RUN uv pip install --system -e .

# Run the worker
CMD ["python", "-m", "agent_runtime_worker.worker"]
