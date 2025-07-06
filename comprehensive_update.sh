#!/bin/bash
gcloud run services update congressional-data-api-v2 \
  --set-env-vars CONGRESS_API_KEY='NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG',SECRET_KEY='your-secret-key-here',DATABASE_URL='postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db' \
  --region us-central1 \
  --project chefgavin
