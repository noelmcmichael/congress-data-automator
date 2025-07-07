#!/usr/bin/env python3
"""
Direct Database Fix Script
Creates a comprehensive plan to fix the database with real congressional data
"""

import json
import requests
import sys
from datetime import datetime

def analyze_current_system():
    """Analyze the current system to understand the exact issue."""
    print("🔍 Analyzing Current System State...")
    
    api_base = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Get current data
    try:
        members_response = requests.get(f"{api_base}/api/v1/members", timeout=30)
        committees_response = requests.get(f"{api_base}/api/v1/committees", timeout=30)
        
        if members_response.status_code == 200 and committees_response.status_code == 200:
            members = members_response.json()
            committees = committees_response.json()
            
            print(f"✅ Current system has {len(members)} members and {len(committees)} committees")
            
            # Show sample member
            if members:
                sample_member = members[0]
                print(f"📊 Sample member: {sample_member}")
            
            # Show sample committee  
            if committees:
                sample_committee = committees[0]
                print(f"📊 Sample committee: {sample_committee}")
            
            return members, committees
        else:
            print("❌ Failed to retrieve current data")
            return None, None
            
    except Exception as e:
        print(f"❌ Error analyzing system: {e}")
        return None, None

def create_database_update_sql():
    """Create SQL commands to fix the database structure."""
    print("📝 Creating Database Update SQL...")
    
    # Load our real committee data
    with open('real_committees_20250706_175857.json', 'r') as f:
        committees = json.load(f)
    
    with open('real_relationships_20250706_175857.json', 'r') as f:
        relationships = json.load(f)
    
    sql_commands = []
    
    # Clear existing committee data
    sql_commands.append("-- Clear existing committee and relationship data")
    sql_commands.append("DELETE FROM committee_memberships;")
    sql_commands.append("DELETE FROM committees;")
    sql_commands.append("")
    
    # Insert main committees only (not subcommittees for now)
    main_committees = [c for c in committees if not c.get('is_subcommittee', False)]
    
    sql_commands.append("-- Insert real congressional committees")
    for committee in main_committees:
        name = committee['name'].replace("'", "''")  # Escape quotes
        chamber = committee['chamber']
        jurisdiction = committee.get('jurisdiction', '').replace("'", "''")
        
        sql = f"""INSERT INTO committees (id, name, chamber, jurisdiction, is_active, is_subcommittee) 
VALUES ({committee['id']}, '{name}', '{chamber}', '{jurisdiction}', true, false);"""
        sql_commands.append(sql)
    
    sql_commands.append("")
    sql_commands.append("-- Insert committee memberships")
    
    # Insert relationships
    for relationship in relationships:
        member_id = relationship['member_id']
        committee_id = relationship['committee_id']
        position = relationship['position']
        
        sql = f"""INSERT INTO committee_memberships (member_id, committee_id, position, is_current, start_date) 
VALUES ({member_id}, {committee_id}, '{position}', true, '2023-01-01');"""
        sql_commands.append(sql)
    
    # Save SQL file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_filename = f"fix_congressional_database_{timestamp}.sql"
    
    with open(sql_filename, 'w') as f:
        f.write('\n'.join(sql_commands))
    
    print(f"✅ SQL update file created: {sql_filename}")
    print(f"📊 Commands: {len(main_committees)} committees, {len(relationships)} relationships")
    
    return sql_filename

def create_api_test_script():
    """Create a comprehensive API test script."""
    print("🧪 Creating API Test Script...")
    
    test_script = '''#!/usr/bin/env python3
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
    print("\\n👥 Testing Member Relationships...")
    
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
        
        print(f"\\n📊 Members with committees: {members_with_committees}/10")
        percentage = (members_with_committees / 10) * 100 if members_with_committees > 0 else 0
        print(f"📊 Relationship coverage: {percentage:.1f}%")
    else:
        print(f"❌ Member endpoint failed: {response.status_code}")

def test_search_functionality():
    """Test search and filter functionality."""
    print("\\n🔍 Testing Search Functionality...")
    
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
    
    print("\\n🎉 TEST COMPLETE")
    print("Check the results above to verify the system is working correctly")

if __name__ == "__main__":
    main()
'''
    
    with open('test_congressional_api.py', 'w') as f:
        f.write(test_script)
    
    print("✅ API test script created: test_congressional_api.py")

