# Congressional Data API Service - Deployment Guide

## Overview

This guide covers deploying the Congressional Data API Service to various cloud platforms and environments. The service is production-ready with comprehensive error handling, monitoring, and security features.

## Prerequisites

- Docker installed and running
- Git repository access
- Cloud platform account (see platform-specific requirements below)

## Quick Deploy Options

### Option 1: Railway (Recommended for simplicity)

**Best for**: Small to medium scale, simple deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
./deploy-cloud.sh railway
```

**Features**: 
- Automatic HTTPS
- Built-in PostgreSQL and Redis
- Zero-config deployment
- $5/month starter plan

### Option 2: Render (Recommended for cost-effectiveness)

**Best for**: Cost-conscious deployments, static configuration

```bash
# Deploy using Blueprint
./deploy-cloud.sh render
```

**Manual Steps**:
1. Fork this repository to your GitHub
2. Connect GitHub to Render
3. Create new Blueprint from `render.yaml`
4. Configure environment variables

**Features**:
- Free tier available
- Automatic deployments from Git
- Built-in PostgreSQL and Redis
- SSL certificates included

### Option 3: Google Cloud Platform (Recommended for enterprise)

**Best for**: Enterprise deployments, advanced features, high scale

```bash
# Prerequisites
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy with Cloud Build
./deploy-cloud.sh gcp
```

**Features**:
- Auto-scaling with Cloud Run
- Managed PostgreSQL (Cloud SQL)
- Redis (Memorystore)
- Global CDN and load balancing

### Option 4: Docker Hub + Any Platform

**Best for**: Flexible deployment to any Docker-compatible platform

```bash
# Build and push to Docker Hub
REGISTRY=your-username ./deploy-cloud.sh docker-hub

# Use the image anywhere
docker run -p 8003:8003 your-username/congressional-api:latest
```

### Option 5: Kubernetes (Advanced)

**Best for**: Large scale, on-premise, or multi-cloud deployments

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## Detailed Platform Guides

### Railway Deployment

Railway offers the simplest deployment experience with built-in databases.

#### Setup Steps:

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Initialize**:
   ```bash
   railway login
   railway init
   ```

3. **Deploy**:
   ```bash
   ./deploy-cloud.sh railway
   ```

4. **Configure Environment Variables** (in Railway dashboard):
   - `DATABASE_URL` - Automatically provided by Railway PostgreSQL
   - `SECRET_KEY` - Generate a secure key
   - `REDIS_URL` - Automatically provided by Railway Redis

#### Railway Pricing:
- **Starter**: $5/month - 512MB RAM, shared CPU
- **Pro**: $20/month - 8GB RAM, 8 vCPUs
- **Team**: Custom pricing

#### Pros:
- Easiest setup
- Built-in databases
- Automatic HTTPS
- GitHub integration

#### Cons:
- Limited customization
- Vendor lock-in

### Render Deployment

Render provides an excellent balance of simplicity and features.

#### Setup Steps:

1. **Fork Repository**: Fork this repo to your GitHub account

2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Create new Blueprint

3. **Deploy**:
   - Select this repository
   - Choose `render.yaml` as blueprint
   - Configure environment variables

4. **Environment Variables**:
   ```
   SECRET_KEY=your-secure-secret-key
   CORS_ORIGINS=["https://yourdomain.com"]
   ```

#### Render Pricing:
- **Free**: 512MB RAM, shared CPU (with limitations)
- **Starter**: $7/month - 512MB RAM, 0.1 CPU
- **Standard**: $25/month - 2GB RAM, 1 CPU

#### Pros:
- Free tier available
- Automatic deployments
- Built-in SSL
- Good performance

#### Cons:
- Limited to Git-based deployments
- Less control over infrastructure

### Google Cloud Platform Deployment

GCP offers enterprise-grade features with global scale.

#### Setup Steps:

1. **Install and Configure gcloud**:
   ```bash
   # Install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   
   # Authenticate
   gcloud auth login
   
   # Set project
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Enable APIs**:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable sqladmin.googleapis.com
   ```

3. **Deploy with Cloud Build**:
   ```bash
   ./deploy-cloud.sh gcp
   ```

4. **Alternative: Terraform Deployment**:
   ```bash
   # Copy and configure variables
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   
   # Edit terraform.tfvars with your values
   ./deploy-cloud.sh terraform
   ```

#### Environment Variables (Secret Manager):
- `DATABASE_URL` - Automatically configured by Terraform
- `SECRET_KEY` - Stored in Secret Manager
- `REDIS_URL` - Automatically configured

#### GCP Pricing (estimated):
- **Cloud Run**: $0.24/million requests
- **Cloud SQL**: $7.67/month (db-f1-micro)
- **Redis**: $26.35/month (1GB)
- **Total**: ~$35/month for moderate usage

#### Pros:
- Enterprise features
- Global scale
- Excellent monitoring
- Managed services

#### Cons:
- More complex setup
- Higher cost
- Requires GCP knowledge

### Kubernetes Deployment

For advanced users requiring maximum control and scalability.

#### Setup Steps:

1. **Prepare Cluster**: Ensure you have a running Kubernetes cluster

2. **Configure Secrets**:
   ```bash
   # Create secrets (base64 encoded)
   echo -n "postgresql://user:pass@host:5432/db" | base64
   # Update k8s/secret.yaml with encoded values
   ```

3. **Deploy**:
   ```bash
   kubectl apply -f k8s/
   ```

4. **Verify Deployment**:
   ```bash
   kubectl get pods -n congressional-api
   kubectl get services -n congressional-api
   ```

#### Features:
- Horizontal auto-scaling
- Rolling updates
- Health checks
- Load balancing

#### Requirements:
- Kubernetes cluster (EKS, GKE, AKS, or self-managed)
- kubectl configured
- Ingress controller (nginx recommended)
- cert-manager for SSL (optional)

## Environment Configuration

### Required Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-super-secure-secret-key-at-least-32-characters

# Optional but recommended
REDIS_URL=redis://host:port/0
CORS_ORIGINS=["https://yourdomain.com"]
```

