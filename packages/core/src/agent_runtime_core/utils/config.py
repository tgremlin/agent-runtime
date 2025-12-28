"""Configuration management using Pydantic Settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/agent_runtime",
        alias="DATABASE_URL",
    )

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL",
    )

    # Temporal
    temporal_address: str = Field(
        default="localhost:7233",
        alias="TEMPORAL_ADDRESS",
    )
    temporal_namespace: str = Field(
        default="default",
        alias="TEMPORAL_NAMESPACE",
    )

    # S3/MinIO
    s3_endpoint: str = Field(
        default="http://localhost:9000",
        alias="S3_ENDPOINT",
    )
    s3_access_key: str = Field(
        default="minioadmin",
        alias="S3_ACCESS_KEY",
    )
    s3_secret_key: str = Field(
        default="minioadmin",
        alias="S3_SECRET_KEY",
    )
    s3_bucket: str = Field(
        default="agent-runtime",
        alias="S3_BUCKET",
    )

    # OIDC
    oidc_issuer: str = Field(
        default="http://localhost:8080/realms/agent-runtime",
        alias="OIDC_ISSUER",
    )
    oidc_client_id: str = Field(
        default="agent-runtime",
        alias="OIDC_CLIENT_ID",
    )
    oidc_client_secret: str = Field(
        default="",
        alias="OIDC_CLIENT_SECRET",
    )

    # LangFuse
    langfuse_host: str = Field(
        default="http://localhost:3000",
        alias="LANGFUSE_HOST",
    )
    langfuse_public_key: str = Field(
        default="",
        alias="LANGFUSE_PUBLIC_KEY",
    )
    langfuse_secret_key: str = Field(
        default="",
        alias="LANGFUSE_SECRET_KEY",
    )

    # Application
    public_base_url: str = Field(
        default="http://localhost:8000",
        alias="PUBLIC_BASE_URL",
    )
    debug: bool = Field(
        default=False,
        alias="DEBUG",
    )

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
