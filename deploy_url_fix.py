#!/usr/bin/env python3

"""
Deploy URL Fix
Simple deployment script to update the API with URL fields
"""

import subprocess
import time
import requests
import json

def get_current_config():
    """Get current Cloud Run configuration"""
    try:
        cmd = [
            "gcloud", "run", "services", "describe", "congressional-data-api-v2",
            "--region", "us-central1", 
            "--project", "chefgavin",
            "--format", "json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            config = json.loads(result.stdout)
            return config
        else:
            print(f"Failed to get config: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error getting config: {e}")
        return None

def deploy_with_existing_config():
    """Deploy using existing working configuration"""
    print("🚀 DEPLOYING URL FIX")
    print("=" * 50)
    
    # Get current config
    config = get_current_config()
    if not config:
        print("❌ Cannot get current configuration")
        return False
    
    # Extract environment variables
    env_vars = {}
    try:
        containers = config.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        if containers:
            env_list = containers[0].get('env', [])
            for env in env_list:
                env_vars[env['name']] = env['value']
    except Exception as e:
        print(f"Error extracting env vars: {e}")
        return False
    
    print(f"Found {len(env_vars)} environment variables")
    
    # Build deployment command
    cmd = [
        "gcloud", "run", "deploy", "congressional-data-api-v2",
        "--image", "gcr.io/chefgavin/congress-api:phase2c-url-fix",
        "--platform", "managed",
        "--region", "us-central1",
        "--project", "chefgavin",
        "--timeout", "300",
        "--memory", "1Gi",
        "--cpu", "1",
        "--max-instances", "10",
        "--allow-unauthenticated",
        "--quiet"
    ]
    
    # Add environment variables
    for key, value in env_vars.items():
        cmd.extend(["--set-env-vars", f"{key}={value}"])
    
    print("🔧 Deploying with environment variables...")
    print(f"Command: {' '.join(cmd[:8])}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print(result.stdout)
            return True
        else:
            print("❌ Deployment failed!")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Deployment timed out")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def wait_for_deployment():
    """Wait for deployment to be ready"""
    print("⏳ Waiting for deployment to be ready...")
    
    for i in range(30):
        try:
            response = requests.get(
                "https://congressional-data-api-v2-1066017671167.us-central1.run.app/health",
                timeout=5
            )
            if response.status_code == 200:
                print("✅ Deployment is ready!")
                return True
        except:
            pass
        
        print(f"   Waiting... ({i+1}/30)")
        time.sleep(5)
    
    print("❌ Deployment not ready after 150 seconds")
    return False

def test_url_fields():
    """Test if URL fields are working"""
    print("🔍 TESTING URL FIELDS")
    print("=" * 50)
    
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/1"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API accessible")
            print(f"Committee: {data.get('name', 'N/A')}")
            
            # Check URL fields
            has_hearings = data.get('hearings_url') is not None
            has_members = data.get('members_url') is not None
            has_official = data.get('official_website_url') is not None
            
            print(f"Hearings URL: {'✅' if has_hearings else '❌'} {data.get('hearings_url', 'Missing')}")
            print(f"Members URL: {'✅' if has_members else '❌'} {data.get('members_url', 'Missing')}")
            print(f"Official URL: {'✅' if has_official else '❌'} {data.get('official_website_url', 'Missing')}")
            
            success = has_hearings and has_members and has_official
            
            if success:
                print("\n🎉 SUCCESS: URL fields are working!")
                return True
            else:
                print("\n❌ FAILURE: URL fields missing")
                return False
        else:
            print(f"❌ API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 CONGRESSIONAL DATA API - URL FIELDS DEPLOYMENT")
    print("=" * 60)
    
    # Step 1: Deploy
    if not deploy_with_existing_config():
        print("❌ DEPLOYMENT FAILED")
        return False
    
    # Step 2: Wait for readiness
    if not wait_for_deployment():
        print("❌ DEPLOYMENT NOT READY")
        return False
    
    # Step 3: Test URL fields
    if not test_url_fields():
        print("❌ URL FIELDS NOT WORKING")
        return False
    
    print("\n🎉 DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print("✅ Container deployed successfully")
    print("✅ Service is ready")
    print("✅ URL fields are working")
    print("✅ Phase 2C: API Enhancement - COMPLETE")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)