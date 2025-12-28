FROM python:3.11-slim

WORKDIR /app

# Install uv for faster dependency resolution
RUN pip install uv

# Copy shared package first
COPY packages/core /app/packages/core

# Copy API service
COPY services/api /app/services/api

# Install dependencies
WORKDIR /app/services/api
RUN uv pip install --system -e /app/packages/core
RUN uv pip install --system -e .

# Run the API
EXPOSE 8000
CMD ["uvicorn", "agent_runtime_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
