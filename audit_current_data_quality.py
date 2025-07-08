#!/usr/bin/env python3
"""
Quick audit of current production data quality issues
"""

import requests
import json
from datetime import datetime

# Production API URL
BASE_URL = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"

def audit_committee_memberships():
    """Audit committee membership data quality"""
    print("🔍 Auditing Committee Memberships...")
    
    # Get all members
    members_response = requests.get(f"{BASE_URL}/members?limit=100")
    members_data = members_response.json()
    
    # Get all committees  
    committees_response = requests.get(f"{BASE_URL}/committees?limit=100")
    committees_data = committees_response.json()
    
    # Handle different response formats
    if isinstance(members_data, dict) and 'members' in members_data:
        members_list = members_data['members']
    elif isinstance(members_data, list):
        members_list = members_data
    else:
        members_list = []
        
    if isinstance(committees_data, dict) and 'committees' in committees_data:
        committees_list = committees_data['committees']
    elif isinstance(committees_data, list):
        committees_list = committees_data
    else:
        committees_list = []
    
    print(f"📊 Found {len(members_list)} members")
    print(f"📊 Found {len(committees_list)} committees")
    
    # Check committee memberships
    members_with_committees = 0
    members_without_committees = 0
    committee_assignment_examples = []
    
    for member in members_list[:10]:  # Sample first 10
        member_id = member.get('id')
        name = f"{member.get('first_name', '')} {member.get('last_name', '')}"
        
        # Check if member has committee assignments
        if 'committees' in member and member['committees']:
            members_with_committees += 1
            committee_assignment_examples.append({
                'member': name,
                'committees': member['committees']
            })
        else:
            members_without_committees += 1
            
    print(f"✅ Members with committee assignments: {members_with_committees}")
    print(f"❌ Members without committee assignments: {members_without_committees}")
    
    # Show examples
    print("\n📋 Committee Assignment Examples:")
    for example in committee_assignment_examples[:3]:
        print(f"  - {example['member']}: {len(example['committees'])} committees")
        for committee in example['committees'][:2]:  # Show first 2 committees
            print(f"    • {committee.get('name', 'Unknown')}")
    
    return {
        'total_members': len(members_list),
        'members_with_committees': members_with_committees,
        'members_without_committees': members_without_committees,
        'committee_assignment_examples': committee_assignment_examples
    }

def audit_hearing_committee_relationships():
    """Audit hearing-committee relationship data quality"""
    print("\n🔍 Auditing Hearing-Committee Relationships...")
    
    # Get all hearings
    hearings_response = requests.get(f"{BASE_URL}/hearings?limit=100")
    hearings_data = hearings_response.json()
    
    # Handle different response formats
    if isinstance(hearings_data, dict) and 'hearings' in hearings_data:
        hearings_list = hearings_data['hearings']
    elif isinstance(hearings_data, list):
        hearings_list = hearings_data
    else:
        hearings_list = []
    
    print(f"📊 Found {len(hearings_list)} hearings")
    
    # Check hearing-committee relationships
    hearings_with_committees = 0
    hearings_without_committees = 0
    hearing_committee_examples = []
    
    for hearing in hearings_list[:10]:  # Sample first 10
        hearing_title = hearing.get('title', 'Unknown')[:50] + "..."
        
        if 'committee' in hearing and hearing['committee']:
            hearings_with_committees += 1
            hearing_committee_examples.append({
                'hearing': hearing_title,
                'committee': hearing['committee']
            })
        else:
            hearings_without_committees += 1
            
    print(f"✅ Hearings with committee assignment: {hearings_with_committees}")
    print(f"❌ Hearings without committee assignment: {hearings_without_committees}")
    
    # Show examples
    print("\n📋 Hearing-Committee Examples:")
    for example in hearing_committee_examples[:3]:
        committee_name = example['committee'].get('name', 'Unknown') if isinstance(example['committee'], dict) else str(example['committee'])
        print(f"  - {example['hearing']}")
        print(f"    Committee: {committee_name}")
    
    return {
        'total_hearings': len(hearings_list),
        'hearings_with_committees': hearings_with_committees,
        'hearings_without_committees': hearings_without_committees,
        'hearing_committee_examples': hearing_committee_examples
    }

