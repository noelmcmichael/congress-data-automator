#!/bin/bash
# Deploy data quality improvements
set -e

echo "🚀 Deploying data quality improvements..."

# Build new container with SQL updates
echo "📦 Building container with SQL updates..."
docker build -t gcr.io/chefgavin/congress-api:data-quality-update .

# Push to registry
echo "📤 Pushing to registry..."
docker push gcr.io/chefgavin/congress-api:data-quality-update

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy congressional-data-api-v2 \
  --image gcr.io/chefgavin/congress-api:data-quality-update \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-cloudsql-instances=chefgavin:us-central1:congressional-db \
  --set-env-vars DATABASE_URL="postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db"

echo "✅ Deployment complete!"
