#!/usr/bin/env python3
"""
Complete API Connection for politicalequity.io
Connect Cloud Run service to Load Balancer via Network Endpoint Group
"""

import subprocess
import json
import time
import requests

def run_command(cmd, description):
    """Run a gcloud command and return the result"""
    print(f"\n🔧 {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True, result.stdout
        else:
            print(f"❌ Failed: {description}")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {description}")
        return False, "Command timed out"
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False, str(e)

def test_endpoint(url, description):
    """Test an HTTP endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ {description} - Working!")
            return True
        else:
            print(f"❌ {description} - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"💥 {description} - Error: {e}")
        return False

def main():
    print("🚀 Complete API Connection for politicalequity.io")
    print("=" * 60)
    
    # Step 1: Create Network Endpoint Group for Cloud Run
    print("\n📋 Step 1: Create Network Endpoint Group")
    cmd = """gcloud compute network-endpoint-groups create congressional-api-neg \
        --region=us-central1 \
        --network-endpoint-type=serverless \
        --cloud-run-service=congressional-data-api-v3"""
    
    success, output = run_command(cmd, "Creating Network Endpoint Group")
    if not success and "already exists" not in output:
        print("Failed to create NEG. Exiting.")
        return False
    
    # Step 2: Add NEG as backend to the backend service
    print("\n📋 Step 2: Connect NEG to Backend Service")
    cmd = """gcloud compute backend-services add-backend api-backend-service \
        --global \
        --network-endpoint-group=congressional-api-neg \
        --network-endpoint-group-region=us-central1"""
    
    success, output = run_command(cmd, "Adding NEG to backend service")
    if not success:
        print("Failed to add NEG to backend service. Continuing to test...")
    
    # Step 3: Wait for propagation
    print("\n⏳ Step 3: Waiting for changes to propagate...")
    time.sleep(30)
    
    # Step 4: Test the connection
    print("\n📋 Step 4: Testing API Connection")
    
    # Test Cloud Run directly
    test_endpoint(
        "https://congressional-data-api-v3-yovvxn4y7q-uc.a.run.app/api/v1/status",
        "Direct Cloud Run API"
    )
    
    # Test through load balancer
    test_endpoint(
        "https://politicalequity.io/api/v1/status",
        "Load Balancer API"
    )
    
    # Test frontend
    test_endpoint(
        "https://politicalequity.io",
        "Frontend"
    )
    
    print("\n📋 Step 5: Configuration Summary")
    
    # Show backend service status
    cmd = "gcloud compute backend-services describe api-backend-service --global --format='value(backends[].group)'"
    success, output = run_command(cmd, "Checking backend service configuration")
    
    if success and output.strip():
        print("✅ Backend service has NEG connected")
    else:
        print("❌ Backend service missing NEG connection")
    
    print("\n🎉 API Connection Setup Complete!")
    print("\n📊 Final Status Check:")
    print("Frontend: https://politicalequity.io")
    print("API: https://politicalequity.io/api/v1/status")
    print("\nIf API is still returning 503, wait 2-3 minutes for full propagation.")

if __name__ == "__main__":
    main()