def check_specific_examples():
    """Check specific examples of potential data issues"""
    print("\n🔍 Checking Specific Data Examples...")
    
    # Check Chuck Grassley as mentioned in previous context
    grassley_response = requests.get(f"{BASE_URL}/members?search=Grassley")
    grassley_data = grassley_response.json()
    
    # Handle different response formats
    if isinstance(grassley_data, dict) and 'members' in grassley_data:
        grassley_list = grassley_data['members']
    elif isinstance(grassley_data, list):
        grassley_list = grassley_data
    else:
        grassley_list = []
    
    if grassley_list:
        grassley = grassley_list[0]
        print(f"📋 Chuck Grassley Committee Assignments:")
        print(f"   Name: {grassley.get('first_name')} {grassley.get('last_name')}")
        print(f"   State: {grassley.get('state')}")
        print(f"   Committees: {len(grassley.get('committees', []))}")
        
        for committee in grassley.get('committees', [])[:3]:
            print(f"     • {committee.get('name', 'Unknown')}")
    
    # Check a specific committee membership
    judiciary_response = requests.get(f"{BASE_URL}/committees?search=Judiciary")
    judiciary_data = judiciary_response.json()
    
    # Handle different response formats
    if isinstance(judiciary_data, dict) and 'committees' in judiciary_data:
        judiciary_list = judiciary_data['committees']
    elif isinstance(judiciary_data, list):
        judiciary_list = judiciary_data
    else:
        judiciary_list = []
    
    if judiciary_list:
        judiciary = judiciary_list[0]
        print(f"\n📋 Judiciary Committee Members:")
        print(f"   Committee: {judiciary.get('name')}")
        
        # Try to get committee members (if the endpoint exists)
        try:
            committee_id = judiciary.get('id')
            members_response = requests.get(f"{BASE_URL}/committees/{committee_id}/members")
            if members_response.status_code == 200:
                committee_members = members_response.json()
                print(f"   Members: {len(committee_members.get('members', []))}")
            else:
                print(f"   Members endpoint not available (status: {members_response.status_code})")
        except Exception as e:
            print(f"   Error checking committee members: {e}")

def generate_audit_report():
    """Generate comprehensive audit report"""
    print("🏛️ Congressional Data Quality Audit Report")
    print("=" * 50)
    print(f"📅 Audit Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Endpoint: {BASE_URL}")
    
    # Run audits
    membership_audit = audit_committee_memberships()
    hearing_audit = audit_hearing_committee_relationships()
    check_specific_examples()
    
    # Summary
    print("\n📊 AUDIT SUMMARY")
    print("-" * 30)
    print(f"Total Members: {membership_audit['total_members']}")
    print(f"Members with Committees: {membership_audit['members_with_committees']}")
    print(f"Members without Committees: {membership_audit['members_without_committees']}")
    print(f"Committee Assignment Rate: {(membership_audit['members_with_committees'] / membership_audit['total_members'] * 100):.1f}%")
    
    print(f"\nTotal Hearings: {hearing_audit['total_hearings']}")
    print(f"Hearings with Committees: {hearing_audit['hearings_with_committees']}")
    print(f"Hearings without Committees: {hearing_audit['hearings_without_committees']}")
    print(f"Hearing-Committee Link Rate: {(hearing_audit['hearings_with_committees'] / hearing_audit['total_hearings'] * 100):.1f}%")
    
    # Data quality assessment
    print("\n🎯 DATA QUALITY ASSESSMENT")
    print("-" * 30)
    
    committee_rate = membership_audit['members_with_committees'] / membership_audit['total_members']
    hearing_rate = hearing_audit['hearings_with_committees'] / hearing_audit['total_hearings']
    
    if committee_rate < 0.5:
        print("❌ CRITICAL: Low committee membership assignment rate")
    elif committee_rate < 0.8:
        print("⚠️  WARNING: Moderate committee membership issues")
    else:
        print("✅ GOOD: Committee membership assignment rate acceptable")
        
    if hearing_rate < 0.5:
        print("❌ CRITICAL: Low hearing-committee relationship rate")
    elif hearing_rate < 0.8:
        print("⚠️  WARNING: Moderate hearing-committee relationship issues")
    else:
        print("✅ GOOD: Hearing-committee relationship rate acceptable")
    
    print("\n🔧 RECOMMENDATIONS")
    print("-" * 30)
    
    if committee_rate < 0.8:
        print("1. Implement committee membership data collection from authoritative sources")
        print("2. Cross-reference member assignments with official committee rosters")
        
    if hearing_rate < 0.8:
        print("3. Parse hearing metadata to extract committee information")
        print("4. Create hearing-committee mapping based on jurisdiction rules")
    
    print("5. Establish ongoing data quality monitoring")
    print("6. Create automated data validation checks")

if __name__ == "__main__":
    generate_audit_report()