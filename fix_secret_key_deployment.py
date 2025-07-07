#!/usr/bin/env python3
"""
Fix the Cloud Run deployment by adding the missing SECRET_KEY environment variable.
"""
import secrets
import subprocess
import sys
import os

def generate_secret_key():
    """Generate a secure secret key."""
    return secrets.token_urlsafe(32)

def update_cloud_run_service():
    """Update the Cloud Run service with the SECRET_KEY environment variable."""
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    print("🔑 Generated secure secret key")
    print(f"📡 Updating Cloud Run service with SECRET_KEY...")
    
    # Update the Cloud Run service with the SECRET_KEY
    cmd = [
        "/opt/homebrew/bin/gcloud", "run", "services", "update", "congressional-data-api-v3",
        "--region=us-central1",
        f"--set-env-vars=SECRET_KEY={secret_key}",
        "--quiet"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully updated Cloud Run service with SECRET_KEY")
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
    time.sleep(30)  # Wait for Cloud Run to deploy
    
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

def main():
    """Main function to fix the deployment."""
    print("🔧 Fixing Cloud Run deployment - Adding SECRET_KEY environment variable")
    print("=" * 60)
    
    # Step 1: Update Cloud Run service
    if not update_cloud_run_service():
        print("❌ Failed to update Cloud Run service")
        sys.exit(1)
    
    # Step 2: Check service health
    if check_service_health():
        print("🎉 Cloud Run deployment fix complete!")
        print("✅ Phase 2 can now be completed")
    else:
        print("⚠️  Service updated but health check failed")
        print("📋 Check Cloud Run logs for additional issues")

if __name__ == "__main__":
    main()