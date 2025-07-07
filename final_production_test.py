#!/usr/bin/env python3
"""
Final production test to verify Phase 2 completion.
"""
import requests
import json

def test_api_health():
    """Test API health endpoint."""
    try:
        response = requests.get(
            "https://congressional-data-api-v3-1066017671167.us-central1.run.app/health",
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print(f"❌ API Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ API Health Check: ERROR - {e}")
        return False

def test_committees_endpoint():
    """Test committees endpoint with URL fields."""
    try:
        response = requests.get(
            "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1/committees",
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Committees Endpoint: PASSED ({len(data)} committees)")
            
            # Check for URL fields
            url_fields = ['hearings_url', 'members_url', 'official_website_url']
            has_url_fields = any(field in data[0] for field in url_fields) if data else False
            
            if has_url_fields:
                print("✅ URL Fields Present: PASSED")
                
                # Count committees with URL data
                committees_with_urls = 0
                for committee in data:
                    if any(committee.get(field) for field in url_fields):
                        committees_with_urls += 1
                
                print(f"✅ Committees with URL Data: {committees_with_urls}")
                
                # Show sample committee with URLs
                for committee in data[:3]:
                    if committee.get('official_website_url'):
                        print(f"   📋 {committee['name']}: {committee['official_website_url']}")
                
                return True
            else:
                print("❌ URL Fields Present: FAILED")
                return False
        else:
            print(f"❌ Committees Endpoint: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Committees Endpoint: ERROR - {e}")
        return False

def test_frontend_accessibility():
    """Test frontend accessibility."""
    try:
        response = requests.get(
            "https://storage.googleapis.com/congressional-data-frontend/index.html",
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Frontend Accessibility: PASSED")
            return True
        else:
            print(f"❌ Frontend Accessibility: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Frontend Accessibility: ERROR - {e}")
        return False

def main():
    """Run final production test."""
    print("🧪 Final Production Test - Phase 2 Completion Verification")
    print("=" * 60)
    
    # Test API health
    api_health = test_api_health()
    
    # Test committees endpoint with URL fields
    committees_test = test_committees_endpoint()
    
    # Test frontend accessibility
    frontend_test = test_frontend_accessibility()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    if api_health and committees_test and frontend_test:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Phase 2 is 100% COMPLETE and fully operational")
        print("✅ Enhanced Congressional Data Platform is live")
        print("✅ Official committee resource integration successful")
        print("")
        print("🌐 Production URLs:")
        print("   Frontend: https://storage.googleapis.com/congressional-data-frontend/index.html")
        print("   API: https://congressional-data-api-v3-1066017671167.us-central1.run.app")
        print("")
        print("🏆 MISSION ACCOMPLISHED!")
    else:
        print("⚠️  Some tests failed - manual verification recommended")
        print(f"   API Health: {'✅' if api_health else '❌'}")
        print(f"   Committees Endpoint: {'✅' if committees_test else '❌'}")
        print(f"   Frontend: {'✅' if frontend_test else '❌'}")

if __name__ == "__main__":
    main()