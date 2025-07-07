#!/usr/bin/env python3
"""
Update the working service with enhanced schema instead of deploying new revision
"""

import subprocess
import sys
import time
import requests

def update_working_service():
    """Update the working service with new container image"""
    print("=== UPDATING WORKING SERVICE ===")
    print("Strategy: Update existing working service instead of creating new revision")
    
    # Update the working service with new image
    update_cmd = [
        "gcloud", "run", "services", "update", "congressional-data-api-v2",
        "--image", "gcr.io/chefgavin/congress-api:phase2c-enhanced-schema",
        "--region", "us-central1"
    ]
    
    print("Updating working service with enhanced schema image...")
    result = subprocess.run(update_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Service update failed")
        print("STDERR:", result.stderr)
        return False
    
    print("✅ Service updated successfully")
    print(result.stdout)
    return True

def test_updated_service():
    """Test the updated service"""
    print("\n=== TESTING UPDATED SERVICE ===")
    
    time.sleep(20)  # Wait for deployment
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Test health endpoint
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Health endpoint working")
            
            # Test committees endpoint for enhanced schema
            committees_response = requests.get(f"{base_url}/api/v1/committees?limit=1", timeout=15)
            if committees_response.status_code == 200:
                data = committees_response.json()
                if data:
                    committee = data[0]
                    print(f"✅ Committees endpoint working")
                    print(f"Committee: {committee.get('name')}")
                    
                    # Check for enhanced URL fields
                    url_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
                    url_fields_found = []
                    
                    print("Fields in response:")
                    for key, value in committee.items():
                        print(f"  {key}: {value}")
                        if key in url_fields:
                            url_fields_found.append(key)
                    
                    if len(url_fields_found) >= 3:
                        print("\n🎉 ENHANCED SCHEMA SUCCESSFULLY DEPLOYED!")
                        print(f"Found URL fields: {url_fields_found}")
                        return True
                    else:
                        print(f"\n⚠️ Enhanced schema not active")
                        print(f"Expected URL fields: {url_fields}")
                        print(f"Found URL fields: {url_fields_found}")
                        
                        # Check if we have the old website_url field
                        if 'website_url' in committee:
                            print("Still seeing old schema with website_url")
                        return False
                else:
                    print("⚠️ No committee data returned")
                    return False
            else:
                print(f"❌ Committees endpoint: {committees_response.status_code}")
                print(f"Response: {committees_response.text}")
                return False
        else:
            print(f"❌ Health endpoint: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return False

def rollback_if_failed():
    """Rollback to previous working image if update fails"""
    print("\n=== ROLLING BACK TO WORKING IMAGE ===")
    
    # Rollback to previous working image
    rollback_cmd = [
        "gcloud", "run", "services", "update", "congressional-data-api-v2",
        "--image", "gcr.io/chefgavin/congress-api@sha256:c3e3a3885a7a38e062d7a77057d0ef5844794566b76e772d69afbb0e8f687683",
        "--region", "us-central1"
    ]
    
    print("Rolling back to previous working image...")
    result = subprocess.run(rollback_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Rollback failed")
        print("STDERR:", result.stderr)
        return False
    
    print("✅ Rollback successful")
    return True

def main():
    """Main update function"""
    print("Service Update Strategy for Enhanced Schema")
    print("Goal: Update working service instead of new deployment")
    print("=" * 50)
    
    # Step 1: Update working service
    if not update_working_service():
        print("\n❌ UPDATE FAILED")
        return False
    
    # Step 2: Test updated service
    if test_updated_service():
        print("\n🎉 UPDATE SUCCESSFUL!")
        print("Enhanced schema with URL fields is now live!")
        return True
    else:
        print("\n⚠️ UPDATE PARTIALLY SUCCESSFUL")
        print("Service updated but enhanced schema not active")
        
        # Ask if should rollback
        print("\nShould we rollback to previous working version? (y/n)")
        try:
            response = input().lower()
            if response == 'y':
                if rollback_if_failed():
                    print("✅ Rollback successful - service restored")
                else:
                    print("❌ Rollback failed")
                return False
            else:
                print("Keeping current deployment for troubleshooting")
                return False
        except:
            print("Keeping current deployment")
            return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Phase 2C API Enhancement: COMPLETED")
        print("Enhanced schema with URL fields successfully deployed")
    else:
        print("\n⚠️ Phase 2C needs further troubleshooting")
    
    sys.exit(0 if success else 1)