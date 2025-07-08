#!/bin/bash
# Multi-platform deployment script for Congressional Data API Service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PLATFORM="${1:-}"
ENVIRONMENT="${ENVIRONMENT:-production}"

echo -e "${BLUE}Congressional Data API Service - Cloud Deployment${NC}"
echo "=================================================="
echo ""

# Show usage if no platform specified
if [ -z "$PLATFORM" ]; then
    echo "Usage: $0 <platform> [options]"
    echo ""
    echo "Supported platforms:"
    echo "  railway     - Deploy to Railway"
    echo "  render      - Deploy to Render"
    echo "  gcp         - Deploy to Google Cloud Platform"
    echo "  docker-hub  - Build and push to Docker Hub"
    echo ""
    echo "Examples:"
    echo "  $0 railway"
    echo "  $0 render"
    echo "  $0 gcp"
    echo "  REGISTRY=your-registry $0 docker-hub"
    echo ""
    exit 1
fi

echo "Platform: ${PLATFORM}"
echo "Environment: ${ENVIRONMENT}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"

# Platform-specific deployment
case $PLATFORM in
    "railway")
        echo -e "${YELLOW}Deploying to Railway...${NC}"
        
        # Check Railway CLI
        if ! command -v railway &> /dev/null; then
            echo -e "${RED}Error: Railway CLI not installed${NC}"
            echo "Install with: npm install -g @railway/cli"
            exit 1
        fi
        
        # Login check
        if ! railway whoami &> /dev/null; then
            echo "Please login to Railway:"
            railway login
        fi
        
        # Build and deploy
        echo "Building Docker image..."
        docker build -t congressional-api:latest -f Dockerfile.optimized .
        
        echo "Deploying to Railway..."
        railway up --service congressional-api
        
        echo -e "${GREEN}✓ Deployed to Railway${NC}"
        echo "Check your Railway dashboard for the service URL"
        ;;
        
    "render")
        echo -e "${YELLOW}Deploying to Render...${NC}"
        
        echo "To deploy to Render:"
        echo "1. Fork this repository to your GitHub account"
        echo "2. Connect your GitHub account to Render"
        echo "3. Create a new Blueprint from the render.yaml file"
        echo "4. Set the required environment variables in Render dashboard"
        echo ""
        echo "The render.yaml file is already configured for automatic deployment"
        echo -e "${GREEN}✓ Render configuration ready${NC}"
        ;;
        
    "gcp")
        echo -e "${YELLOW}Deploying to Google Cloud Platform...${NC}"
        
        # Check gcloud CLI
        if ! command -v gcloud &> /dev/null; then
            echo -e "${RED}Error: gcloud CLI not installed${NC}"
            echo "Install from: https://cloud.google.com/sdk/docs/install"
            exit 1
        fi
        
        # Check if authenticated
        if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 &> /dev/null; then
            echo "Please authenticate with Google Cloud:"
            gcloud auth login
        fi
        
        # Get project ID
        PROJECT_ID=$(gcloud config get-value project)
        if [ -z "$PROJECT_ID" ]; then
            echo -e "${RED}Error: No GCP project set${NC}"
            echo "Set with: gcloud config set project YOUR_PROJECT_ID"
            exit 1
        fi
        
        echo "Project ID: $PROJECT_ID"
        
        # Build and submit to Cloud Build
        echo "Building with Cloud Build..."
        gcloud builds submit --config cloudbuild.yaml .
        
        echo -e "${GREEN}✓ Deployed to Google Cloud Platform${NC}"
        echo "Service URL: https://congressional-api-$PROJECT_ID.a.run.app"
        ;;
        
    "docker-hub")
        echo -e "${YELLOW}Building and pushing to Docker Hub...${NC}"
        
        REGISTRY="${REGISTRY:-}"
        if [ -z "$REGISTRY" ]; then
            echo -e "${RED}Error: REGISTRY environment variable not set${NC}"
            echo "Set with: export REGISTRY=your-dockerhub-username"
            exit 1
        fi
        
        # Check Docker Hub authentication
        if ! docker info | grep -q "Username:"; then
            echo "Please login to Docker Hub:"
            docker login
        fi
        
        # Build and push
        VERSION=$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')
        IMAGE_NAME="$REGISTRY/congressional-api"
        
        echo "Building image: $IMAGE_NAME:$VERSION"
        docker build -t "$IMAGE_NAME:$VERSION" -t "$IMAGE_NAME:latest" -f Dockerfile.optimized .
        
        echo "Pushing to Docker Hub..."
        docker push "$IMAGE_NAME:$VERSION"
        docker push "$IMAGE_NAME:latest"
        
        echo -e "${GREEN}✓ Pushed to Docker Hub${NC}"
        echo "Image: $IMAGE_NAME:$VERSION"
        echo "Latest: $IMAGE_NAME:latest"
        ;;
        
    "terraform")
        echo -e "${YELLOW}Deploying with Terraform...${NC}"
        
        # Check Terraform
        if ! command -v terraform &> /dev/null; then
            echo -e "${RED}Error: Terraform not installed${NC}"
            echo "Install from: https://www.terraform.io/downloads.html"
            exit 1
        fi
        
        # Check if terraform.tfvars exists
        if [ ! -f "terraform/terraform.tfvars" ]; then
            echo -e "${RED}Error: terraform/terraform.tfvars not found${NC}"
            echo "Copy terraform/terraform.tfvars.example to terraform/terraform.tfvars and configure it"
            exit 1
        fi
        
        cd terraform
        
        echo "Initializing Terraform..."
        terraform init
        
        echo "Planning deployment..."
        terraform plan
        
        echo -e "${YELLOW}Apply this plan? (y/N):${NC}"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo "Applying Terraform configuration..."
            terraform apply -auto-approve
            
            echo -e "${GREEN}✓ Deployed with Terraform${NC}"
            terraform output
        else
            echo "Deployment cancelled"
        fi
        
        cd ..
        ;;
        
    *)
        echo -e "${RED}Error: Unknown platform '$PLATFORM'${NC}"
        echo "Supported platforms: railway, render, gcp, docker-hub, terraform"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Cloud deployment completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Verify the service is running"
echo "2. Test the API endpoints"
echo "3. Set up monitoring and alerts"
echo "4. Configure custom domain (if needed)"
echo ""