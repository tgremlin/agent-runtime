#!/bin/bash
# Development environment setup script

set -e

echo "🚀 Setting up Agent Runtime development environment..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }

# Check for uv (recommended) or pip
if command -v uv >/dev/null 2>&1; then
    PKG_MANAGER="uv"
    echo "✓ Using uv for package management"
else
    PKG_MANAGER="pip"
    echo "⚠ uv not found, falling back to pip (consider installing uv for faster installs)"
fi

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Create .env file if it doesn't exist
if [ ! -f docker/.env ]; then
    echo "📝 Creating docker/.env from template..."
    cp docker/.env.example docker/.env
    echo "⚠  Please review and update docker/.env with secure passwords"
fi

# Install Python packages
echo "📦 Installing Python packages..."

if [ "$PKG_MANAGER" = "uv" ]; then
    # Install core package
    cd packages/core
    uv sync
    cd ../..

    # Install API service
    cd services/api
    uv sync
    cd ../..

    # Install worker service
    cd services/worker
    uv sync
    cd ../..
else
    # pip fallback
    pip install -e packages/core
    pip install -e services/api
    pip install -e services/worker
fi

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review docker/.env and update passwords"
echo "  2. Start infrastructure: cd docker && docker compose up -d"
echo "  3. (Optional) Start LangFuse: docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d"
echo "  4. Run API: cd services/api && uv run uvicorn agent_runtime_api.main:app --reload"
echo "  5. Run Worker: cd services/worker && uv run python -m agent_runtime_worker.worker"
