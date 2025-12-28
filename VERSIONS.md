# Agent Runtime - Technology Versions

This document lists all technologies used in the Agent Runtime platform with their pinned versions and documentation links.

> **Last Updated:** 2024-12-28

---

## Infrastructure Services

### Database & Storage

| Technology | Version | Image | Documentation |
|------------|---------|-------|---------------|
| PostgreSQL | 16.4 | `postgres:16-alpine` | https://www.postgresql.org/docs/16/ |
| Redis | 7.4 | `redis:7-alpine` | https://redis.io/docs/latest/ |
| MinIO | 2024-11-07 | `minio/minio:RELEASE.2024-11-07T00-52-20Z` | https://min.io/docs/minio/linux/index.html |
| ClickHouse | 24.8 | `clickhouse/clickhouse-server:24.8` | https://clickhouse.com/docs/en/24.8 |

### Orchestration & Gateway

| Technology | Version | Image | Documentation |
|------------|---------|-------|---------------|
| Temporal Server | 1.24.2 | `temporalio/auto-setup:1.24.2` | https://docs.temporal.io/ |
| Temporal UI | 2.26.2 | `temporalio/ui:2.26.2` | https://docs.temporal.io/references/web-ui-configuration |
| Kong Gateway | 3.6 | `kong:3.6-ubuntu` | https://docs.konghq.com/gateway/3.6.x/ |

### Identity & Auth

| Technology | Version | Image | Documentation |
|------------|---------|-------|---------------|
| Keycloak | 24.0 | `quay.io/keycloak/keycloak:24.0` | https://www.keycloak.org/docs/24.0.5/ |

### Observability - LLM/Agent

| Technology | Version | Image | Documentation |
|------------|---------|-------|---------------|
| LangFuse | 2.95.0 | `langfuse/langfuse:2.95.0` | https://langfuse.com/docs |

### Observability - Infrastructure

| Technology | Version | Image | Documentation |
|------------|---------|-------|---------------|
| Prometheus | 2.51.0 | `prom/prometheus:v2.51.0` | https://prometheus.io/docs/prometheus/2.51/ |
| Grafana | 10.4.0 | `grafana/grafana:10.4.0` | https://grafana.com/docs/grafana/v10.4/ |
| Loki | 2.9.6 | `grafana/loki:2.9.6` | https://grafana.com/docs/loki/v2.9.x/ |
| Promtail | 2.9.6 | `grafana/promtail:2.9.6` | https://grafana.com/docs/loki/v2.9.x/send-data/promtail/ |

---

## Python Runtime & Build Tools

| Technology | Version | Documentation |
|------------|---------|---------------|
| Python | 3.11.10 | https://docs.python.org/3.11/ |
| uv | 0.5.x | https://docs.astral.sh/uv/ |
| Hatchling | 1.25.x | https://hatch.pypa.io/latest/ |

### About uv

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver written in Rust. It replaces pip, pip-tools, and virtualenv with a single tool that is 10-100x faster.

**Installation:**
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Key Commands:**
```bash
uv sync                    # Install deps & create .venv
uv run <command>           # Run command in venv
uv add <package>           # Add dependency
uv add --dev <package>     # Add dev dependency
uv lock                    # Update lock file
uv pip install -e .        # Editable install
```

**Why uv:**
- 10-100x faster than pip
- Automatic virtual environment management
- Native pyproject.toml support
- Deterministic lock files
- Drop-in pip replacement

---

## Python Dependencies

### Core Package (`packages/core`)

| Package | Version | Documentation |
|---------|---------|---------------|
| Pydantic | 2.10.3 | https://docs.pydantic.dev/2.10/ |
| SQLAlchemy | 2.0.36 | https://docs.sqlalchemy.org/en/20/ |
| asyncpg | 0.30.0 | https://magicstack.github.io/asyncpg/current/ |

### API Service (`services/api`)

