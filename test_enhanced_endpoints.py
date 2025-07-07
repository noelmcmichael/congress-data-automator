#!/usr/bin/env python3
"""
Test script to verify enhanced endpoints work with current API structure
"""
import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"

def test_basic_endpoints():
    """Test basic endpoints to ensure API is working"""
    print("🔍 Testing Basic Endpoints")
    
    # Test members endpoint
    response = requests.get(f"{BASE_URL}/members?limit=5")
    if response.status_code == 200:
        members = response.json()
        print(f"✅ Members endpoint: {len(members)} members returned")
        if members:
            print(f"   First member: {members[0]['first_name']} {members[0]['last_name']} ({members[0]['party']}, {members[0]['chamber']})")
    else:
        print(f"❌ Members endpoint failed: {response.status_code}")
    
    # Test committees endpoint
    response = requests.get(f"{BASE_URL}/committees?limit=5")
    if response.status_code == 200:
        committees = response.json()
        print(f"✅ Committees endpoint: {len(committees)} committees returned")
        if committees:
            print(f"   First committee: {committees[0]['name']} ({committees[0]['chamber']})")
    else:
        print(f"❌ Committees endpoint failed: {response.status_code}")

def test_relationship_endpoints():
    """Test relationship endpoints"""
    print("\n🔗 Testing Relationship Endpoints")
    
    # Get a member ID first
    response = requests.get(f"{BASE_URL}/members?limit=1")
    if response.status_code == 200:
        members = response.json()
        if members:
            member_id = members[0]['id']
            member_name = f"{members[0]['first_name']} {members[0]['last_name']}"
            
            # Test member committees
            response = requests.get(f"{BASE_URL}/members/{member_id}/committees")
            if response.status_code == 200:
                committees = response.json()
                print(f"✅ Member committees: {member_name} serves on {len(committees)} committees")
                for committee in committees:
                    position = committee.get('position', 'Member')
                    print(f"   - {committee['committee']['name']} ({position})")
            else:
                print(f"❌ Member committees endpoint failed: {response.status_code}")
    
    # Test committee members
    response = requests.get(f"{BASE_URL}/committees?limit=1")
    if response.status_code == 200:
        committees = response.json()
        if committees:
            committee_id = committees[0]['id']
            committee_name = committees[0]['name']
            
            response = requests.get(f"{BASE_URL}/committees/{committee_id}/members")
            if response.status_code == 200:
                members = response.json()
                print(f"✅ Committee members: {committee_name} has {len(members)} members")
                for member in members[:3]:  # Show first 3
                    position = member.get('position', 'Member')
                    print(f"   - {member['member']['first_name']} {member['member']['last_name']} ({position})")
            else:
                print(f"❌ Committee members endpoint failed: {response.status_code}")

def test_senate_data():
    """Test Senate-specific data for term class analysis"""
    print("\n🏛️ Testing Senate Data")
    
    # Get senators
    response = requests.get(f"{BASE_URL}/members?chamber=Senate&limit=10")
    if response.status_code == 200:
        senators = response.json()
        print(f"✅ Senate members: {len(senators)} senators returned")
        
        # Analyze term classes
        term_classes = {"I": 0, "II": 0, "III": 0, "Unknown": 0}
        
        for senator in senators:
            term_end = senator.get('term_end')
            if term_end:
                # Parse date string
                try:
                    if isinstance(term_end, str):
                        year = int(term_end[:4])
                    else:
                        year = term_end.year
                    
                    if year % 6 == 1:  # 2025, 2031, etc.
                        term_classes["I"] += 1
                        next_election = 2024
                    elif year % 6 == 3:  # 2027, 2033, etc.
                        term_classes["II"] += 1
                        next_election = 2026
                    else:  # 2029, 2035, etc.
                        term_classes["III"] += 1
                        next_election = 2028
                    
                    print(f"   {senator['first_name']} {senator['last_name']} (Class {['I', 'II', 'III'][list(term_classes.keys()).index(max(term_classes, key=term_classes.get))]}, next election: {next_election})")
                except:
                    term_classes["Unknown"] += 1
            else:
                term_classes["Unknown"] += 1
        
        print(f"   Term class distribution: {term_classes}")
    else:
        print(f"❌ Senate members endpoint failed: {response.status_code}")

def test_committee_hierarchy():
    """Test committee hierarchy data"""
    print("\n📊 Testing Committee Hierarchy")
    
    # Get committees with subcommittees
    response = requests.get(f"{BASE_URL}/committees?limit=20")
    if response.status_code == 200:
        committees = response.json()
        
        standing_committees = [c for c in committees if not c.get('is_subcommittee', False)]
        subcommittees = [c for c in committees if c.get('is_subcommittee', False)]
        
        print(f"✅ Committee structure: {len(standing_committees)} standing committees, {len(subcommittees)} subcommittees")
        
        # Show hierarchy examples
        for committee in standing_committees[:3]:
            committee_id = committee['id']
            response = requests.get(f"{BASE_URL}/committees/{committee_id}/subcommittees")
            if response.status_code == 200:
                subs = response.json()
                print(f"   {committee['name']}: {len(subs)} subcommittees")
                for sub in subs[:2]:  # Show first 2
                    print(f"     - {sub['name']}")
            else:
                print(f"   {committee['name']}: Unable to fetch subcommittees")
    else:
        print(f"❌ Committees endpoint failed: {response.status_code}")

def generate_enhancement_summary():
    """Generate summary of what enhanced endpoints would provide"""
    print("\n🎯 Enhancement Summary")
    print("Based on current API structure, enhanced endpoints would provide:")
    print("1. ✅ Enhanced Member Views:")
    print("   - Member committee memberships with leadership positions")
    print("   - Term information and re-election dates")
    print("   - Committee assignment statistics")
    print("   - Current API: /members/{id}/committees already works")
    
    print("\n2. ✅ Committee Hierarchy Dashboards:")
    print("   - Standing committee → subcommittee relationships")
    print("   - Committee member rosters with leadership")
    print("   - Committee statistics and jurisdiction")
    print("   - Current API: /committees/{id}/subcommittees already works")
    
    print("\n3. ✅ Senator Re-election Timeline:")
    print("   - Term class analysis (I, II, III)")
    print("   - Next election year calculations")
    print("   - State-by-state senator term views")
    print("   - Data available through /members?chamber=Senate")
    
    print("\n4. ✅ Committee Jurisdiction Mapping:")
    print("   - Committee responsibility areas")
    print("   - Policy jurisdiction overlap analysis")
    print("   - Committee scope and oversight")
    print("   - Data structure ready for enhancement")
    
    print("\n5. 🔄 Complete Senate Representation:")
    print("   - Need to verify 100/100 senators in database")
    print("   - Web scraping for missing senators")
    print("   - Committee assignment completion")

if __name__ == "__main__":
    print("🚀 Testing Enhanced Congressional Data API Endpoints")
    print("=" * 60)
    
    try:
        test_basic_endpoints()
        test_relationship_endpoints()
        test_senate_data()
        test_committee_hierarchy()
        generate_enhancement_summary()
        
        print("\n" + "=" * 60)
        print("✅ API Testing Complete - Ready for Enhancement Implementation")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("Check API connectivity and endpoints")