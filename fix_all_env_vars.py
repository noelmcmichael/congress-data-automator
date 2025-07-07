#!/usr/bin/env python3
"""
Fix the Cloud Run deployment by setting all required environment variables.
"""
import secrets
import subprocess
import sys
import os

def generate_secret_key():
    """Generate a secure secret key."""
    return secrets.token_urlsafe(32)

def update_cloud_run_service():
    """Update the Cloud Run service with all required environment variables."""
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    print("🔑 Generated secure secret key")
    print(f"📡 Updating Cloud Run service with all required environment variables...")
    
    # Update the Cloud Run service with all required environment variables
    cmd = [
        "/opt/homebrew/bin/gcloud", "run", "services", "update", "congressional-data-api-v3",
        "--region=us-central1",
        "--set-env-vars=CONGRESS_API_KEY=NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG,DATABASE_URL=postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db,ENVIRONMENT=production,SECRET_KEY=" + secret_key,
        "--quiet"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully updated Cloud Run service with all environment variables")
            print("🚀 Cloud Run service should now start properly")
            return True
        else:
            print(f"❌ Failed to update Cloud Run service: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error updating Cloud Run service: {e}")
        return False

def check_service_health():
    """Check if the service is now healthy."""
    import time
    import requests
    
    print("⏳ Waiting for service to start...")
    time.sleep(45)  # Wait for Cloud Run to deploy
    
    try:
        # Check the health endpoint
        response = requests.get(
            "https://congressional-data-api-v3-1066017671167.us-central1.run.app/health",
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Service is healthy!")
            print(f"📊 Health check response: {response.json()}")
            return True
        else:
            print(f"❌ Service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking service health: {e}")
        return False

def test_enhanced_api():
    """Test the enhanced API with URL fields."""
    import requests
    
    print("🧪 Testing enhanced API endpoints...")
    
    try:
        # Test committees endpoint
        response = requests.get(
            "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1/committees",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Committees endpoint working: {len(data)} committees found")
            
            # Check if URL fields are present
            if data and 'official_website_url' in data[0]:
                print("✅ URL fields are present in API response!")
                return True
            else:
                print("⚠️  URL fields not found in API response")
                return False
        else:
            print(f"❌ Committees endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing enhanced API: {e}")
        return False

def main():
    """Main function to fix the deployment."""
    print("🔧 Fixing Cloud Run deployment - Setting all required environment variables")
    print("=" * 70)
    
    # Step 1: Update Cloud Run service
    if not update_cloud_run_service():
        print("❌ Failed to update Cloud Run service")
        sys.exit(1)
    
    # Step 2: Check service health
    if not check_service_health():
        print("⚠️  Service updated but health check failed")
        print("📋 Check Cloud Run logs for additional issues")
        return
    
    # Step 3: Test enhanced API
    if test_enhanced_api():
        print("🎉 Cloud Run deployment fix complete!")
        print("✅ Phase 2 is now 100% complete!")
        print("🚀 Enhanced API with URL fields is working!")
    else:
        print("⚠️  Service is healthy but URL fields not working")
        print("📋 May need to check API schema implementation")

if __name__ == "__main__":
    main()