#!/bin/bash
# Package images and configs for offline/airgapped deployment

set -e

echo "📦 Packaging Agent Runtime for offline deployment..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${PROJECT_ROOT}/dist/offline"

mkdir -p "$OUTPUT_DIR"

# List of images to save
IMAGES=(
    "kong:3.6-ubuntu"
    "quay.io/keycloak/keycloak:24.0"
    "temporalio/auto-setup:1.24"
    "temporalio/ui:2.26.2"
    "postgres:16-alpine"
    "redis:7-alpine"
    "minio/minio:latest"
    # LangFuse (optional)
    "langfuse/langfuse:2"
    "clickhouse/clickhouse-server:24"
)

echo "🐳 Pulling images..."
for image in "${IMAGES[@]}"; do
    echo "  Pulling $image..."
    docker pull "$image"
done

echo "💾 Saving images to tarball..."
docker save "${IMAGES[@]}" | gzip > "$OUTPUT_DIR/agent-runtime-images.tar.gz"

echo "📁 Copying configuration files..."
cp -r "$PROJECT_ROOT/docker" "$OUTPUT_DIR/"
cp -r "$PROJECT_ROOT/gateway" "$OUTPUT_DIR/"
cp -r "$PROJECT_ROOT/auth" "$OUTPUT_DIR/"

echo "📝 Creating load script..."
cat > "$OUTPUT_DIR/offline-load.sh" << 'EOF'
#!/bin/bash
# Load images from offline package
set -e
echo "🐳 Loading Docker images..."
gunzip -c agent-runtime-images.tar.gz | docker load
echo "✅ Images loaded successfully!"
echo ""
echo "Next steps:"
echo "  1. cd docker && cp .env.example .env"
echo "  2. Edit .env with your configuration"
echo "  3. docker compose up -d"
EOF
chmod +x "$OUTPUT_DIR/offline-load.sh"

echo ""
echo "✅ Offline package created at: $OUTPUT_DIR"
echo "   - agent-runtime-images.tar.gz (Docker images)"
echo "   - docker/ (Compose files)"
echo "   - gateway/ (Kong config)"
echo "   - auth/ (Keycloak config)"
echo "   - offline-load.sh (Load script)"
