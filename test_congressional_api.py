#!/usr/bin/env python3
"""
Congressional API Test Script
Comprehensive testing of the fixed congressional database
"""

import requests
import json

def test_committees():
    """Test committee endpoints."""
    print("🏛️ Testing Committee Endpoints...")
    
    api_base = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Get all committees
    response = requests.get(f"{api_base}/api/v1/committees", timeout=30)
    if response.status_code == 200:
        committees = response.json()
        print(f"✅ Retrieved {len(committees)} committees")
        
        # Check for major committees
        major_committees = [
            "Appropriations", "Armed Services", "Judiciary", "Foreign Affairs",
            "Energy and Commerce", "Financial Services", "Transportation"
        ]
        
        committee_names = [c.get('name', '').lower() for c in committees]
        found_major = 0
        
        for major in major_committees:
            if any(major.lower() in name for name in committee_names):
                found_major += 1
                print(f"✅ Found: {major}")
            else:
                print(f"❌ Missing: {major}")
        
        print(f"📊 Major committees found: {found_major}/{len(major_committees)}")
        
        # Test committee detail
        if committees:
            test_committee = committees[0]
            committee_id = test_committee.get('id')
            if committee_id:
                detail_response = requests.get(f"{api_base}/api/v1/committees/{committee_id}/detail", timeout=30)
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    members = detail_data.get('members', [])
                    print(f"✅ Committee detail working: {len(members)} members")
                else:
                    print("❌ Committee detail endpoint failed")
    else:
        print(f"❌ Committee endpoint failed: {response.status_code}")

def test_member_relationships():
    """Test member-committee relationships."""
    print("\n👥 Testing Member Relationships...")
    
    api_base = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Get all members
    response = requests.get(f"{api_base}/api/v1/members", timeout=30)
    if response.status_code == 200:
        members = response.json()
        print(f"✅ Retrieved {len(members)} members")
        
        # Test member details
        members_with_committees = 0
        
        for member in members[:10]:  # Test first 10
            member_id = member.get('id')
            member_name = member.get('name', 'Unknown')
            
            if member_id:
                detail_response = requests.get(f"{api_base}/api/v1/members/{member_id}/detail", timeout=30)
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    committees = detail_data.get('committees', [])
                    
                    if committees:
                        members_with_committees += 1
                        print(f"✅ {member_name}: {len(committees)} committee(s)")
                        
                        # Show committee details
                        for committee in committees[:2]:  # Show first 2
                            committee_name = committee.get('name', 'Unknown')
                            position = committee.get('position', 'Member')
                            print(f"   - {committee_name} ({position})")
                    else:
                        print(f"⚠️ {member_name}: No committees")
        
        print(f"\n📊 Members with committees: {members_with_committees}/10")
        percentage = (members_with_committees / 10) * 100 if members_with_committees > 0 else 0
        print(f"📊 Relationship coverage: {percentage:.1f}%")
    else:
        print(f"❌ Member endpoint failed: {response.status_code}")

def test_search_functionality():
    """Test search and filter functionality."""
    print("\n🔍 Testing Search Functionality...")
    
    api_base = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    test_cases = [
        ("Committee search - Judiciary", "/api/v1/committees?search=Judiciary"),
        ("Committee search - Appropriations", "/api/v1/committees?search=Appropriations"),
        ("Member party filter", "/api/v1/members?party=Republican"),
        ("Member chamber filter", "/api/v1/members?chamber=House"),
        ("Member search", "/api/v1/members?search=John"),
    ]
    
    for test_name, endpoint in test_cases:
        try:
            response = requests.get(f"{api_base}{endpoint}", timeout=30)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('total', 0)
                print(f"✅ {test_name}: {count} results")
            else:
                print(f"❌ {test_name}: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {test_name}: Error - {str(e)}")

def main():
    """Main test function."""
    print("🧪 CONGRESSIONAL API COMPREHENSIVE TEST")
    print("=" * 60)
    
    test_committees()
    test_member_relationships()
    test_search_functionality()
    
    print("\n🎉 TEST COMPLETE")
    print("Check the results above to verify the system is working correctly")

if __name__ == "__main__":
    main()
