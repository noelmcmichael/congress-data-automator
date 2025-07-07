#!/usr/bin/env python3

"""
Simple Deploy - Quick deployment of updated API
"""

import subprocess
import time
import requests

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def deploy_api():
    """Simple deployment"""
    
    print("🚀 SIMPLE API DEPLOYMENT")
    print("=" * 60)
    
    # Build with a simple tag
    build_cmd = "cd /Users/noelmcmichael/Workspace/congress_data_automator/backend && docker build -t gcr.io/chefgavin/congress-api:phase2-urls ."
    if not run_command(build_cmd, "Building Docker image"):
        return False
    
    # Push to registry
    push_cmd = "docker push gcr.io/chefgavin/congress-api:phase2-urls"
    if not run_command(push_cmd, "Pushing to registry"):
        return False
    
    # Deploy with simpler command
    deploy_cmd = """
    gcloud run deploy congressional-data-api-v2 \
        --image gcr.io/chefgavin/congress-api:phase2-urls \
        --platform managed \
        --region us-central1 \
        --project chefgavin
    """
    
    if not run_command(deploy_cmd, "Deploying to Cloud Run"):
        return False
    
    print("\n⏳ Waiting for deployment to stabilize...")
    time.sleep(30)
    
    # Test the deployment
    try:
        response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/health", timeout=30)
        if response.status_code == 200:
            print("✅ Health check passed")
            
            # Test committees endpoint
            response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees", timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Committees endpoint working: {len(data)} committees")
                
                # Quick check for URL fields
                if data and len(data) > 0:
                    first_committee = data[0]
                    if 'hearings_url' in first_committee:
                        print("✅ URL fields are present in response")
                        return True
                    else:
                        print("⚠️ URL fields not present in response")
                        return False
                else:
                    print("⚠️ No committee data returned")
                    return False
            else:
                print(f"❌ Committees endpoint failed: {response.status_code}")
                return False
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Deployment test failed: {e}")
        return False

def main():
    """Main deployment"""
    
    if deploy_api():
        print("\n🎉 DEPLOYMENT SUCCESSFUL")
        print("=" * 60)
        print("✅ API deployed with URL fields")
        print("✅ All tests passed")
        print("🌐 Ready for frontend integration")
    else:
        print("\n❌ DEPLOYMENT FAILED")
        print("=" * 60)
        print("❌ Check logs for detailed error information")

if __name__ == "__main__":
    main()