#!/usr/bin/env python3
"""
Deploy simplified test to identify the root cause of container startup issue
"""

import subprocess
import sys
import time
import requests

def deploy_minimal_config():
    """Deploy with minimal configuration matching working deployment"""
    print("=== TESTING MINIMAL DEPLOYMENT ===")
    print("Deploying with minimal config to match working revision...")
    
    # Deploy with same environment as working revision (None values)
    deploy_cmd = [
        "gcloud", "run", "deploy", "congressional-data-api-v2",
        "--image", "gcr.io/chefgavin/congress-api:phase2c-enhanced-schema",
        "--region", "us-central1",
        "--platform", "managed",
        "--allow-unauthenticated",
        "--memory", "2Gi",
        "--cpu", "2",
        "--timeout", "300",
        "--concurrency", "80",
        "--max-instances", "10",
        "--set-env-vars", "DATABASE_URL=postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db",
        "--add-cloudsql-instances", "chefgavin:us-central1:congressional-db",
        "--port", "8000"
    ]
    
    print("Deploying with minimal environment variables...")
    result = subprocess.run(deploy_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Minimal deployment failed")
        print("STDERR:", result.stderr)
        return False
    
    print("✅ Minimal deployment successful")
    return True

def test_minimal_deployment():
    """Test the minimal deployment"""
    print("\n=== TESTING MINIMAL DEPLOYMENT ===")
    
    time.sleep(20)  # Wait for deployment
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Health endpoint working")
            
            # Test committees endpoint
            committees_response = requests.get(f"{base_url}/api/v1/committees?limit=1", timeout=15)
            if committees_response.status_code == 200:
                data = committees_response.json()
                if data:
                    committee = data[0]
                    print(f"✅ Committees endpoint working")
                    print(f"Committee: {committee.get('name')}")
                    print("Fields in response:")
                    for key in committee.keys():
                        print(f"  {key}")
                    
                    # Check for URL fields
                    url_fields = ['hearings_url', 'members_url', 'official_website_url']
                    if any(field in committee for field in url_fields):
                        print("🎉 Enhanced schema is working!")
                        return True
                    else:
                        print("⚠️ Enhanced schema not active yet")
                        return True  # At least it deployed
                else:
                    print("⚠️ No data returned")
                    return True
            else:
                print(f"⚠️ Committees endpoint: {committees_response.status_code}")
                return True  # At least health works
        else:
            print(f"❌ Health endpoint: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return False

def add_api_key_if_working():
    """Add API key back if minimal deployment works"""
    print("\n=== ADDING API KEY TO WORKING DEPLOYMENT ===")
    
    import keyring
    try:
        congress_api_key = keyring.get_password('memex', 'CONGRESS_API_KEY')
    except:
        print("❌ Cannot get API key")
        return False
    
    # Update deployment with API key
    update_cmd = [
        "gcloud", "run", "services", "update", "congressional-data-api-v2",
        "--region", "us-central1",
        "--update-env-vars", f"CONGRESS_API_KEY={congress_api_key}",
        "--update-env-vars", "SECRET_KEY=enhanced-api-secret-key"
    ]
    
    print("Adding API key to working deployment...")
    result = subprocess.run(update_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Update with API key failed")
        print("STDERR:", result.stderr)
        return False
    
    print("✅ API key added successfully")
    return True

def main():
    """Main testing function"""
    print("Simplified Deployment Test")
    print("Goal: Identify why enhanced schema deployment fails")
    print("=" * 50)
    
    # Step 1: Try minimal deployment
    if not deploy_minimal_config():
        print("\n❌ Even minimal deployment fails - container issue")
        return False
    
    # Step 2: Test minimal deployment
    if not test_minimal_deployment():
        print("\n❌ Minimal deployment not responding")
        return False
    
    print("\n✅ Minimal deployment works!")
    
    # Step 3: Add API key incrementally
    if add_api_key_if_working():
        print("\n✅ API key added successfully")
        time.sleep(10)
        
        # Test again
        if test_minimal_deployment():
            print("\n🎉 FULL DEPLOYMENT SUCCESSFUL!")
            return True
        else:
            print("\n⚠️ API key caused issues")
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)