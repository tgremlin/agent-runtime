#!/usr/bin/env python3
"""Database migration script for Agent Runtime.

This script handles database schema migrations using SQLAlchemy.
For production, consider using Alembic for more robust migrations.
"""

import asyncio
import os
import sys

# Add packages to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "packages", "core", "src"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def run_migrations() -> None:
    """Run database migrations."""
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/agent_runtime"
    )

    print(f"🗄️  Connecting to database...")
    engine = create_async_engine(database_url, echo=True)

    async with engine.begin() as conn:
        print("📝 Running migrations...")

        # Create extension for UUID generation
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))

        # Tenants table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tenants (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(63) NOT NULL UNIQUE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """))

        # Agents table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS agents (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """))

        # Agent versions table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS agent_versions (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
                version VARCHAR(50) NOT NULL,
                config JSONB DEFAULT '{}',
                is_published BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(agent_id, version)
            )
        """))

        # Runs table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS runs (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
                agent_version_id UUID NOT NULL REFERENCES agent_versions(id) ON DELETE CASCADE,
                status VARCHAR(20) NOT NULL DEFAULT 'pending',
                input JSONB DEFAULT '{}',
                output JSONB,
                error TEXT,
                workflow_id VARCHAR(255),
                workflow_run_id VARCHAR(255),
                started_at TIMESTAMP WITH TIME ZONE,
                completed_at TIMESTAMP WITH TIME ZONE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """))

        # Run events table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS run_events (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                run_id UUID NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
                event_type VARCHAR(100) NOT NULL,
                data JSONB DEFAULT '{}',
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """))

        # Indexes
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_agents_tenant ON agents(tenant_id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_agent_versions_agent ON agent_versions(agent_id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_runs_tenant ON runs(tenant_id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_runs_agent ON runs(agent_id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_run_events_run ON run_events(run_id)"))

        print("✅ Migrations completed successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_migrations())