### Production Environment Variables

```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8003
UVICORN_WORKERS=4
DATABASE_POOL_SIZE=20
RATE_LIMIT_REQUESTS=100
CACHE_ENABLED=true
METRICS_ENABLED=true
SECURITY_HEADERS_ENABLED=true
```

## Post-Deployment Steps

### 1. Verify Deployment

```bash
# Health check
curl https://your-domain.com/health

# Detailed health check
curl https://your-domain.com/healthz

# API test
curl https://your-domain.com/api/v1/members?page=1&size=1
```

### 2. Database Migration

```bash
# If using existing data, migrate from SQLite to PostgreSQL
# This will be covered in the next deployment step
```

### 3. Monitor Performance

- Check response times: `/metrics` endpoint
- Monitor error rates: application logs
- Set up alerts for health check failures

### 4. Configure Custom Domain (if needed)

- **Railway**: Add custom domain in dashboard
- **Render**: Configure custom domain in settings
- **GCP**: Update Cloud Run service domain mapping
- **Kubernetes**: Configure ingress with your domain

## Troubleshooting

### Common Issues

1. **Container Fails to Start**:
   ```bash
   # Check logs
   docker logs container-name
   
   # For Kubernetes
   kubectl logs -n congressional-api deployment/congressional-api
   ```

2. **Database Connection Errors**:
   - Verify `DATABASE_URL` format
   - Check database server accessibility
   - Ensure database exists and user has permissions

3. **Health Check Failures**:
   - Verify port configuration (8003)
   - Check container startup time
   - Review application logs

### Getting Help

- **Issues**: Open GitHub issue with logs and configuration
- **Documentation**: Check `/docs` endpoint when deployed
- **Community**: Join discussions in repository

## Security Considerations

### Production Checklist

- [ ] Use HTTPS only
- [ ] Set secure `SECRET_KEY`
- [ ] Configure proper CORS origins
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Use environment variables for secrets
- [ ] Enable security headers
- [ ] Review and audit access logs

### Monitoring

Each deployment includes:
- Health checks (`/health`, `/healthz`)
- Metrics endpoint (`/metrics`)
- Performance monitoring
- Error tracking
- Request logging

## Cost Optimization

### Tips for Reducing Costs

1. **Start Small**: Use free tiers or starter plans
2. **Auto-scaling**: Configure based on actual usage
3. **Resource Limits**: Set appropriate CPU/memory limits
4. **Caching**: Enable Redis caching to reduce database load
5. **CDN**: Use cloud provider CDN for static content
6. **Monitoring**: Track usage to optimize resources

### Cost Comparison

| Platform | Free Tier | Starter | Production | Best For |
|----------|-----------|---------|------------|----------|
| Railway  | No        | $5/mo   | $20+/mo    | Simplicity |
| Render   | Yes       | $7/mo   | $25+/mo    | Cost |
| GCP      | Yes       | $35+/mo | $100+/mo   | Enterprise |
| K8s      | Cluster cost | Variable | Variable | Control |

Choose based on your requirements for scale, features, and budget.