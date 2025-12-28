-- Initialize additional databases needed by services
-- Main agent_runtime database is created by POSTGRES_DB env var

-- Keycloak database
CREATE DATABASE keycloak;

-- LangFuse database (if using LangFuse compose overlay)
CREATE DATABASE langfuse;

-- Temporal databases (auto-setup creates these, but we ensure they exist)
CREATE DATABASE temporal;
CREATE DATABASE temporal_visibility;
