#!/usr/bin/env python3
"""
Script to build and deploy the fixed Congressional API with correct architecture support.
"""

import subprocess
import json
import os
import sys
import time

# The working Congress.gov API key
CONGRESS_API_KEY = "NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG"

def run_command(command, description):
    """Run a shell command and return the result."""
    print(f"Running: {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        print(f"Output: {result.stdout}")
        return result.stdout
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    """Main function to build and deploy the fixed API."""
    print("🚀 Building and Deploying Fixed Congressional API")
    print("=" * 50)
    
    project_id = "chefgavin"
    service_name = "congressional-data-api-v2"
    region = "us-central1"
    image_name = "gcr.io/chefgavin/congress-api"
    tag = "phase2-fix"
    
    # Step 1: Build Docker image with correct architecture
    print("\n1. Building Docker image with correct architecture...")
    
    # Build for amd64 architecture explicitly
    build_cmd = f"""docker buildx build --platform linux/amd64 \\
        -t {image_name}:{tag} \\
        -f backend/Dockerfile \\
        backend/"""
    
    result = run_command(build_cmd, "Build Docker image for amd64")
    
    if not result:
        print("❌ Failed to build Docker image")
        return False
    
    print("✅ Docker image built successfully")
    
    # Step 2: Push Docker image to Google Container Registry
    print("\n2. Pushing Docker image to GCR...")
    
    # Configure Docker to use gcloud as credential helper
    config_cmd = "gcloud auth configure-docker"
    run_command(config_cmd, "Configure Docker authentication")
    
    # Push the image
    push_cmd = f"docker push {image_name}:{tag}"
    result = run_command(push_cmd, "Push Docker image to GCR")
    
    if not result:
        print("❌ Failed to push Docker image")
        return False
    
    print("✅ Docker image pushed successfully")
    
    # Step 3: Deploy to Cloud Run with updated environment variables
    print("\n3. Deploying to Cloud Run with API key...")
    
    # Deploy the service
    deploy_cmd = f"""gcloud run deploy {service_name} \\
        --image={image_name}:{tag} \\
        --platform=managed \\
        --region={region} \\
        --project={project_id} \\
        --set-env-vars CONGRESS_API_KEY="{CONGRESS_API_KEY}" \\
        --set-env-vars DATABASE_URL="postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db" \\
        --set-env-vars ENVIRONMENT="production" \\
        --add-cloudsql-instances=chefgavin:us-central1:congressional-db \\
        --memory=2Gi \\
        --cpu=1 \\
        --allow-unauthenticated \\
        --max-instances=10 \\
        --quiet"""
    
    result = run_command(deploy_cmd, "Deploy service to Cloud Run")
    
    if not result:
        print("❌ Failed to deploy service")
        return False
    
    print("✅ Service deployed successfully")
    
    # Step 4: Wait for deployment to be ready
    print("\n4. Waiting for deployment to be ready...")
    
    max_wait = 120  # 2 minutes
    wait_time = 0
    
    while wait_time < max_wait:
        # Check health endpoint
        health_cmd = f"curl -s https://{service_name}-1066017671167.us-central1.run.app/health || echo 'not ready'"
        health_result = run_command(health_cmd, "Check service health")
        
        if health_result and '"status": "healthy"' in health_result:
            print("✅ Service is healthy and ready")
            break
        
        print(f"Waiting for service to be ready... ({wait_time}s)")
        time.sleep(10)
        wait_time += 10
    
    if wait_time >= max_wait:
        print("⚠️ Service taking longer than expected, but continuing...")
    
    # Step 5: Test the API key
    print("\n5. Testing the Congress.gov API integration...")
    
    import requests
    
    # Test the API
    test_url = f"https://{service_name}-1066017671167.us-central1.run.app/api/v1/test/congress-api"
    
    try:
        print(f"Testing API at: {test_url}")
        response = requests.get(test_url, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API key test successful!")
            print(f"Sample members count: {data.get('sample_members_count', 'Unknown')}")
            print(f"Rate limit remaining: {data.get('rate_limit_status', {}).get('remaining', 'Unknown')}")
            print(f"API connection: {data.get('api_connection', 'Unknown')}")
            
            # Also test the status endpoint
            status_url = f"https://{service_name}-1066017671167.us-central1.run.app/api/v1/status"
            status_response = requests.get(status_url, timeout=30)
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"✅ Status endpoint working: {status_data.get('api_status', 'Unknown')}")
            
        else:
            print(f"❌ API key test failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False
    
    # Step 6: Summary
    print("\n6. Deployment Summary:")
    service_url = f"https://{service_name}-1066017671167.us-central1.run.app"
    print(f"✅ Service URL: {service_url}")
    print(f"✅ API Status: {service_url}/api/v1/status")
    print(f"✅ API Test: {service_url}/api/v1/test/congress-api")
    print(f"✅ Members API: {service_url}/api/v1/members")
    
    print("\n🎉 Phase 2 Step 1 Complete: API Key Fixed!")
    print("Ready to proceed with full data collection...")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)