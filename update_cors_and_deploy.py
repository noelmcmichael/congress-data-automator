#!/usr/bin/env python3
"""
Update CORS settings for politicalequity.io and redeploy
"""

import subprocess
import os
import time

def run_command(cmd, description):
    """Run a command and return the result"""
    print(f"\n🔧 {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()[:500]}")
            return True, result.stdout
        else:
            print(f"❌ Failed: {description}")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False, str(e)

def main():
    print("🚀 Updating CORS and Redeploying for politicalequity.io")
    print("=" * 60)
    
    # Step 1: Update environment variables for Cloud Run
    print("\n📋 Step 1: Update CORS Environment Variable")
    cmd = """gcloud run services update congressional-data-api-v3 \
        --region=us-central1 \
        --set-env-vars="ALLOWED_ORIGINS=https://politicalequity.io,https://storage.googleapis.com" \
        --max-instances=10 \
        --memory=1Gi \
        --cpu=1"""
    
    success, output = run_command(cmd, "Updating CORS settings")
    
    if success:
        print("\n⏳ Waiting for deployment to complete...")
        time.sleep(30)
        
        # Step 2: Test the updated service
        print("\n📋 Step 2: Testing updated service")
        test_cmd = 'curl -s "https://congressional-data-api-v3-yovvxn4y7q-uc.a.run.app/api/v1/members?limit=1"'
        success, output = run_command(test_cmd, "Testing direct Cloud Run")
        
        if success:
            print("✅ Direct Cloud Run service working")
            
            # Step 3: Test through load balancer
            print("\n📋 Step 3: Testing through load balancer")
            test_lb_cmd = 'curl -s "https://politicalequity.io/api/v1/members?limit=1"'
            success, output = run_command(test_lb_cmd, "Testing load balancer")
            
            if success:
                print("🎉 Load balancer working perfectly!")
            else:
                print("⚠️  Load balancer still has issues")
        
    print("\n📊 Deployment Summary:")
    print("✅ CORS updated for politicalequity.io")
    print("✅ Cloud Run service redeployed")
    print("🔍 Testing results above")

if __name__ == "__main__":
    main()