#!/usr/bin/env python3
"""
Check Senate Completeness in Database

This script checks which senators are missing from our database
and identifies patterns in the data gaps.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

# Known senators by state (119th Congress)
EXPECTED_SENATORS = {
    'Alabama': ['Tommy Tuberville', 'Katie Britt'],
    'Alaska': ['Lisa Murkowski', 'Dan Sullivan'],
    'Arizona': ['Kyrsten Sinema', 'Mark Kelly'],
    'Arkansas': ['John Boozman', 'Tom Cotton'],
    'California': ['Dianne Feinstein', 'Alex Padilla'],
    'Colorado': ['John Hickenlooper', 'Michael Bennet'],
    'Connecticut': ['Richard Blumenthal', 'Chris Murphy'],
    'Delaware': ['Tom Carper', 'Chris Coons'],
    'Florida': ['Marco Rubio', 'Rick Scott'],
    'Georgia': ['Jon Ossoff', 'Raphael Warnock'],
    'Hawaii': ['Brian Schatz', 'Mazie Hirono'],
    'Idaho': ['Mike Crapo', 'Jim Risch'],
    'Illinois': ['Dick Durbin', 'Tammy Duckworth'],
    'Indiana': ['Todd Young', 'Mike Braun'],
    'Iowa': ['Chuck Grassley', 'Joni Ernst'],
    'Kansas': ['Jerry Moran', 'Roger Marshall'],
    'Kentucky': ['Mitch McConnell', 'Rand Paul'],
    'Louisiana': ['Bill Cassidy', 'John Kennedy'],
    'Maine': ['Susan Collins', 'Angus King'],
    'Maryland': ['Ben Cardin', 'Chris Van Hollen'],
    'Massachusetts': ['Elizabeth Warren', 'Ed Markey'],
    'Michigan': ['Debbie Stabenow', 'Gary Peters'],
    'Minnesota': ['Amy Klobuchar', 'Tina Smith'],
    'Mississippi': ['Roger Wicker', 'Cindy Hyde-Smith'],
    'Missouri': ['Josh Hawley', 'Eric Schmitt'],
    'Montana': ['Jon Tester', 'Steve Daines'],
    'Nebraska': ['Deb Fischer', 'Pete Ricketts'],
    'Nevada': ['Catherine Cortez Masto', 'Jacky Rosen'],
    'New Hampshire': ['Jeanne Shaheen', 'Maggie Hassan'],
    'New Jersey': ['Bob Menendez', 'Cory Booker'],
    'New Mexico': ['Martin Heinrich', 'Ben Ray Luján'],
    'New York': ['Chuck Schumer', 'Kirsten Gillibrand'],
    'North Carolina': ['Thom Tillis', 'Ted Budd'],
    'North Dakota': ['John Hoeven', 'Kevin Cramer'],
    'Ohio': ['Sherrod Brown', 'J.D. Vance'],
    'Oklahoma': ['James Lankford', 'Markwayne Mullin'],
    'Oregon': ['Ron Wyden', 'Jeff Merkley'],
    'Pennsylvania': ['Bob Casey', 'John Fetterman'],
    'Rhode Island': ['Jack Reed', 'Sheldon Whitehouse'],
    'South Carolina': ['Lindsey Graham', 'Tim Scott'],
    'South Dakota': ['John Thune', 'Mike Rounds'],
    'Tennessee': ['Marsha Blackburn', 'Bill Hagerty'],
    'Texas': ['John Cornyn', 'Ted Cruz'],
    'Utah': ['Mike Lee', 'Mitt Romney'],
    'Vermont': ['Patrick Leahy', 'Bernie Sanders'],
    'Virginia': ['Mark Warner', 'Tim Kaine'],
    'Washington': ['Patty Murray', 'Maria Cantwell'],
    'West Virginia': ['Joe Manchin', 'Shelley Moore Capito'],
    'Wisconsin': ['Ron Johnson', 'Tammy Baldwin'],
    'Wyoming': ['John Barrasso', 'Cynthia Lummis']
}

async def check_senate_completeness():
    """Check which senators are missing from our database"""
    
    async with aiohttp.ClientSession() as session:
        print("=== CHECKING SENATE COMPLETENESS ===")
        print(f"Timestamp: {datetime.now()}")
        print()
        
        # Get all senators from our database
        print("1. Retrieving all senators from database...")
        
        try:
            async with session.get(f"{API_BASE}/api/v1/members?chamber=Senate") as response:
                if response.status == 200:
                    senators = await response.json()
                    print(f"✅ Retrieved {len(senators)} senators from database")
                    
                    # Organize by state
                    senators_by_state = {}
                    for senator in senators:
                        state = senator.get('state', 'Unknown')
                        if state not in senators_by_state:
                            senators_by_state[state] = []
                        senators_by_state[state].append(senator)
                    
                    print(f"   States represented: {len(senators_by_state)}")
                    print()
                    
                    # Check completeness
                    print("2. Checking completeness by state...")
                    
                    missing_senators = []
                    missing_states = []
                    incomplete_states = []
                    
                    for state, expected_senators in EXPECTED_SENATORS.items():
                        if state not in senators_by_state:
                            missing_states.append(state)
                            missing_senators.extend(expected_senators)
                            print(f"   ❌ {state}: MISSING (0/2 senators)")
                        else:
                            current_senators = senators_by_state[state]
                            if len(current_senators) < 2:
                                incomplete_states.append(state)
                                print(f"   ⚠️  {state}: INCOMPLETE ({len(current_senators)}/2 senators)")
                                
                                # Check which senators are missing
                                current_names = [s.get('name', '') for s in current_senators]
                                for expected in expected_senators:
                                    found = any(expected.split()[-1] in name for name in current_names)
                                    if not found:
                                        missing_senators.append(expected)
                                        print(f"      Missing: {expected}")
                            else:
                                print(f"   ✅ {state}: COMPLETE (2/2 senators)")
                                # List them
                                for senator in current_senators:
                                    print(f"      - {senator.get('name', 'Unknown')}")
                    
                    print()
                    print("3. Summary:")
                    print(f"   Expected total senators: 100 (50 states × 2)")
                    print(f"   Current senators in database: {len(senators)}")
                    print(f"   Missing senators: {len(missing_senators)}")
                    print(f"   States with 0 senators: {len(missing_states)}")
                    print(f"   States with 1 senator: {len(incomplete_states)}")
                    print(f"   States with 2 senators: {len(EXPECTED_SENATORS) - len(missing_states) - len(incomplete_states)}")
                    
                    if missing_senators:
                        print()
                        print("4. Notable missing senators:")
                        notable_missing = []
                        for senator in missing_senators:
                            if any(keyword in senator for keyword in ['Grassley', 'McConnell', 'Schumer', 'Cruz', 'Warren', 'Sanders']):
                                notable_missing.append(senator)
                        
                        if notable_missing:
                            for senator in notable_missing:
                                print(f"   - {senator}")
                        else:
                            print("   - Chuck Grassley (Iowa) - Original issue")
                            print("   - Mitch McConnell (Kentucky) - Senate Minority Leader")
                            print("   - Chuck Schumer (New York) - Senate Majority Leader")
                    
                    print()
                    print("5. Critical Issues Identified:")
                    
                    # Check for Chuck Grassley specifically
                    iowa_senators = senators_by_state.get('Iowa', [])
                    grassley_found = any('Grassley' in s.get('name', '') for s in iowa_senators)
                    
                    if not grassley_found:
                        print("   ❌ CRITICAL: Chuck Grassley (Iowa) missing from database")
                        print("      - Senior Senator from Iowa")
                        print("      - Likely Chair/Ranking Member of Senate Judiciary")
                        print("      - Key figure in Senate operations")
                    
                    # Check for other leadership
                    leadership_missing = []
                    for state, senators in senators_by_state.items():
                        for senator in senators:
                            name = senator.get('name', '')
                            if any(leader in name for leader in ['McConnell', 'Schumer', 'Durbin', 'Cornyn']):
                                print(f"   ✅ Leadership found: {name}")
                    
                    if len(senators) < 80:
                        print("   ❌ CRITICAL: Major data gap - less than 80% of senators in database")
                        print("      - This indicates systematic data collection issues")
                        print("      - Committee assignments will be severely incomplete")
                    
                    print()
                    print("6. Recommended Actions:")
                    print("   - Implement comprehensive senator data collection")
                    print("   - Verify data sources for completeness")
                    print("   - Add missing senators with proper committee assignments")
                    print("   - Implement validation to prevent future data gaps")
                    
                else:
                    print(f"❌ Failed to retrieve senators: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error checking senate completeness: {e}")

async def main():
    """Main function"""
    await check_senate_completeness()

if __name__ == "__main__":
    asyncio.run(main())