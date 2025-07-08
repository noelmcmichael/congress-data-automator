#!/usr/bin/env python3
"""
Audit current committee assignment accuracy
"""

import requests
import json
from datetime import datetime

def audit_committee_accuracy():
    """Audit current committee assignment accuracy."""
    
    print("🔍 COMMITTEE ACCURACY AUDIT")
    print("=" * 50)
    print(f"Audit Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    base_url = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    # Test 1: Check Senate Judiciary Committee
    print("1. SENATE JUDICIARY COMMITTEE AUDIT")
    print("-" * 35)
    
    # Known Senate Judiciary members (119th Congress)
    known_judiciary = {
        "Chair": "Dick Durbin (D-IL)",
        "Ranking": "Chuck Grassley (R-IA)", 
        "Members": [
            "Sheldon Whitehouse (D-RI)",
            "Amy Klobuchar (D-MN)",
            "Chris Coons (D-DE)",
            "Richard Blumenthal (D-CT)",
            "Mazie Hirono (D-HI)",
            "Cory Booker (D-NJ)",
            "Alex Padilla (D-CA)",
            "Jon Ossoff (D-GA)",
            "Peter Welch (D-VT)",
            "Lindsey Graham (R-SC)",
            "John Cornyn (R-TX)", 
            "Mike Lee (R-UT)",
            "Ted Cruz (R-TX)",
            "Josh Hawley (R-MO)",
            "Tom Cotton (R-AR)",
            "John Kennedy (R-LA)",
            "Thom Tillis (R-NC)",
            "Marsha Blackburn (R-TN)"
        ]
    }
    
    # Get current Judiciary Committee data
    try:
        response = requests.get(f"{base_url}/api/v1/committees", timeout=10)
        if response.status_code == 200:
            committees = response.json()
            judiciary_committee = None
            for committee in committees:
                if "Judiciary" in committee.get('name', ''):
                    judiciary_committee = committee
                    break
            
            if judiciary_committee:
                print(f"Found committee: {judiciary_committee['name']}")
                print(f"Committee ID: {judiciary_committee['id']}")
                
                # Get members
                response = requests.get(f"{base_url}/api/v1/committees/{judiciary_committee['id']}/members", timeout=10)
                if response.status_code == 200:
                    current_members = response.json()
                    print(f"Current members in system: {len(current_members)}")
                    print(f"Expected members: {len(known_judiciary['Members']) + 2}")  # +2 for chair/ranking
                    
                    # Show current members
                    print("\nCurrent members in system:")
                    for member in current_members[:10]:  # Show first 10
                        name = f"{member.get('first_name', '')} {member.get('last_name', '')}"
                        state = member.get('state', 'Unknown')
                        party = member.get('party', 'Unknown')
                        print(f"  - {name} ({party}-{state})")
                    
                    if len(current_members) > 10:
                        print(f"  ... and {len(current_members) - 10} more")
                        
                else:
                    print(f"Error getting members: {response.status_code}")
            else:
                print("❌ Senate Judiciary Committee not found")
        else:
            print(f"Error getting committees: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Test 2: Check Commerce, Science, and Transportation Committee
    print("2. COMMERCE, SCIENCE, AND TRANSPORTATION AUDIT")
    print("-" * 48)
    
    # Known Commerce Committee members (119th Congress)
    known_commerce = {
        "Chair": "Maria Cantwell (D-WA)",
        "Ranking": "Ted Cruz (R-TX)",
        "Members": [
            "Amy Klobuchar (D-MN)",
            "Richard Blumenthal (D-CT)",
            "Brian Schatz (D-HI)",
            "Edward Markey (D-MA)",
            "Gary Peters (D-MI)",
            "Tammy Baldwin (D-WI)",
            "Tammy Duckworth (D-IL)",
            "Jon Tester (D-MT)",
            "Kyrsten Sinema (I-AZ)",
            "Ben Ray Luján (D-NM)",
            "John Hickenlooper (D-CO)",
            "Raphael Warnock (D-GA)",
            "Peter Welch (D-VT)",
            "John Thune (R-SD)",
            "Roger Wicker (R-MS)",
            "Marsha Blackburn (R-TN)",
            "Dan Sullivan (R-AK)",
            "Deb Fischer (R-NE)",
            "Jerry Moran (R-KS)",
            "Todd Young (R-IN)",
            "Cynthia Lummis (R-WY)",
            "Katie Britt (R-AL)",
            "JD Vance (R-OH)",
            "Eric Schmitt (R-MO)"
        ]
    }
    
    # Similar check for Commerce committee
    try:
        response = requests.get(f"{base_url}/api/v1/committees", timeout=10)
        if response.status_code == 200:
            committees = response.json()
            commerce_committee = None
            for committee in committees:
                if "Commerce" in committee.get('name', ''):
                    commerce_committee = committee
                    break
            
            if commerce_committee:
                print(f"Found committee: {commerce_committee['name']}")
                print(f"Committee ID: {commerce_committee['id']}")
                
                # Get members
                response = requests.get(f"{base_url}/api/v1/committees/{commerce_committee['id']}/members", timeout=10)
                if response.status_code == 200:
                    current_members = response.json()
                    print(f"Current members in system: {len(current_members)}")
                    print(f"Expected members: {len(known_commerce['Members']) + 2}")  # +2 for chair/ranking
                    
                    # Show current members
                    print("\nCurrent members in system:")
                    for member in current_members[:10]:  # Show first 10
                        name = f"{member.get('first_name', '')} {member.get('last_name', '')}"
                        state = member.get('state', 'Unknown')
                        party = member.get('party', 'Unknown')
                        print(f"  - {name} ({party}-{state})")
                    
                    if len(current_members) > 10:
                        print(f"  ... and {len(current_members) - 10} more")
                        
                else:
                    print(f"Error getting members: {response.status_code}")
            else:
                print("❌ Commerce Committee not found")
        else:
            print(f"Error getting committees: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    
    # Test 3: Check specific member assignments
    print("3. SPOT CHECK KNOWN MEMBER ASSIGNMENTS")
    print("-" * 38)
    
    # Known assignments to test
    test_cases = [
        ("Chuck Grassley", "Judiciary Committee (Ranking Member)"),
        ("Dick Durbin", "Judiciary Committee (Chair)"),
        ("Maria Cantwell", "Commerce Committee (Chair)"),
        ("Amy Klobuchar", "Judiciary + Commerce + Rules"),
        ("Ted Cruz", "Judiciary + Commerce (Ranking)")
    ]
    
    for member_name, expected_committees in test_cases:
        try:
            # Search for member
            response = requests.get(f"{base_url}/api/v1/members?search={member_name}", timeout=10)
            if response.status_code == 200:
                members = response.json()
                if members:
                    member = members[0]
                    print(f"\n{member_name}:")
                    print(f"  Found: {member.get('first_name')} {member.get('last_name')} ({member.get('party')}-{member.get('state')})")
                    print(f"  Expected: {expected_committees}")
                    
                    # Get member's committees
                    response = requests.get(f"{base_url}/api/v1/members/{member['id']}/committees", timeout=10)
                    if response.status_code == 200:
                        committees = response.json()
                        print(f"  Current committees: {len(committees)}")
                        for committee in committees:
                            print(f"    - {committee.get('name', 'Unknown')}")
                    else:
                        print(f"  Error getting committees: {response.status_code}")
                else:
                    print(f"{member_name}: Not found")
            else:
                print(f"{member_name}: Search error {response.status_code}")
        except Exception as e:
            print(f"{member_name}: Error {e}")
    
    print()
    
    # Test 4: Subcommittee check
    print("4. SUBCOMMITTEE ASSIGNMENT CHECK")
    print("-" * 32)
    
    try:
        response = requests.get(f"{base_url}/api/v1/committees", timeout=10)
        if response.status_code == 200:
            committees = response.json()
            
            # Count committees vs subcommittees
            committees_count = len([c for c in committees if not c.get('parent_committee_id')])
            subcommittees_count = len([c for c in committees if c.get('parent_committee_id')])
            
            print(f"Total committees: {len(committees)}")
            print(f"Standing committees: {committees_count}")  
            print(f"Subcommittees: {subcommittees_count}")
            
            if subcommittees_count > 0:
                print("\nSample subcommittees:")
                subcommittees = [c for c in committees if c.get('parent_committee_id')]
                for sub in subcommittees[:5]:
                    print(f"  - {sub.get('name', 'Unknown')}")
            else:
                print("❌ No subcommittees found in system")
                
        else:
            print(f"Error getting committees: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("🚨 AUDIT COMPLETE")
    print("=" * 50)
    print("RECOMMENDATION: Proceed with comprehensive committee data overhaul")
    print("All member-committee assignments should be considered unreliable")
    print("until verified against official Congressional sources.")

if __name__ == "__main__":
    audit_committee_accuracy()