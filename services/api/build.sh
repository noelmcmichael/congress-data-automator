#!/bin/bash
# Production build script for Congressional Data API Service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="congressional-api"
REGISTRY="${REGISTRY:-}"
VERSION="${VERSION:-$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')}"
DOCKERFILE="${DOCKERFILE:-Dockerfile.optimized}"

echo -e "${BLUE}Congressional Data API Service - Production Build${NC}"
echo "=================================================="
echo "Image: ${IMAGE_NAME}"
echo "Version: ${VERSION}"
echo "Dockerfile: ${DOCKERFILE}"
echo "Registry: ${REGISTRY:-<local>}"
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    exit 1
fi

# Build the image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build \
    -t "${IMAGE_NAME}:${VERSION}" \
    -t "${IMAGE_NAME}:latest" \
    -f "${DOCKERFILE}" \
    --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --build-arg VCS_REF="$(git rev-parse HEAD 2>/dev/null || echo 'unknown')" \
    .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build completed successfully${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

# Show image size
echo ""
echo -e "${BLUE}Image Information:${NC}"
docker images "${IMAGE_NAME}:${VERSION}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Tag for registry if specified
if [ -n "${REGISTRY}" ]; then
    echo ""
    echo -e "${YELLOW}Tagging for registry...${NC}"
    docker tag "${IMAGE_NAME}:${VERSION}" "${REGISTRY}/${IMAGE_NAME}:${VERSION}"
    docker tag "${IMAGE_NAME}:latest" "${REGISTRY}/${IMAGE_NAME}:latest"
    echo -e "${GREEN}✓ Tagged for registry: ${REGISTRY}${NC}"
fi

# Optional: Run security scan
if command -v trivy &> /dev/null; then
    echo ""
    echo -e "${YELLOW}Running security scan...${NC}"
    trivy image "${IMAGE_NAME}:${VERSION}"
fi

echo ""
echo -e "${GREEN}Build completed successfully!${NC}"
echo ""
echo "Commands to run the container:"
echo "  Development: docker run -p 8003:8003 ${IMAGE_NAME}:${VERSION}"
echo "  Production:  docker-compose -f docker-compose.production.yml up"
echo ""

# Optional: Push to registry
if [ -n "${REGISTRY}" ] && [ "${PUSH:-false}" = "true" ]; then
    echo -e "${YELLOW}Pushing to registry...${NC}"
    docker push "${REGISTRY}/${IMAGE_NAME}:${VERSION}"
    docker push "${REGISTRY}/${IMAGE_NAME}:latest"
    echo -e "${GREEN}✓ Pushed to registry${NC}"
fi