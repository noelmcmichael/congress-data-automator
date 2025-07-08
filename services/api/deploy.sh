#!/bin/bash
# Production deployment script for Congressional Data API Service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT="${ENVIRONMENT:-production}"
COMPOSE_FILE="docker-compose.production.yml"
SERVICE_NAME="congressional-api"

echo -e "${BLUE}Congressional Data API Service - Production Deployment${NC}"
echo "======================================================"
echo "Environment: ${ENVIRONMENT}"
echo "Compose File: ${COMPOSE_FILE}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    exit 1
fi

# Check if production environment file exists
if [ ! -f ".env.production" ]; then
    echo -e "${RED}Error: .env.production file not found${NC}"
    echo "Please copy .env.production.template to .env.production and configure it"
    exit 1
fi

# Validate environment file
echo -e "${YELLOW}Validating environment configuration...${NC}"
if ! grep -q "DATABASE_URL=postgresql://" .env.production; then
    echo -e "${RED}Error: DATABASE_URL not configured in .env.production${NC}"
    exit 1
fi

if ! grep -q "SECRET_KEY=" .env.production; then
    echo -e "${RED}Error: SECRET_KEY not configured in .env.production${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"

# Build the latest image
echo ""
echo -e "${YELLOW}Building latest image...${NC}"
./build.sh

# Create necessary directories
echo ""
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p logs ssl

# Set proper permissions
chmod 755 logs
echo -e "${GREEN}✓ Directories created${NC}"

# Deploy with Docker Compose
echo ""
echo -e "${YELLOW}Deploying with Docker Compose...${NC}"

# Stop existing services
docker-compose -f "${COMPOSE_FILE}" down

# Pull any external images
docker-compose -f "${COMPOSE_FILE}" pull postgres redis nginx

# Start services
docker-compose -f "${COMPOSE_FILE}" up -d

# Wait for services to be healthy
echo ""
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check service health
MAX_ATTEMPTS=30
ATTEMPT=1

while [ ${ATTEMPT} -le ${MAX_ATTEMPTS} ]; do
    if curl -f http://localhost:8003/health >/dev/null 2>&1; then
        echo -e "${GREEN}✓ API service is healthy${NC}"
        break
    fi
    
    echo "Attempt ${ATTEMPT}/${MAX_ATTEMPTS}: Waiting for API service..."
    sleep 5
    ATTEMPT=$((ATTEMPT + 1))
done

if [ ${ATTEMPT} -gt ${MAX_ATTEMPTS} ]; then
    echo -e "${RED}✗ API service failed to become healthy${NC}"
    echo "Checking logs:"
    docker-compose -f "${COMPOSE_FILE}" logs --tail=20 api
    exit 1
fi

# Show service status
echo ""
echo -e "${BLUE}Service Status:${NC}"
docker-compose -f "${COMPOSE_FILE}" ps

# Show logs
echo ""
echo -e "${BLUE}Recent logs:${NC}"
docker-compose -f "${COMPOSE_FILE}" logs --tail=10

# Test endpoints
echo ""
echo -e "${YELLOW}Testing endpoints...${NC}"

# Health check
if curl -s http://localhost:8003/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check: PASS${NC}"
else
    echo -e "${RED}✗ Health check: FAIL${NC}"
fi

# Detailed health check
if curl -s http://localhost:8003/healthz | grep -q "healthy"; then
    echo -e "${GREEN}✓ Detailed health check: PASS${NC}"
else
    echo -e "${RED}✗ Detailed health check: FAIL${NC}"
fi

# API endpoint test
if curl -s http://localhost:8003/api/v1/members?page=1&size=1 | grep -q "success"; then
    echo -e "${GREEN}✓ API endpoints: PASS${NC}"
else
    echo -e "${RED}✗ API endpoints: FAIL${NC}"
fi

echo ""
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo ""
echo "Service URLs:"
echo "  API: http://localhost:8003"
echo "  Health: http://localhost:8003/health"
echo "  Metrics: http://localhost:8003/metrics"
echo "  Documentation: http://localhost:8003/docs (if enabled)"
echo ""
echo "Management commands:"
echo "  View logs: docker-compose -f ${COMPOSE_FILE} logs -f"
echo "  Stop: docker-compose -f ${COMPOSE_FILE} down"
echo "  Restart: docker-compose -f ${COMPOSE_FILE} restart"
echo ""

# Optional: Show resource usage
if command -v docker &> /dev/null; then
    echo -e "${BLUE}Resource Usage:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | head -5
fi