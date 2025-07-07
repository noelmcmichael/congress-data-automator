#!/usr/bin/env python3
"""
Examine Current Senators in Database

This script examines what senators we actually have in the database
to understand the nature of the data collection issue.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Production API base URL
API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"

async def examine_current_senators():
    """Examine what senators we currently have in the database"""
    
    async with aiohttp.ClientSession() as session:
        print("=== EXAMINING CURRENT SENATORS IN DATABASE ===")
        print(f"Timestamp: {datetime.now()}")
        print()
        
        # Get all senators from our database
        print("1. Retrieving all senators from database...")
        
        try:
            async with session.get(f"{API_BASE}/api/v1/members?chamber=Senate") as response:
                if response.status == 200:
                    senators = await response.json()
                    print(f"✅ Retrieved {len(senators)} senators from database")
                    print()
                    
                    print("2. Current senators in database:")
                    
                    # Group by state
                    senators_by_state = {}
                    for senator in senators:
                        state = senator.get('state', 'Unknown')
                        if state not in senators_by_state:
                            senators_by_state[state] = []
                        senators_by_state[state].append(senator)
                    
                    # Sort states for consistent output
                    for state in sorted(senators_by_state.keys()):
                        state_senators = senators_by_state[state]
                        print(f"   {state}: {len(state_senators)} senators")
                        
                        for senator in state_senators:
                            name = senator.get('name', 'Unknown')
                            party = senator.get('party', 'Unknown')
                            district = senator.get('district', 'At Large')
                            print(f"      - {name} ({party}) - District: {district}")
                    
                    print()
                    print("3. Data Quality Analysis:")
                    
                    # Check for suspicious patterns
                    states_with_data = list(senators_by_state.keys())
                    print(f"   States represented: {len(states_with_data)}")
                    print(f"   States with data: {', '.join(sorted(states_with_data))}")
                    
                    # Look for patterns
                    if 'Unknown' in states_with_data:
                        unknown_count = len(senators_by_state['Unknown'])
                        print(f"   ⚠️  {unknown_count} senators with 'Unknown' state")
                    
                    # Check for non-state entries (maybe territories or districts)
                    non_state_entries = []
                    for state in states_with_data:
                        if state not in ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']:
                            non_state_entries.append(state)
                    
                    if non_state_entries:
                        print(f"   ⚠️  Non-state entries found: {', '.join(non_state_entries)}")
                        print("      This suggests data collection from House districts or territories")
                    
                    # Check for duplicates
                    all_names = [s.get('name', '') for s in senators]
                    unique_names = set(all_names)
                    if len(all_names) != len(unique_names):
                        print(f"   ⚠️  Duplicate names detected: {len(all_names)} total vs {len(unique_names)} unique")
                    
                    # Check party distribution
                    party_counts = {}
                    for senator in senators:
                        party = senator.get('party', 'Unknown')
                        party_counts[party] = party_counts.get(party, 0) + 1
                    
                    print()
                    print("4. Party Distribution:")
                    for party, count in sorted(party_counts.items()):
                        print(f"   {party}: {count} senators")
                    
                    print()
                    print("5. Sample Senator Data:")
                    if senators:
                        sample = senators[0]
                        print(f"   Sample record structure:")
                        for key, value in sample.items():
                            print(f"      {key}: {value}")
                    
                    print()
                    print("6. Hypothesis about Data Issue:")
                    
                    # Look for patterns that might explain the issue
                    has_districts = any(s.get('district') and s.get('district') != 'At Large' for s in senators)
                    if has_districts:
                        print("   ❌ LIKELY ISSUE: Senators have district numbers")
                        print("      This suggests House representatives are being labeled as senators")
                        print("      Senators should only have 'At Large' or null districts")
                    
                    non_at_large = [s for s in senators if s.get('district') not in ['At Large', None, '']]
                    if non_at_large:
                        print(f"   ❌ CONFIRMED: {len(non_at_large)} senators have specific districts")
                        print("      Examples:")
                        for senator in non_at_large[:5]:  # Show first 5
                            print(f"         - {senator.get('name')} ({senator.get('state')}) - District {senator.get('district')}")
                    
                    print()
                    print("7. Recommended Fix:")
                    print("   - Check data source query - likely mixing House and Senate data")
                    print("   - Verify chamber filter is working correctly")
                    print("   - Re-run data collection with proper Senate-only filtering")
                    print("   - Validate state names match expected US states")
                    print("   - Ensure districts are 'At Large' for all senators")
                    
                else:
                    print(f"❌ Failed to retrieve senators: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error examining senators: {e}")

async def main():
    """Main function"""
    await examine_current_senators()

if __name__ == "__main__":
    asyncio.run(main())