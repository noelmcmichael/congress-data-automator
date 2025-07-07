#!/usr/bin/env python3

"""
Troubleshoot API Deployment Issues
Try different approaches to get the API working with URL fields
"""

import requests
import json
import time

def check_current_api_status():
    """Check what the current API is returning"""
    
    print("🔍 CHECKING CURRENT API STATUS")
    print("=" * 60)
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        # Check health
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health endpoint: {response.status_code}")
        
        # Check committees endpoint
        response = requests.get(f"{base_url}/api/v1/committees?limit=1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                first_committee = data[0]
                print(f"\nFirst committee: {first_committee.get('name')}")
                print(f"Available fields:")
                for key in sorted(first_committee.keys()):
                    value = first_committee[key]
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:50] + "..."
                    print(f"  {key}: {value}")
                
                # Check specifically for URL fields
                url_fields = ['hearings_url', 'members_url', 'official_website_url', 'last_url_update']
                missing_fields = [field for field in url_fields if field not in first_committee]
                
                if missing_fields:
                    print(f"\n❌ Missing URL fields: {missing_fields}")
                    return False
                else:
                    print(f"\n✅ All URL fields present!")
                    return True
            else:
                print("❌ No committee data returned")
                return False
        else:
            print(f"❌ Committees endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API check failed: {e}")
        return False

def try_alternative_approach():
    """Try different approaches to get URL fields working"""
    
    print("\n🔧 TRYING ALTERNATIVE APPROACHES")
    print("=" * 60)
    
    # Approach 1: Check if there's a different endpoint that might work
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Try getting a specific committee by ID
    try:
        response = requests.get(f"{base_url}/api/v1/committees/1", timeout=10)
        if response.status_code == 200:
            committee = response.json()
            print(f"✅ Specific committee endpoint works")
            print(f"Committee: {committee.get('name')}")
            
            # Check for URL fields
            url_fields = ['hearings_url', 'members_url', 'official_website_url']
            for field in url_fields:
                if field in committee:
                    print(f"  {field}: {committee[field]}")
                else:
                    print(f"  {field}: ❌ Missing")
        else:
            print(f"❌ Specific committee endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Specific committee test failed: {e}")

def check_deployment_logs():
    """Check deployment logs for specific errors"""
    
    print("\n📋 DEPLOYMENT TROUBLESHOOTING SUGGESTIONS")
    print("=" * 60)
    print("Based on the deployment failures, here are potential issues:")
    print("")
    print("1. 🔧 DATABASE CONNECTION:")
    print("   - The new model fields may be causing connection issues")
    print("   - Cloud SQL proxy configuration might need updating")
    print("")
    print("2. 🔧 MODEL SYNCHRONIZATION:")
    print("   - SQLAlchemy models updated but database tables already exist")
    print("   - May need to explicitly handle schema changes")
    print("")
    print("3. 🔧 CONTAINER STARTUP:")
    print("   - Timeout during startup due to database validation")
    print("   - Health check failing before service is ready")
    print("")
    print("4. 🔧 SUGGESTED FIXES:")
    print("   - Try deploying without model changes first")
    print("   - Add explicit database connection testing")
    print("   - Increase container startup timeout")
    print("   - Check Cloud SQL proxy configuration")

def suggest_next_steps():
    """Suggest next steps based on current status"""
    
    current_api_working = check_current_api_status()
    
    print("\n🎯 RECOMMENDED NEXT STEPS")
    print("=" * 60)
    
    if current_api_working:
        print("✅ Current API is working and has URL fields!")
        print("📋 Ready to proceed with:")
        print("   - Web scraping framework development")
        print("   - Frontend enhancement with URL display")
        print("   - Phase 2B implementation")
    else:
        print("🔧 API needs URL field fixes. Options:")
        print("   1. Manual fix: Update just the response serialization")
        print("   2. Database-first: Ensure API uses correct database fields")
        print("   3. Simple deployment: Try minimal changes")
        print("   4. Alternative: Develop web scraping framework while debugging API")
        print("")
        print("💡 RECOMMENDED: Proceed with web scraping framework")
        print("   - Database has all URL data needed")
        print("   - Can develop scraping independent of API fix")
        print("   - API can be fixed in parallel")

def main():
    """Main troubleshooting function"""
    
    print("🚀 TROUBLESHOOTING API DEPLOYMENT")
    print("=" * 60)
    
    # Check current status
    try_alternative_approach()
    
    # Provide troubleshooting guidance
    check_deployment_logs()
    
    # Suggest next steps
    suggest_next_steps()

if __name__ == "__main__":
    main()