#!/usr/bin/env python3
"""
Database Structure Assessment Script
Comprehensive audit of current production database state
"""

import requests
import json
import sys
from datetime import datetime

def get_production_data(endpoint, description):
    """Get data from production API endpoint."""
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    try:
        print(f"📊 Fetching {description}...")
        response = requests.get(f"{base_url}{endpoint}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {description}: {len(data)} items retrieved")
            return data
        else:
            print(f"❌ {description}: Failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ {description}: Error - {str(e)}")
        return None

def analyze_committees(committees):
    """Analyze committee structure and identify gaps."""
    print("\n🏛️ COMMITTEE STRUCTURE ANALYSIS")
    print("=" * 50)
    
    if not committees:
        print("❌ No committee data available")
        return
    
    # Group by chamber
    house_committees = [c for c in committees if c.get('chamber') == 'House']
    senate_committees = [c for c in committees if c.get('chamber') == 'Senate']
    joint_committees = [c for c in committees if c.get('chamber') not in ['House', 'Senate']]
    
    print(f"📊 Committee Distribution:")
    print(f"   House Committees: {len(house_committees)}")
    print(f"   Senate Committees: {len(senate_committees)}")
    print(f"   Joint/Other Committees: {len(joint_committees)}")
    
    # Check for major House committees
    major_house_committees = [
        "Appropriations", "Armed Services", "Budget", "Education", "Energy", 
        "Financial Services", "Foreign Affairs", "Homeland Security", "Judiciary",
        "Natural Resources", "Oversight", "Rules", "Science", "Small Business",
        "Transportation", "Veterans", "Ways and Means", "Agriculture", "Ethics"
    ]
    
    print(f"\n🏛️ HOUSE COMMITTEES:")
    house_names = [c.get('name', '') for c in house_committees]
    for major in major_house_committees:
        found = any(major.lower() in name.lower() for name in house_names)
        status = "✅" if found else "❌"
        print(f"   {status} {major}")
    
    # Check for major Senate committees
    major_senate_committees = [
        "Agriculture", "Appropriations", "Armed Services", "Banking", "Budget",
        "Commerce", "Energy", "Environment", "Finance", "Foreign Relations",
        "Health", "Homeland Security", "Judiciary", "Rules", "Small Business", "Veterans"
    ]
    
    print(f"\n🏛️ SENATE COMMITTEES:")
    senate_names = [c.get('name', '') for c in senate_committees]
    for major in major_senate_committees:
        found = any(major.lower() in name.lower() for name in senate_names)
        status = "✅" if found else "❌"
        print(f"   {status} {major}")
    
    # List actual committees
    print(f"\n📋 ACTUAL HOUSE COMMITTEES ({len(house_committees)}):")
    for i, committee in enumerate(house_committees[:10], 1):  # Show first 10
        print(f"   {i}. {committee.get('name', 'Unknown')}")
    if len(house_committees) > 10:
        print(f"   ... and {len(house_committees) - 10} more")
    
    print(f"\n📋 ACTUAL SENATE COMMITTEES ({len(senate_committees)}):")
    for i, committee in enumerate(senate_committees[:10], 1):  # Show first 10
        print(f"   {i}. {committee.get('name', 'Unknown')}")
    if len(senate_committees) > 10:
        print(f"   ... and {len(senate_committees) - 10} more")

def analyze_members(members):
    """Analyze member structure."""
    print("\n👥 MEMBER STRUCTURE ANALYSIS")
    print("=" * 50)
    
    if not members:
        print("❌ No member data available")
        return
    
    # Group by chamber
    house_members = [m for m in members if m.get('chamber') == 'House']
    senate_members = [m for m in members if m.get('chamber') == 'Senate']
    
    print(f"📊 Member Distribution:")
    print(f"   House Members: {len(house_members)}")
    print(f"   Senate Members: {len(senate_members)}")
    print(f"   Total Members: {len(members)}")
    
    # Check party distribution
    party_counts = {}
    for member in members:
        party = member.get('party', 'Unknown')
        party_counts[party] = party_counts.get(party, 0) + 1
    
    print(f"\n🎭 Party Distribution:")
    for party, count in sorted(party_counts.items()):
        print(f"   {party}: {count}")
    
    # Show sample members
    print(f"\n📋 SAMPLE MEMBERS:")
    for i, member in enumerate(members[:5], 1):
        name = member.get('name', 'Unknown')
        chamber = member.get('chamber', 'Unknown')
        party = member.get('party', 'Unknown')
        state = member.get('state', 'Unknown')
        print(f"   {i}. {name} ({party}-{state}) - {chamber}")

