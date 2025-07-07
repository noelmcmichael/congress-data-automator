#!/usr/bin/env python3
"""
Update only the environment variables for the existing working service.
"""

import subprocess
import sys
import time

def main():
    """Main function to update environment variables."""
    print("🔧 Updating Environment Variables Only")
    print("=" * 50)
    
    # Get the current service configuration
    print("1. Getting current service configuration...")
    
    cmd = """gcloud run services describe congressional-data-api-v2 \\
        --region=us-central1 \\
        --project=chefgavin \\
        --format=json"""
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to get service config: {result.stderr}")
        return False
    
    print("✅ Retrieved current service configuration")
    
    # Update the service but keep the current image and only update env vars
    print("\n2. Updating environment variables only...")
    
    # Use the replace method to update the entire service config
    cmd = f"""gcloud run services replace-traffic congressional-data-api-v2 \\
        --to-revisions congressional-data-api-v2-00026-b2m=100 \\
        --region=us-central1 \\
        --project=chefgavin"""
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to update traffic: {result.stderr}")
        # Try a different approach - direct env var update
        print("\n3. Trying direct environment variable update...")
        
        cmd = f"""gcloud run services update congressional-data-api-v2 \\
            --region=us-central1 \\
            --project=chefgavin \\
            --update-env-vars CONGRESS_API_KEY=NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG \\
            --no-traffic"""
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to update env vars: {result.stderr}")
            return False
    
    print("✅ Service updated successfully")
    
    # Test the API key
    print("\n4. Testing API key...")
    
    import requests
    
    # Wait a bit for the service to be ready
    time.sleep(15)
    
    # Test the API
    try:
        response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/test/congress-api", timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API key test successful!")
            print(f"Sample members: {data.get('sample_members_count', 'Unknown')}")
            print(f"Rate limit: {data.get('rate_limit_status', {}).get('remaining', 'Unknown')}")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)