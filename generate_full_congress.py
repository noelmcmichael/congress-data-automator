#!/usr/bin/env python3
"""
Generate complete congressional member data for all 535 members of Congress.
This creates realistic data for testing the full functionality.
"""
import json
import random
from datetime import datetime

def generate_full_congress_data():
    """Generate data for all 535 members of Congress (435 House + 100 Senate)."""
    
    # State data with representative counts
    states_data = {
        'AL': {'name': 'Alabama', 'house_seats': 7, 'senators': 2},
        'AK': {'name': 'Alaska', 'house_seats': 1, 'senators': 2},
        'AZ': {'name': 'Arizona', 'house_seats': 9, 'senators': 2},
        'AR': {'name': 'Arkansas', 'house_seats': 4, 'senators': 2},
        'CA': {'name': 'California', 'house_seats': 52, 'senators': 2},
        'CO': {'name': 'Colorado', 'house_seats': 8, 'senators': 2},
        'CT': {'name': 'Connecticut', 'house_seats': 5, 'senators': 2},
        'DE': {'name': 'Delaware', 'house_seats': 1, 'senators': 2},
        'FL': {'name': 'Florida', 'house_seats': 28, 'senators': 2},
        'GA': {'name': 'Georgia', 'house_seats': 14, 'senators': 2},
        'HI': {'name': 'Hawaii', 'house_seats': 2, 'senators': 2},
        'ID': {'name': 'Idaho', 'house_seats': 2, 'senators': 2},
        'IL': {'name': 'Illinois', 'house_seats': 17, 'senators': 2},
        'IN': {'name': 'Indiana', 'house_seats': 9, 'senators': 2},
        'IA': {'name': 'Iowa', 'house_seats': 4, 'senators': 2},
        'KS': {'name': 'Kansas', 'house_seats': 4, 'senators': 2},
        'KY': {'name': 'Kentucky', 'house_seats': 6, 'senators': 2},
        'LA': {'name': 'Louisiana', 'house_seats': 6, 'senators': 2},
        'ME': {'name': 'Maine', 'house_seats': 2, 'senators': 2},
        'MD': {'name': 'Maryland', 'house_seats': 8, 'senators': 2},
        'MA': {'name': 'Massachusetts', 'house_seats': 9, 'senators': 2},
        'MI': {'name': 'Michigan', 'house_seats': 13, 'senators': 2},
        'MN': {'name': 'Minnesota', 'house_seats': 8, 'senators': 2},
        'MS': {'name': 'Mississippi', 'house_seats': 4, 'senators': 2},
        'MO': {'name': 'Missouri', 'house_seats': 8, 'senators': 2},
        'MT': {'name': 'Montana', 'house_seats': 2, 'senators': 2},
        'NE': {'name': 'Nebraska', 'house_seats': 3, 'senators': 2},
        'NV': {'name': 'Nevada', 'house_seats': 4, 'senators': 2},
        'NH': {'name': 'New Hampshire', 'house_seats': 2, 'senators': 2},
        'NJ': {'name': 'New Jersey', 'house_seats': 12, 'senators': 2},
        'NM': {'name': 'New Mexico', 'house_seats': 3, 'senators': 2},
        'NY': {'name': 'New York', 'house_seats': 26, 'senators': 2},
        'NC': {'name': 'North Carolina', 'house_seats': 14, 'senators': 2},
        'ND': {'name': 'North Dakota', 'house_seats': 1, 'senators': 2},
        'OH': {'name': 'Ohio', 'house_seats': 15, 'senators': 2},
        'OK': {'name': 'Oklahoma', 'house_seats': 5, 'senators': 2},
        'OR': {'name': 'Oregon', 'house_seats': 6, 'senators': 2},
        'PA': {'name': 'Pennsylvania', 'house_seats': 17, 'senators': 2},
        'RI': {'name': 'Rhode Island', 'house_seats': 2, 'senators': 2},
        'SC': {'name': 'South Carolina', 'house_seats': 7, 'senators': 2},
        'SD': {'name': 'South Dakota', 'house_seats': 1, 'senators': 2},
        'TN': {'name': 'Tennessee', 'house_seats': 9, 'senators': 2},
        'TX': {'name': 'Texas', 'house_seats': 38, 'senators': 2},
        'UT': {'name': 'Utah', 'house_seats': 4, 'senators': 2},
        'VT': {'name': 'Vermont', 'house_seats': 1, 'senators': 2},
        'VA': {'name': 'Virginia', 'house_seats': 11, 'senators': 2},
        'WA': {'name': 'Washington', 'house_seats': 10, 'senators': 2},
        'WV': {'name': 'West Virginia', 'house_seats': 2, 'senators': 2},
        'WI': {'name': 'Wisconsin', 'house_seats': 8, 'senators': 2},
        'WY': {'name': 'Wyoming', 'house_seats': 1, 'senators': 2},
    }
    
    # Common names for generating realistic member data
    first_names = [
        'James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda',
        'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
        'Thomas', 'Sarah', 'Christopher', 'Karen', 'Charles', 'Nancy', 'Daniel', 'Lisa',
        'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra', 'Donald', 'Donna',
        'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle',
        'Kenneth', 'Laura', 'Kevin', 'Sarah', 'Brian', 'Kimberly', 'George', 'Deborah'
    ]
    
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
        'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
        'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
        'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill',
        'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell'
    ]
    
    parties = ['D', 'R', 'I']  # Democrat, Republican, Independent
    party_weights = [0.47, 0.50, 0.03]  # Rough distribution
    
    members = []
    member_id = 1
    
    print("Generating House members...")
    
    # Generate House members (435 total)
    district_counter = {}
    for state, data in states_data.items():
        for district in range(1, data['house_seats'] + 1):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            party = random.choices(parties, weights=party_weights)[0]
            
            member = {
                "id": member_id,
                "bioguide_id": f"H{member_id:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": random.choice([None, None, None, "J", "A", "M", "L"]),
                "nickname": None,
                "party": party,
                "chamber": "House",
                "state": state,
                "district": district,
                "is_current": True,
                "official_photo_url": None,
                "created_at": "2025-01-04T12:00:00Z",
                "updated_at": "2025-01-04T12:00:00Z",
                "last_scraped_at": "2025-01-04T12:00:00Z",
            }
            members.append(member)
            member_id += 1
    
    print(f"Generated {len(members)} House members")
    
    # Generate Senate members (100 total, 2 per state)
    print("Generating Senate members...")
    senate_start_id = member_id
    
    for state, data in states_data.items():
        for senator_num in range(1, 3):  # 2 senators per state
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            party = random.choices(parties, weights=party_weights)[0]
            
            member = {
                "id": member_id,
                "bioguide_id": f"S{member_id:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": random.choice([None, None, None, "J", "A", "M", "L"]),
                "nickname": None,
                "party": party,
                "chamber": "Senate",
                "state": state,
                "district": None,
                "is_current": True,
                "official_photo_url": None,
                "created_at": "2025-01-04T12:00:00Z",
                "updated_at": "2025-01-04T12:00:00Z",
                "last_scraped_at": "2025-01-04T12:00:00Z",
            }
            members.append(member)
            member_id += 1
    
    print(f"Generated {len(members) - 435} Senate members")
    
    # Verify totals
    house_count = sum(1 for m in members if m['chamber'] == 'House')
    senate_count = sum(1 for m in members if m['chamber'] == 'Senate')
    
    print(f"\nTotal members generated: {len(members)}")
    print(f"House: {house_count}")
    print(f"Senate: {senate_count}")
    
    # Save to file
    output_file = "frontend/src/data/fullCongressMembers.json"
    with open(output_file, "w") as f:
        json.dump(members, f, indent=2)
    
    print(f"\nData saved to {output_file}")
    
    # Generate summary statistics
    party_counts = {}
    for member in members:
        party = member['party']
        chamber = member['chamber']
        key = f"{chamber}_{party}"
        party_counts[key] = party_counts.get(key, 0) + 1
    
    print("\nParty breakdown:")
    print(f"House Democrats: {party_counts.get('House_D', 0)}")
    print(f"House Republicans: {party_counts.get('House_R', 0)}")
    print(f"House Independents: {party_counts.get('House_I', 0)}")
    print(f"Senate Democrats: {party_counts.get('Senate_D', 0)}")
    print(f"Senate Republicans: {party_counts.get('Senate_R', 0)}")
    print(f"Senate Independents: {party_counts.get('Senate_I', 0)}")
    
    return members

if __name__ == "__main__":
    generate_full_congress_data()