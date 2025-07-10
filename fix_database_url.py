#!/usr/bin/env python3
"""
Fix the DATABASE_URL for Cloud Run deployment
"""

import subprocess
import json

def fix_database_url():
    """Fix the DATABASE_URL environment variable for Cloud Run"""
    
    # Correct DATABASE_URL for Cloud SQL
    correct_database_url = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db"
    
    services = [
        "congressional-data-api-v3",
        "congressional-data-api"
    ]
    
    for service in services:
        try:
            print(f"Fixing {service}...")
            
            # Update the service with correct DATABASE_URL
            cmd = [
                "gcloud", "run", "services", "update", service,
                "--region", "us-central1",
                "--project", "chefgavin",
                "--set-env-vars", f"DATABASE_URL={correct_database_url}",
                "--quiet"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {service} updated successfully")
            else:
                print(f"❌ {service} update failed: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error updating {service}: {e}")

def verify_fix():
    """Verify the fix worked"""
    import time
    
    print("Waiting for deployment to complete...")
    time.sleep(10)
    
    import requests
    
    # Test the committees endpoint
    try:
        response = requests.get("https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1/committees?limit=5", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Committees endpoint fixed! Returned {len(data)} committees")
            if data:
                print(f"First committee: {data[0]['name']} ({data[0]['chamber']})")
            return True
        else:
            print(f"❌ Committees endpoint still failing: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing committees endpoint: {e}")
        return False

def main():
    """Fix the database URL and verify"""
    print("=== Fixing Database URL in Cloud Run ===")
    print()
    
    print("1. Updating DATABASE_URL environment variable...")
    fix_database_url()
    print()
    
    print("2. Verifying fix...")
    success = verify_fix()
    print()
    
    if success:
        print("🎉 DATABASE_URL fix successful!")
        print("The committees endpoint should now work correctly.")
    else:
        print("⚠️  Fix may not have worked completely.")
        print("Check Cloud Run logs for more details.")

if __name__ == "__main__":
    main()