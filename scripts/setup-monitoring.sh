#!/bin/bash
# Setup monitoring and alerting for Congressional Data Service

set -e

PROJECT_ID="chefgavin"
SERVICE_NAME="congressional-data-api"
REGION="us-central1"

echo "Setting up monitoring for Congressional Data Service..."

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable monitoring.googleapis.com --project=$PROJECT_ID
gcloud services enable logging.googleapis.com --project=$PROJECT_ID

# Create uptime check for service health
echo "Creating uptime check..."
gcloud monitoring uptime create "Congressional Data API Health Check" \
  --resource-type=uptime-url \
  --resource-labels=host=congressional-data-api-1066017671167.us-central1.run.app,project_id=$PROJECT_ID \
  --path="/health" \
  --port=443 \
  --protocol=https \
  --period=5 \
  --timeout=10 \
  --project=$PROJECT_ID

# Create log-based metric for errors
echo "Creating log-based metrics..."
gcloud logging metrics create congressional_api_errors \
  --description="Count of API errors" \
  --log-filter='resource.type="cloud_run_revision" AND resource.labels.service_name="congressional-data-api" AND severity>=ERROR' \
  --project=$PROJECT_ID

# Create alerting policy for high error rate
echo "Creating alerting policies..."
cat > /tmp/error-alert-policy.json << EOF
{
  "displayName": "Congressional API High Error Rate",
  "documentation": {
    "content": "The Congressional Data API is experiencing a high error rate. Check logs and service health.",
    "mimeType": "text/markdown"
  },
  "conditions": [
    {
      "displayName": "Error rate condition",
      "conditionThreshold": {
        "filter": "metric.type=\"logging.googleapis.com/user/congressional_api_errors\" resource.type=\"cloud_run_revision\"",
        "comparison": "COMPARISON_GREATER_THAN",
        "thresholdValue": 5,
        "duration": "300s",
        "aggregations": [
          {
            "alignmentPeriod": "300s",
            "perSeriesAligner": "ALIGN_RATE"
          }
        ]
      }
    }
  ],
  "enabled": true,
  "alertStrategy": {
    "autoClose": "1800s"
  }
}
EOF

gcloud alpha monitoring policies create --policy-from-file=/tmp/error-alert-policy.json --project=$PROJECT_ID

echo "Monitoring setup complete!"
echo "View monitoring dashboard: https://console.cloud.google.com/monitoring/dashboards?project=$PROJECT_ID"
echo "View logs: https://console.cloud.google.com/logs/query?project=$PROJECT_ID"

# Cleanup
rm /tmp/error-alert-policy.json