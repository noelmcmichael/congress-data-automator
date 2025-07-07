#!/usr/bin/env python3
"""
Script to fix the Congress.gov API key in production environment.
This script will update the Cloud Run service with the correct API key.
"""

import subprocess
import json
import os
import sys

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
        return result.stdout
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    """Main function to update the API key in production."""
    print("🔧 Fixing Congress.gov API Key in Production")
    print("=" * 50)
    
    # Step 1: Check current service configuration
    print("\n1. Checking current service configuration...")
    service_name = "congressional-data-api-v2"
    project_id = "chefgavin"
    region = "us-central1"
    
    # Get current service config
    get_service_cmd = f"gcloud run services describe {service_name} --region={region} --project={project_id} --format=json"
    service_config = run_command(get_service_cmd, "Get current service configuration")
    
    if not service_config:
        print("❌ Failed to get current service configuration")
        return False
    
    # Parse current config
    try:
        config = json.loads(service_config)
        current_env = config.get("spec", {}).get("template", {}).get("spec", {}).get("template", {}).get("spec", {}).get("containers", [{}])[0].get("env", [])
        
        print(f"Current environment variables:")
        for env_var in current_env:
            name = env_var.get("name", "")
            if "API_KEY" in name:
                print(f"  {name}: {'Set' if env_var.get('value') else 'Not Set'}")
        
    except Exception as e:
        print(f"Failed to parse service config: {e}")
    
    # Step 2: Update environment variables
    print("\n2. Updating environment variables...")
    
    # Update the service with the correct API key
    update_env_cmd = f"""gcloud run services update {service_name} \\
        --region={region} \\
        --project={project_id} \\
        --set-env-vars CONGRESS_API_KEY="{CONGRESS_API_KEY}" \\
        --quiet"""
    
    result = run_command(update_env_cmd, "Update service environment variables")
    
    if not result:
        print("❌ Failed to update environment variables")
        return False
    
    print("✅ Environment variables updated successfully")
    
    # Step 3: Wait for deployment
    print("\n3. Waiting for deployment to complete...")
    
    # Wait for the service to be ready
    wait_cmd = f"""gcloud run services describe {service_name} \\
        --region={region} \\
        --project={project_id} \\
        --format="value(status.conditions[0].status)" """
    
    import time
    max_wait = 120  # 2 minutes
    wait_time = 0
    
    while wait_time < max_wait:
        status = run_command(wait_cmd, "Check deployment status")
        if status and status.strip() == "True":
            print("✅ Service deployed successfully")
            break
        
        print(f"Waiting for deployment... ({wait_time}s)")
        time.sleep(10)
        wait_time += 10
    
    if wait_time >= max_wait:
        print("⚠️ Deployment taking longer than expected, but continuing...")
    
    # Step 4: Test the API key
    print("\n4. Testing the updated API key...")
    
    import requests
    import time
    
    # Wait a bit for the service to be fully ready
    print("Waiting 30 seconds for service to be ready...")
    time.sleep(30)
    
    # Test the API
    test_url = f"https://{service_name}-1066017671167.us-central1.run.app/api/v1/test/congress-api"
    
    try:
        response = requests.get(test_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✅ API key test successful!")
            print(f"Sample members count: {data.get('sample_members_count', 'Unknown')}")
            print(f"Rate limit remaining: {data.get('rate_limit_status', {}).get('remaining', 'Unknown')}")
        else:
            print(f"❌ API key test failed with status {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ API key test failed: {e}")
    
    # Step 5: Update the service URL for consistency
    print("\n5. Service Information:")
    service_url = f"https://{service_name}-1066017671167.us-central1.run.app"
    print(f"Service URL: {service_url}")
    print(f"API Status: {service_url}/api/v1/status")
    print(f"API Test: {service_url}/api/v1/test/congress-api")
    
    print("\n🎉 Production API key update complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)