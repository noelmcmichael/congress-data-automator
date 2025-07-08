#!/usr/bin/env python3
"""
Check current deployment status of data quality improvements
"""

import requests
import json
from datetime import datetime

def check_api_health():
    """Check API health status"""
    try:
        response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/health")
        print(f"🔍 API Health: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ API Health Error: {e}")
        return False

def check_member_committee_coverage():
    """Check member committee relationship coverage"""
    try:
        # Get first 20 members
        response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members?limit=20")
        members = response.json()
        
        coverage_count = 0
        total_members = len(members)
        
        print(f"📊 Testing {total_members} members for committee coverage...")
        
        for member in members:
            member_id = member['id']
            committees_response = requests.get(f"https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members/{member_id}/committees")
            
            if committees_response.status_code == 200:
                committees = committees_response.json()
                if committees:  # Has committee assignments
                    coverage_count += 1
                    print(f"✅ Member {member_id} ({member.get('chamber', 'N/A')}): {len(committees)} committees")
                else:
                    print(f"❌ Member {member_id} ({member.get('chamber', 'N/A')}): No committees")
            else:
                print(f"⚠️  Member {member_id}: API error {committees_response.status_code}")
        
        coverage_percentage = (coverage_count / total_members) * 100
        print(f"\n📈 Committee Coverage: {coverage_count}/{total_members} ({coverage_percentage:.1f}%)")
        return coverage_percentage
        
    except Exception as e:
        print(f"❌ Coverage Check Error: {e}")
        return 0

def check_hearing_committee_coverage():
    """Check hearing committee relationship coverage"""
    try:
        # Get first 50 hearings
        response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/hearings?limit=50")
        hearings = response.json()
        
        coverage_count = 0
        total_hearings = len(hearings)
        
        print(f"📊 Testing {total_hearings} hearings for committee coverage...")
        
        for hearing in hearings:
            if hearing.get('committee_id'):
                coverage_count += 1
                print(f"✅ Hearing {hearing['id']}: Committee {hearing['committee_id']}")
            else:
                print(f"❌ Hearing {hearing['id']}: No committee assigned")
        
        coverage_percentage = (coverage_count / total_hearings) * 100
        print(f"\n📈 Hearing Coverage: {coverage_count}/{total_hearings} ({coverage_percentage:.1f}%)")
        return coverage_percentage
        
    except Exception as e:
        print(f"❌ Hearing Coverage Check Error: {e}")
        return 0

def check_specific_improvements():
    """Check specific improvements from data quality implementation"""
    print("\n🔍 Checking specific improvements...")
    
    # Check Chuck Grassley (member 510)
    try:
        response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members/510/committees")
        if response.status_code == 200:
            committees = response.json()
            print(f"✅ Chuck Grassley (510): {len(committees)} committees")
            for committee in committees:
                print(f"   - {committee['committee']['name']} ({committee['position']})")
        else:
            print(f"❌ Chuck Grassley (510): API error {response.status_code}")
    except Exception as e:
        print(f"❌ Chuck Grassley check error: {e}")
    
    # Check Senate Judiciary Committee (ID 189)
    try:
        response = requests.get("https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/189/members")
        if response.status_code == 200:
            members = response.json()
            print(f"✅ Senate Judiciary Committee (189): {len(members)} members")
            for member in members:
                print(f"   - {member.get('name', 'N/A')} ({member.get('party', 'N/A')}-{member.get('state', 'N/A')})")
        else:
            print(f"❌ Senate Judiciary Committee (189): API error {response.status_code}")
    except Exception as e:
        print(f"❌ Senate Judiciary Committee check error: {e}")

def main():
    print("🚀 CHECKING CURRENT DEPLOYMENT STATUS")
    print("=" * 50)
    
    # Check API health
    if not check_api_health():
        print("❌ API is not healthy, cannot continue")
        return
    
    print("\n" + "=" * 50)
    
    # Check member committee coverage
    member_coverage = check_member_committee_coverage()
    
    print("\n" + "=" * 50)
    
    # Check hearing committee coverage
    hearing_coverage = check_hearing_committee_coverage()
    
    print("\n" + "=" * 50)
    
    # Check specific improvements
    check_specific_improvements()
    
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT STATUS SUMMARY")
    print(f"✅ API Health: Operational")
    print(f"📈 Member Committee Coverage: {member_coverage:.1f}%")
    print(f"📈 Hearing Committee Coverage: {hearing_coverage:.1f}%")
    
    if member_coverage >= 70 and hearing_coverage >= 40:
        print("🎉 DATA QUALITY IMPROVEMENTS ALREADY DEPLOYED!")
    elif member_coverage >= 50 or hearing_coverage >= 30:
        print("⚠️  PARTIAL DEPLOYMENT DETECTED")
    else:
        print("❌ DATA QUALITY IMPROVEMENTS NOT YET DEPLOYED")

if __name__ == "__main__":
    main()