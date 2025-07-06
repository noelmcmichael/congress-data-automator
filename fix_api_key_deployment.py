#!/usr/bin/env python3
"""
Fix API key deployment issue and redeploy the service.
"""
import subprocess
import sys
import os
import keyring

def get_api_key():
    """Get API key from keyring."""
    return keyring.get_password("memex", "CONGRESS_API_KEY")

def build_and_deploy():
    """Build and deploy the updated service."""
    
    # Get the API key
    api_key = get_api_key()
    if not api_key:
        raise ValueError("API key not found in keyring")
    
    print(f"✅ API Key retrieved: {api_key[:8]}...{api_key[-4:]}")
    
    # Build the Docker image
    print("📦 Building Docker image...")
    build_cmd = [
        "docker", "build", 
        "-t", "gcr.io/chefgavin/congress-api:api-fix",
        "-f", "backend/Dockerfile", 
        "backend/"
    ]
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Build failed: {result.stderr}")
        return False
    
    print("✅ Docker image built successfully")
    
    # Push the image
    print("🚀 Pushing Docker image...")
    push_cmd = ["docker", "push", "gcr.io/chefgavin/congress-api:api-fix"]
    result = subprocess.run(push_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Push failed: {result.stderr}")
        return False
    
    print("✅ Docker image pushed successfully")
    
    # Deploy to Cloud Run with explicit environment variables
    print("🌐 Deploying to Cloud Run...")
    deploy_cmd = [
        "gcloud", "run", "deploy", "congressional-data-api-v2",
        "--image", "gcr.io/chefgavin/congress-api:api-fix",
        "--platform", "managed",
        "--region", "us-central1",
        "--project", "chefgavin",
        "--add-cloudsql-instances", "chefgavin:us-central1:congressional-db",
        "--set-env-vars", f"CONGRESS_API_KEY={api_key}",
        "--set-env-vars", "SECRET_KEY=your-secret-key-here",
        "--set-env-vars", "DATABASE_URL=postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db",
        "--allow-unauthenticated"
    ]
    
    result = subprocess.run(deploy_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Deployment failed: {result.stderr}")
        return False
    
    print("✅ Service deployed successfully")
    print(f"Service URL: https://congressional-data-api-v2-1066017671167.us-central1.run.app")
    
    return True

if __name__ == "__main__":
    try:
        success = build_and_deploy()
        if success:
            print("\n🎉 API key fix deployment completed successfully!")
        else:
            print("\n❌ Deployment failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)