def create_step_by_step_plan():
    """Create a step-by-step implementation plan."""
    print("📋 Creating Step-by-Step Implementation Plan...")
    
    plan = {
        "title": "Congressional Database Fix - Step by Step Plan",
        "created": datetime.now().isoformat(),
        "objective": "Fix the congressional database with real committee structure and member relationships",
        "current_issues": [
            "Database has wrong committees (mostly subcommittees, not main committees)",
            "No member-committee relationships (0% coverage)",
            "Missing all major committees (Appropriations, Armed Services, etc.)",
            "UI shows no cross-relationships"
        ],
        "solution_steps": [
            {
                "step": 1,
                "title": "Database Schema Update",
                "description": "Execute SQL commands to replace existing data with real committees",
                "actions": [
                    "Connect to production Cloud SQL database",
                    "Execute the generated SQL file to clear and repopulate committees",
                    "Insert real committee memberships",
                    "Verify data integrity"
                ],
                "estimated_time": "30 minutes",
                "risk": "Medium - involves database changes"
            },
            {
                "step": 2,
                "title": "API Endpoint Testing",
                "description": "Verify all API endpoints work with new data",
                "actions": [
                    "Test committee endpoints return real committees",
                    "Test member detail pages show committees",
                    "Test committee detail pages show members", 
                    "Verify search and filter functionality"
                ],
                "estimated_time": "20 minutes",
                "risk": "Low - read-only testing"
            },
            {
                "step": 3,
                "title": "Frontend Integration Testing",
                "description": "Ensure UI properly displays relationships",
                "actions": [
                    "Test member detail pages in frontend",
                    "Test committee detail pages in frontend",
                    "Verify cross-navigation works",
                    "Check search and filter UI functionality"
                ],
                "estimated_time": "30 minutes",
                "risk": "Low - UI testing"
            },
            {
                "step": 4,
                "title": "Data Quality Validation",
                "description": "Ensure all data is accurate and complete",
                "actions": [
                    "Verify major committees are present",
                    "Check member-committee assignments are realistic",
                    "Validate leadership positions",
                    "Confirm chamber assignments are correct"
                ],
                "estimated_time": "20 minutes",
                "risk": "Low - validation only"
            }
        ],
        "success_criteria": [
            "All major House and Senate committees in database",
            "Member detail pages show committee memberships",
            "Committee detail pages show member rosters",
            "Search and filter functionality works",
            "UI cross-navigation is functional",
            "Data matches real congressional structure"
        ],
        "files_created": [
            "fix_congressional_database_[timestamp].sql",
            "test_congressional_api.py",
            "congressional_fix_plan.json"
        ]
    }
    
    # Save plan
    with open('congressional_fix_plan.json', 'w') as f:
        json.dump(plan, f, indent=2)
    
    print("✅ Step-by-step plan created: congressional_fix_plan.json")
    return plan

def main():
    """Main function for direct database fix."""
    print("🔧 CONGRESSIONAL DATABASE DIRECT FIX")
    print("=" * 60)
    print("Creating comprehensive plan to fix congressional database")
    print("=" * 60)
    
    # Step 1: Analyze current system
    members, committees = analyze_current_system()
    
    # Step 2: Create database update SQL
    sql_file = create_database_update_sql()
    
    # Step 3: Create API test script
    create_api_test_script()
    
    # Step 4: Create implementation plan
    plan = create_step_by_step_plan()
    
    print(f"\n🎯 NEXT STEPS TO FIX THE DATABASE:")
    print("=" * 50)
    print("1. Execute the SQL file to update the database:")
    print(f"   📄 File: {sql_file}")
    print("2. Run the API test to verify functionality:")
    print("   📄 File: test_congressional_api.py")
    print("3. Test the frontend to ensure UI relationships work")
    print("4. Validate data quality and completeness")
    
    print(f"\n🎉 DATABASE FIX PLAN COMPLETE!")
    print("All files created and ready for implementation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)