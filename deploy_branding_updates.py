#!/usr/bin/env python3
"""
Deploy frontend branding updates to production.
"""
import subprocess
import sys
import json
import time
from datetime import datetime

def run_command(cmd, description):
    """Run a command and return the result."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def deploy_frontend():
    """Deploy the updated frontend to Google Cloud Storage."""
    
    print("🚀 Starting Frontend Branding Deployment")
    print("=" * 50)
    
    # Step 1: Build the frontend
    build_result = run_command(
        "cd frontend && npm run build",
        "Building frontend with new branding"
    )
    
    if build_result is None:
        print("❌ Frontend build failed. Aborting deployment.")
        return False
    
    # Step 2: Deploy to Google Cloud Storage
    deploy_result = run_command(
        "cd frontend && gsutil -m rsync -r -d build/ gs://congressional-data-frontend/",
        "Deploying to Google Cloud Storage"
    )
    
    if deploy_result is None:
        print("❌ Frontend deployment failed.")
        return False
    
    # Step 3: Set proper cache headers for the new favicon
    cache_result = run_command(
        "gsutil -m setmeta -h 'Cache-Control:public, max-age=3600' gs://congressional-data-frontend/favicon.ico",
        "Setting cache headers for favicon"
    )
    
    # Step 4: Verify deployment
    verify_result = run_command(
        "curl -s -I https://storage.googleapis.com/congressional-data-frontend/index.html | head -5",
        "Verifying deployment"
    )
    
    if verify_result:
        print("📊 Deployment Verification:")
        print(verify_result)
    
    # Step 5: Test favicon specifically
    favicon_test = run_command(
        "curl -s -I https://storage.googleapis.com/congressional-data-frontend/favicon.ico | head -3",
        "Testing favicon deployment"
    )
    
    if favicon_test:
        print("🖼️ Favicon Status:")
        print(favicon_test)
    
    return True

def main():
    """Main deployment function."""
    
    deployment_summary = {
        "timestamp": datetime.now().isoformat(),
        "deployment_type": "frontend_branding_update",
        "changes": [
            "Custom polequity-ico.png favicon",
            "Updated HTML title: 'Political Equity - Congressional Data'",
            "Enhanced meta description",
            "Brand-consistent touch icons"
        ]
    }
    
    print("🎨 Congressional Data Automator - Branding Deployment")
    print(f"📅 Started: {deployment_summary['timestamp']}")
    print()
    
    success = deploy_frontend()
    
    if success:
        print()
        print("✅ BRANDING DEPLOYMENT SUCCESSFUL!")
        print("=" * 50)
        print("🌐 Frontend URL: https://storage.googleapis.com/congressional-data-frontend/index.html")
        print("🖼️ New favicon should be visible in browser tabs")
        print("📱 Touch icons updated for mobile devices")
        print()
        print("🔍 Verification Steps:")
        print("1. Open the frontend URL in a new browser tab")
        print("2. Check that the browser tab shows the polequity icon")
        print("3. Check that the title shows 'Political Equity - Congressional Data'")
        print("4. Test on mobile devices for touch icon consistency")
        
        deployment_summary["status"] = "success"
        deployment_summary["frontend_url"] = "https://storage.googleapis.com/congressional-data-frontend/index.html"
        
    else:
        print()
        print("❌ BRANDING DEPLOYMENT FAILED!")
        print("Check the error messages above for details.")
        deployment_summary["status"] = "failed"
    
    # Save deployment summary
    with open(f"branding_deployment_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(deployment_summary, f, indent=2)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)