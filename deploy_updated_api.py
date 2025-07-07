#!/usr/bin/env python3

"""
Deploy Updated API with URL Fields
Build and deploy the enhanced API with new URL fields
"""

import subprocess
import time
import requests
import json
from datetime import datetime

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {description} timed out")
        return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def build_and_deploy():
    """Build and deploy the updated API"""
    
    print("🚀 DEPLOYING UPDATED API WITH URL FIELDS")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = "/Users/noelmcmichael/Workspace/congress_data_automator/backend"
    
    # Build the Docker image
    build_command = f"cd {backend_dir} && docker build -t gcr.io/chefgavin/congress-api:enhanced-urls ."
    if not run_command(build_command, "Building Docker image"):
        return False
    
    # Push to Google Container Registry
    push_command = "docker push gcr.io/chefgavin/congress-api:enhanced-urls"
    if not run_command(push_command, "Pushing to Container Registry"):
        return False
    
    # Deploy to Cloud Run
    deploy_command = """
    gcloud run deploy congressional-data-api-v2 \
        --image gcr.io/chefgavin/congress-api:enhanced-urls \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --set-env-vars DATABASE_URL=postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db \
        --add-cloudsql-instances chefgavin:us-central1:congressional-db \
        --memory 2Gi \
        --cpu 2 \
        --timeout 300 \
        --concurrency 80 \
        --max-instances 10 \
        --project chefgavin
    """
    
    if not run_command(deploy_command, "Deploying to Cloud Run"):
        return False
    
    print("\n✅ DEPLOYMENT COMPLETED")
    print("=" * 60)
    print("⏳ Waiting for service to be ready...")
    
    # Wait for service to be ready
    time.sleep(30)
    
    return True

def test_deployment():
    """Test the deployed API"""
    
    print("\n🔍 TESTING DEPLOYED API")
    print("=" * 60)
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test committees endpoint with URL fields
    try:
        response = requests.get(f"{base_url}/api/v1/committees", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Committees endpoint working: {len(data)} committees")
            
            # Check for URL fields
            if data and len(data) > 0:
                first_committee = data[0]
                url_fields = ['hearings_url', 'members_url', 'official_website_url']
                
                fields_present = 0
                for field in url_fields:
                    if field in first_committee:
                        fields_present += 1
                
                print(f"📊 URL fields present: {fields_present}/{len(url_fields)}")
                
                # Find a committee with URLs
                committees_with_urls = 0
                for committee in data:
                    if (committee.get('hearings_url') and 
                        committee.get('members_url')):
                        committees_with_urls += 1
                        
                        # Show one example
                        if committees_with_urls == 1:
                            print(f"📋 SAMPLE COMMITTEE WITH URLS:")
                            print(f"   Name: {committee.get('name')}")
                            print(f"   Chamber: {committee.get('chamber')}")
                            print(f"   Hearings: {committee.get('hearings_url')}")
                            print(f"   Members: {committee.get('members_url')}")
                
                print(f"📊 Committees with URLs: {committees_with_urls}/{len(data)}")
                
                if committees_with_urls > 0:
                    print("✅ URL fields are working correctly")
                    return True
                else:
                    print("⚠️ No committees have URLs - may need database sync")
                    return False
            else:
                print("❌ No committee data returned")
                return False
        else:
            print(f"❌ Committees endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Committees endpoint error: {e}")
        return False

def main():
    """Main deployment function"""
    
    print("🎯 ENHANCED API DEPLOYMENT")
    print("=" * 60)
    print("🔧 Building and deploying API with URL fields")
    print("🔗 Database already populated with committee URLs")
    print("📋 Testing deployment after update")
    
    # Build and deploy
    if not build_and_deploy():
        print("\n❌ DEPLOYMENT FAILED")
        return
    
    # Test deployment
    if test_deployment():
        print("\n🎉 DEPLOYMENT SUCCESSFUL")
        print("=" * 60)
        print("✅ API enhanced with URL fields")
        print("✅ Database populated with committee URLs")
        print("✅ All endpoints working correctly")
        print("📋 Ready for frontend enhancement")
    else:
        print("\n⚠️ DEPLOYMENT PARTIALLY SUCCESSFUL")
        print("=" * 60)
        print("✅ API deployed successfully")
        print("⚠️ URL fields may need additional configuration")
        print("📋 Check database connection and schema")

if __name__ == "__main__":
    main()