#!/bin/bash

gcloud run services update congressional-data-api-v2 \
  --set-env-vars CONGRESS_API_KEY='NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG' \
  --region us-central1 \
  --project chefgavin

