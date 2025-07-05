# Deployment Guide

## Prerequisites

### GCP Project Setup
1. Enable billing for project `congressional-db-service`
2. Enable required APIs:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable sqladmin.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   gcloud services enable cloudscheduler.googleapis.com
   ```

### Required Secrets
Set up the following secrets in GCP Secret Manager:
- `congress-api-key`: Your Congress.gov API key
- `database-url`: PostgreSQL connection string
- `secret-key`: Application secret key
- `allowed-origins`: CORS allowed origins (JSON array)

## Infrastructure Setup

### 1. Cloud SQL Database
```bash
# Create PostgreSQL instance
gcloud sql instances create congress-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_SECURE_PASSWORD

# Create database
gcloud sql databases create congress_data \
  --instance=congress-db

# Create database user
gcloud sql users create congress_user \
  --instance=congress-db \
  --password=YOUR_USER_PASSWORD
```

### 2. Cloud Build Setup
```bash
# Create build trigger
gcloud builds triggers create github \
  --repo-name=congress-data-automator \
  --repo-owner=noelmcmichael \
  --branch-pattern="^main$" \
  --build-config=backend/cloudbuild.yaml
```

### 3. Cloud Run Deployment
```bash
# Deploy to Cloud Run
gcloud run deploy congress-api \
  --image gcr.io/congressional-db-service/congress-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --min-instances 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars="DEBUG=false,GCP_PROJECT_ID=congressional-db-service"
```

### 4. Cloud Scheduler Setup
```bash
# Create daily members update job
gcloud scheduler jobs create http members-update \
  --schedule="0 2 1 * *" \
  --uri="https://congress-api-[hash]-uc.a.run.app/api/v1/update/members" \
  --http-method=POST \
  --timezone="America/New_York" \
  --description="Update congressional members monthly"

# Create weekly committees update job
gcloud scheduler jobs create http committees-update \
  --schedule="0 2 * * 1" \
  --uri="https://congress-api-[hash]-uc.a.run.app/api/v1/update/committees" \
  --http-method=POST \
  --timezone="America/New_York" \
  --description="Update committees weekly"

# Create daily hearings update job
gcloud scheduler jobs create http hearings-update \
  --schedule="0 */6 * * *" \
  --uri="https://congress-api-[hash]-uc.a.run.app/api/v1/update/hearings" \
  --http-method=POST \
  --timezone="America/New_York" \
  --description="Update hearings every 6 hours"
```

## Alternative Deployment Options

### Docker Compose (Local Development)
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: congress_data
      POSTGRES_USER: congress_user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://congress_user:password@db:5432/congress_data
      CONGRESS_API_KEY: your_api_key_here
      SECRET_KEY: your_secret_key_here
      DEBUG: "true"
    depends_on:
      - db
    ports:
      - "8000:8000"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Heroku Deployment
```bash
# Create Heroku app
heroku create congress-data-automator

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set CONGRESS_API_KEY=your_api_key_here
heroku config:set SECRET_KEY=your_secret_key_here
heroku config:set DEBUG=false

# Deploy
git push heroku main
```

### Railway Deployment
1. Connect GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push to main

## Environment Variables

### Required
- `DATABASE_URL`: PostgreSQL connection string
- `CONGRESS_API_KEY`: Your Congress.gov API key
- `SECRET_KEY`: Application secret key (generate with `openssl rand -base64 32`)

### Optional
- `DEBUG`: Enable debug mode (default: false)
- `GCP_PROJECT_ID`: GCP project ID for Cloud services
- `REDIS_URL`: Redis connection string for caching
- `ALLOWED_ORIGINS`: CORS allowed origins (JSON array)
- `LOG_LEVEL`: Logging level (default: INFO)

## Database Migration

Once deployed, run database migrations:

```bash
# Using Cloud Run
gcloud run jobs create migrate-db \
  --image gcr.io/congressional-db-service/congress-api:latest \
  --command "python" \
  --args "-m","alembic","upgrade","head"

# Using Docker
docker run --rm \
  -e DATABASE_URL=your_database_url \
  gcr.io/congressional-db-service/congress-api:latest \
  python -m alembic upgrade head
```

## Monitoring and Logging

### Health Checks
- Application health: `GET /health`
- Database status: `GET /api/v1/stats/database`
- API status: `GET /api/v1/status`

### Logging
- Structured JSON logs via Cloud Logging
- Request tracing with correlation IDs
- Error tracking and alerting

### Monitoring
- API response times and error rates
- Database query performance
- Resource utilization (CPU, memory)
- Data freshness metrics

## Security Considerations

1. **API Keys**: Store in GCP Secret Manager
2. **Database**: Use IAM authentication where possible
3. **Network**: Restrict access to specific IP ranges
4. **SSL/TLS**: Enforce HTTPS for all endpoints
5. **Rate Limiting**: Implement API rate limiting
6. **Input Validation**: Validate all user inputs

## Scaling Considerations

1. **Database**: Use read replicas for read-heavy workloads
2. **API**: Configure auto-scaling based on CPU/memory
3. **Caching**: Implement Redis for frequently accessed data
4. **CDN**: Use Cloud CDN for static assets
5. **Background Jobs**: Use Cloud Tasks for heavy processing

## Cost Optimization

1. **Instances**: Use minimum required instance sizes
2. **Scheduling**: Scale down during low-traffic hours
3. **Storage**: Use lifecycle policies for old data
4. **Monitoring**: Set up billing alerts
5. **Cleanup**: Regular cleanup of unused resources

## Troubleshooting

### Common Issues

1. **Database Connection**: Check connection string and credentials
2. **API Limits**: Monitor Congress.gov API rate limits
3. **Memory Issues**: Increase Cloud Run memory allocation
4. **Timeout**: Increase timeout for long-running operations
5. **Permissions**: Verify IAM permissions for GCP services

### Debugging Commands

```bash
# Check application logs
gcloud logs read --project=congressional-db-service --limit=50

# Check service status
gcloud run services describe congress-api --region=us-central1

# Test API connectivity
curl -X GET https://your-service-url/health

# Check database connectivity
gcloud sql connect congress-db --user=congress_user
```

## Backup and Recovery

1. **Database**: Automated daily backups with 7-day retention
2. **Code**: Git repository with tagged releases
3. **Configuration**: Infrastructure as Code with Terraform
4. **Secrets**: Backup secret manager entries
5. **Monitoring**: Set up alerts for backup failures

## Performance Tuning

1. **Database**: Add indexes for frequently queried columns
2. **API**: Implement response caching
3. **Scraping**: Optimize request patterns and delays
4. **Memory**: Profile memory usage and optimize
5. **Network**: Use connection pooling and keep-alive