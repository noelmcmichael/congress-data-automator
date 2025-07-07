#!/usr/bin/env python3
"""
Deploy enhanced API with URL fields to Cloud Run
"""

import subprocess
import sys
import time
import requests
import keyring

def get_congress_api_key():
    """Get Congress API key from secrets"""
    try:
        congress_api_key = keyring.get_password('memex', 'CONGRESS_API_KEY')
        return congress_api_key
    except Exception as e:
        print(f"Error getting Congress API key: {e}")
        return None

def build_and_push_container():
    """Build and push container to GCR"""
    print("=== STEP 5: BUILD AND PUSH CONTAINER ===")
    
    # Build container
    build_cmd = [
        "docker", "build",
        "-t", "gcr.io/chefgavin/congress-api:phase2c-enhanced-schema",
        "-f", "backend/Dockerfile",
        "backend/"
    ]
    
    print(f"Building container: {' '.join(build_cmd)}")
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Container build failed")
        print("STDERR:", result.stderr)
        return False
    
    print("✅ Container built successfully")
    
    # Push container
    push_cmd = [
        "docker", "push", "gcr.io/chefgavin/congress-api:phase2c-enhanced-schema"
    ]
    
    print(f"Pushing container: {' '.join(push_cmd)}")
    result = subprocess.run(push_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Container push failed")
        print("STDERR:", result.stderr)
        return False
    
    print("✅ Container pushed successfully")
    return True

def deploy_to_cloud_run():
    """Deploy container to Cloud Run"""
    print("\n=== STEP 6: DEPLOY TO CLOUD RUN ===")
    
    congress_api_key = get_congress_api_key()
    if not congress_api_key:
        print("❌ Cannot get Congress API key")
        return False
    
    # Deploy with minimal environment variables (matching working deployment)
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
        "--set-env-vars", f"DATABASE_URL=postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db",
        "--set-env-vars", f"CONGRESS_API_KEY={congress_api_key}",
        "--set-env-vars", "SECRET_KEY=enhanced-api-secret-key-2025",
        "--add-cloudsql-instances", "chefgavin:us-central1:congressional-db",
        "--port", "8000"
    ]
    
    print(f"Deploying to Cloud Run...")
    print("Command: gcloud run deploy congressional-data-api-v2 [with environment variables]")
    
    result = subprocess.run(deploy_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Cloud Run deployment failed")
        print("STDERR:", result.stderr)
        print("STDOUT:", result.stdout)
        return False
    
    print("✅ Cloud Run deployment successful")
    print(result.stdout)
    return True

def test_enhanced_api():
    """Test that the enhanced API is working with URL fields"""
    print("\n=== STEP 7: TEST ENHANCED API ===")
    
    # Wait for deployment to be ready
    print("Waiting for deployment to be ready...")
    time.sleep(30)
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Test health endpoint
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"⚠️ Health endpoint returned: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False
    
    # Test committees endpoint for URL fields
    try:
        committees_response = requests.get(f"{base_url}/api/v1/committees?limit=1", timeout=15)
        if committees_response.status_code == 200:
            data = committees_response.json()
            if data:
                committee = data[0]
                print(f"✅ Committees endpoint working")
                print(f"Committee: {committee.get('name')}")
                
                # Check for URL fields
                url_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
                url_fields_found = []
                for field in url_fields:
                    if field in committee:
                        url_fields_found.append(field)
                        print(f"  ✅ {field}: {committee[field]}")
                    else:
                        print(f"  ❌ {field}: MISSING")
                
                if len(url_fields_found) >= 3:  # At least 3 of 4 URL fields
                    print("🎉 Enhanced schema with URL fields successfully deployed!")
                    return True
                else:
                    print("⚠️ URL fields still missing - enhanced schema not active")
                    return False
            else:
                print("⚠️ No committee data returned")
                return False
        else:
            print(f"❌ Committees endpoint returned: {committees_response.status_code}")
            print(f"Response: {committees_response.text}")
            return False
    except Exception as e:
        print(f"❌ Committees endpoint test failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("Enhanced API Deployment for Congressional Data Platform")
    print("Goal: Deploy enhanced schema with URL fields")
    print("=" * 50)
    
    # Step 5: Build and push container
    if not build_and_push_container():
        print("\n❌ DEPLOYMENT FAILED - Container build/push issue")
        return False
    
    # Step 6: Deploy to Cloud Run
    if not deploy_to_cloud_run():
        print("\n❌ DEPLOYMENT FAILED - Cloud Run deployment issue")
        return False
    
    # Step 7: Test enhanced API
    if not test_enhanced_api():
        print("\n⚠️ DEPLOYMENT PARTIAL - API deployed but URL fields not working")
        return False
    
    print("\n🎉 DEPLOYMENT SUCCESSFUL!")
    print("Enhanced API with URL fields is now live in production")
    print("URL: https://congressional-data-api-v2-1066017671167.us-central1.run.app")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Phase 2C API Enhancement: COMPLETED")
        print("Ready to proceed with frontend integration")
    else:
        print("\n❌ Deployment failed - troubleshooting required")
    
    sys.exit(0 if success else 1)