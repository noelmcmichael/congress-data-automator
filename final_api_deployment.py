#!/usr/bin/env python3

"""
Final API Deployment - Deploy working container with URL fields
"""

import subprocess
import time
import requests
import json

def build_and_deploy():
    """Build fresh container and deploy"""
    print("🚀 BUILDING FRESH CONTAINER")
    print("=" * 50)
    
    # Build with unique tag
    tag = f"phase2c-final-{int(time.time())}"
    print(f"Building with tag: {tag}")
    
    try:
        # Build container
        build_cmd = [
            "docker", "build", 
            "-t", f"gcr.io/chefgavin/congress-api:{tag}",
            "/Users/noelmcmichael/Workspace/congress_data_automator/backend"
        ]
        
        print("Building container...")
        build_result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if build_result.returncode != 0:
            print(f"❌ Build failed: {build_result.stderr}")
            return False
            
        print("✅ Container built successfully")
        
        # Push container
        push_cmd = ["docker", "push", f"gcr.io/chefgavin/congress-api:{tag}"]
        print("Pushing container...")
        push_result = subprocess.run(push_cmd, capture_output=True, text=True)
        
        if push_result.returncode != 0:
            print(f"❌ Push failed: {push_result.stderr}")
            return False
            
        print("✅ Container pushed successfully")
        
        # Deploy to Cloud Run
        deploy_cmd = [
            "gcloud", "run", "deploy", "congressional-data-api-v2",
            "--image", f"gcr.io/chefgavin/congress-api:{tag}",
            "--platform", "managed",
            "--region", "us-central1",
            "--project", "chefgavin",
            "--timeout", "300",
            "--memory", "1Gi",
            "--cpu", "1",
            "--max-instances", "10",
            "--allow-unauthenticated",
            "--update-env-vars", "DATABASE_URL=postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db",
            "--update-env-vars", "CONGRESS_API_KEY=NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG",
            "--update-env-vars", "SECRET_KEY=your-secret-key-here-for-jwt-tokens",
            "--update-env-vars", "DEBUG=false",
            "--quiet"
        ]
        
        print("Deploying to Cloud Run...")
        deploy_result = subprocess.run(deploy_cmd, capture_output=True, text=True)
        
        if deploy_result.returncode != 0:
            print(f"❌ Deploy failed: {deploy_result.stderr}")
            return False
            
        print("✅ Deployment successful")
        return True
        
    except Exception as e:
        print(f"❌ Build and deploy failed: {e}")
        return False

def wait_for_deployment():
    """Wait for deployment to be ready"""
    print("\n⏳ WAITING FOR DEPLOYMENT")
    print("=" * 50)
    
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    for i in range(30):  # Wait up to 150 seconds
        try:
            response = requests.get(f"{api_url}/health", timeout=10)
            if response.status_code == 200:
                print("✅ Deployment is ready!")
                return True
        except:
            pass
        
        print(f"   Waiting for deployment... ({i+1}/30)")
        time.sleep(5)
    
    print("❌ Deployment not ready after 150 seconds")
    return False

def test_url_fields():
    """Test if URL fields are working"""
    print("\n🔍 TESTING URL FIELDS")
    print("=" * 50)
    
    api_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Test committee endpoint
        response = requests.get(f"{api_url}/api/v1/committees/1", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Committee: {data.get('name', 'N/A')}")
            
            # Check for URL fields
            url_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
            has_url_fields = True
            
            for field in url_fields:
                if field in data:
                    print(f"✅ {field}: {data[field] if data[field] is not None else 'NULL'}")
                else:
                    print(f"❌ {field}: MISSING FROM RESPONSE")
                    has_url_fields = False
            
            if has_url_fields:
                print("\n🎉 SUCCESS: URL fields are now available in API!")
                return True
            else:
                print("\n❌ FAILURE: URL fields still missing")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ URL fields test failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 FINAL API DEPLOYMENT - URL FIELDS INTEGRATION")
    print("=" * 60)
    
    # Step 1: Build and deploy fresh container
    if not build_and_deploy():
        print("❌ BUILD AND DEPLOY FAILED")
        return False
    
    # Step 2: Wait for deployment to be ready
    if not wait_for_deployment():
        print("❌ DEPLOYMENT NOT READY")
        return False
    
    # Step 3: Test URL fields
    if not test_url_fields():
        print("❌ URL FIELDS NOT WORKING")
        return False
    
    print("\n🎉 DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print("✅ Fresh container built and deployed")
    print("✅ Service is ready and responding")
    print("✅ URL fields are working in API responses")
    print("✅ Phase 2C: API Enhancement - COMPLETE")
    print("✅ Phase 2: Official Committee URLs - 100% COMPLETE")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)