| Package | Version | Documentation |
|---------|---------|---------------|
| FastAPI | 0.115.6 | https://fastapi.tiangolo.com/ |
| Uvicorn | 0.32.1 | https://www.uvicorn.org/ |
| Pydantic | 2.10.3 | https://docs.pydantic.dev/2.10/ |
| Pydantic-Settings | 2.6.1 | https://docs.pydantic.dev/2.10/concepts/pydantic_settings/ |
| SQLAlchemy | 2.0.36 | https://docs.sqlalchemy.org/en/20/ |
| asyncpg | 0.30.0 | https://magicstack.github.io/asyncpg/current/ |
| redis-py | 5.2.1 | https://redis-py.readthedocs.io/en/stable/ |
| temporalio | 1.8.0 | https://python.temporal.io/ |
| python-jose | 3.3.0 | https://python-jose.readthedocs.io/en/latest/ |
| httpx | 0.28.1 | https://www.python-httpx.org/ |

### Worker Service (`services/worker`)

| Package | Version | Documentation |
|---------|---------|---------------|
| temporalio | 1.8.0 | https://python.temporal.io/ |
| Pydantic | 2.10.3 | https://docs.pydantic.dev/2.10/ |
| Pydantic-Settings | 2.6.1 | https://docs.pydantic.dev/2.10/concepts/pydantic_settings/ |
| Pydantic-AI | 0.0.40 | https://ai.pydantic.dev/ |
| SQLAlchemy | 2.0.36 | https://docs.sqlalchemy.org/en/20/ |
| asyncpg | 0.30.0 | https://magicstack.github.io/asyncpg/current/ |
| redis-py | 5.2.1 | https://redis-py.readthedocs.io/en/stable/ |
| httpx | 0.28.1 | https://www.python-httpx.org/ |
| boto3 | 1.35.81 | https://boto3.amazonaws.com/v1/documentation/api/1.35.81/index.html |
| langfuse | 2.57.5 | https://langfuse.com/docs/sdk/python |

### Dev Dependencies

| Package | Version | Documentation |
|---------|---------|---------------|
| pytest | 8.3.4 | https://docs.pytest.org/en/8.3.x/ |
| pytest-asyncio | 0.24.0 | https://pytest-asyncio.readthedocs.io/en/stable/ |

---

## Documentation URLs for RAG Knowledge Base

### Primary Documentation (High Priority)

```
# Core Framework
https://fastapi.tiangolo.com/
https://docs.pydantic.dev/2.10/
https://docs.sqlalchemy.org/en/20/
https://python.temporal.io/
https://ai.pydantic.dev/

# Infrastructure
https://www.postgresql.org/docs/16/
https://redis.io/docs/latest/
https://docs.konghq.com/gateway/3.6.x/
https://www.keycloak.org/docs/24.0.5/
https://docs.temporal.io/

# Observability
https://langfuse.com/docs
https://prometheus.io/docs/prometheus/2.51/
https://grafana.com/docs/grafana/v10.4/
```

### Secondary Documentation

```
# Storage & Data
https://min.io/docs/minio/linux/index.html
https://clickhouse.com/docs/en/24.8
https://boto3.amazonaws.com/v1/documentation/api/1.35.81/index.html

# Python Libraries
https://www.python-httpx.org/
https://redis-py.readthedocs.io/en/stable/
https://magicstack.github.io/asyncpg/current/
https://www.uvicorn.org/
https://python-jose.readthedocs.io/en/latest/

# Testing
https://docs.pytest.org/en/8.3.x/
https://pytest-asyncio.readthedocs.io/en/stable/

# Build Tools
https://docs.python.org/3.11/
https://docs.astral.sh/uv/
https://hatch.pypa.io/latest/

# Logs
https://grafana.com/docs/loki/v2.9.x/
```

---

## Version Update Checklist

When updating versions:

1. **Docker Images** - Update in `docker/docker-compose*.yml`
2. **Python Deps** - Update in `packages/*/pyproject.toml` and `services/*/pyproject.toml`
3. **Python Runtime** - Update in `services/*/Dockerfile`
4. **This File** - Update version numbers and "Last Updated" date
5. **Lock Files** - Run `uv sync` in each package/service directory