def test_member_relationships():
    """Test member-committee relationships."""
    print("\n🔗 MEMBER-COMMITTEE RELATIONSHIPS TEST")
    print("=" * 50)
    
    # Get members and test relationship endpoints
    members = get_production_data("/api/v1/members", "Members for relationship testing")
    
    if not members:
        print("❌ Cannot test relationships - no member data")
        return
    
    # Test first few members' detail pages
    tested_members = 0
    members_with_committees = 0
    
    for member in members[:10]:  # Test first 10 members
        member_id = member.get('id')
        member_name = member.get('name', 'Unknown')
        
        if member_id:
            try:
                response = requests.get(
                    f"https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/members/{member_id}/detail",
                    timeout=30
                )
                
                if response.status_code == 200:
                    detail_data = response.json()
                    committees = detail_data.get('committees', [])
                    
                    tested_members += 1
                    if committees:
                        members_with_committees += 1
                        print(f"✅ {member_name}: {len(committees)} committee(s)")
                    else:
                        print(f"❌ {member_name}: No committees")
                else:
                    print(f"❌ {member_name}: Detail endpoint failed ({response.status_code})")
                    
            except Exception as e:
                print(f"❌ {member_name}: Error testing detail - {str(e)}")
    
    print(f"\n📊 Relationship Test Summary:")
    print(f"   Members tested: {tested_members}")
    print(f"   Members with committees: {members_with_committees}")
    print(f"   Members without committees: {tested_members - members_with_committees}")
    
    if tested_members > 0:
        percentage = (members_with_committees / tested_members) * 100
        print(f"   Relationship coverage: {percentage:.1f}%")

def test_committee_relationships():
    """Test committee-member relationships."""
    print("\n🔗 COMMITTEE-MEMBER RELATIONSHIPS TEST")
    print("=" * 50)
    
    # Get committees and test relationship endpoints
    committees = get_production_data("/api/v1/committees", "Committees for relationship testing")
    
    if not committees:
        print("❌ Cannot test relationships - no committee data")
        return
    
    # Test first few committees' detail pages
    tested_committees = 0
    committees_with_members = 0
    
    for committee in committees[:10]:  # Test first 10 committees
        committee_id = committee.get('id')
        committee_name = committee.get('name', 'Unknown')
        
        if committee_id:
            try:
                response = requests.get(
                    f"https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1/committees/{committee_id}/detail",
                    timeout=30
                )
                
                if response.status_code == 200:
                    detail_data = response.json()
                    members = detail_data.get('members', [])
                    
                    tested_committees += 1
                    if members:
                        committees_with_members += 1
                        print(f"✅ {committee_name}: {len(members)} member(s)")
                    else:
                        print(f"❌ {committee_name}: No members")
                else:
                    print(f"❌ {committee_name}: Detail endpoint failed ({response.status_code})")
                    
            except Exception as e:
                print(f"❌ {committee_name}: Error testing detail - {str(e)}")
    
    print(f"\n📊 Committee Relationship Test Summary:")
    print(f"   Committees tested: {tested_committees}")
    print(f"   Committees with members: {committees_with_members}")
    print(f"   Committees without members: {tested_committees - committees_with_members}")
    
    if tested_committees > 0:
        percentage = (committees_with_members / tested_committees) * 100
        print(f"   Member coverage: {percentage:.1f}%")

def generate_audit_report(members, committees, hearings):
    """Generate comprehensive audit report."""
    print("\n📋 COMPREHENSIVE AUDIT REPORT")
    print("=" * 50)
    
    # Create detailed report
    report = {
        "audit_date": datetime.now().isoformat(),
        "database_status": "audited",
        "summary": {
            "total_members": len(members) if members else 0,
            "total_committees": len(committees) if committees else 0,
            "total_hearings": len(hearings) if hearings else 0
        },
        "issues_identified": [],
        "recommendations": []
    }
    
    # Identify issues
    if not members or len(members) < 400:
        report["issues_identified"].append("Insufficient member data (expected ~535 members)")
    
    if not committees or len(committees) < 30:
        report["issues_identified"].append("Insufficient committee data (expected ~40+ committees)")
    
    # Check for major missing committees
    if committees:
        committee_names = [c.get('name', '').lower() for c in committees]
        critical_committees = ['appropriations', 'judiciary', 'foreign', 'armed services', 'finance']
        
        for critical in critical_committees:
            if not any(critical in name for name in committee_names):
                report["issues_identified"].append(f"Missing critical committee: {critical}")
    
    # Add recommendations
    report["recommendations"] = [
        "Collect complete committee structure from official sources",
        "Establish real member-committee relationships",
        "Implement UI cross-relationship navigation",
        "Validate data accuracy against House.gov and Senate.gov",
        "Add subcommittee hierarchy support"
    ]
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"database_audit_report_{timestamp}.json"
    
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Detailed audit report saved to: {report_filename}")
    
    # Print summary
    print(f"\n🎯 CRITICAL ISSUES IDENTIFIED:")
    for issue in report["issues_identified"]:
        print(f"   ❌ {issue}")
    
    print(f"\n💡 RECOMMENDED ACTIONS:")
    for rec in report["recommendations"]:
        print(f"   🔧 {rec}")
    
    return report

def main():
    """Main database audit function."""
    print("🔍 CONGRESSIONAL DATABASE AUDIT")
    print("=" * 60)
    print("Comprehensive assessment of production database state")
    print("=" * 60)
    
    # Step 1: Get all data
    members = get_production_data("/api/v1/members", "Members")
    committees = get_production_data("/api/v1/committees", "Committees")
    hearings = get_production_data("/api/v1/hearings", "Hearings")
    
    # Step 2: Analyze structure
    analyze_committees(committees)
    analyze_members(members)
    
    # Step 3: Test relationships
    test_member_relationships()
    test_committee_relationships()
    
    # Step 4: Generate report
    report = generate_audit_report(members, committees, hearings)
    
    print(f"\n🎉 DATABASE AUDIT COMPLETE")
    print("=" * 40)
    print("Review the detailed findings above and the generated report.")
    print("Next: Implement fixes based on identified issues.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)