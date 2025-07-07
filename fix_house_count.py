#!/usr/bin/env python3
"""
Fix House member count to reach 441 total
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import time
from datetime import datetime

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def get_state_mapping():
    """Get mapping from full state names to 2-character codes"""
    return {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY',
        # Territories
        'American Samoa': 'AS', 'District of Columbia': 'DC', 'Guam': 'GU',
        'Northern Mariana Islands': 'MP', 'Puerto Rico': 'PR', 'Virgin Islands': 'VI'
    }

def analyze_house_composition():
    """Analyze current House composition"""
    
    conn = connect_to_database()
    if not conn:
        return False
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get current House composition
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN district IS NULL OR district = '' THEN 'Non-voting'
                    ELSE 'Voting'
                END as member_type,
                COUNT(*) as count
            FROM members
            WHERE chamber = 'House'
            GROUP BY 
                CASE 
                    WHEN district IS NULL OR district = '' THEN 'Non-voting'
                    ELSE 'Voting'
                END
            ORDER BY member_type
        """)
        
        composition = cursor.fetchall()
        
        print("📊 CURRENT HOUSE COMPOSITION:")
        total_house = 0
        for comp in composition:
            print(f"   {comp['member_type']}: {comp['count']}")
            total_house += comp['count']
        
        print(f"   TOTAL: {total_house}")
        print(f"   TARGET: 441 (435 voting + 6 non-voting)")
        print(f"   SHORTFALL: {441 - total_house}")
        
        # Check non-voting delegates/commissioners
        cursor.execute("""
            SELECT state, COUNT(*) as count
            FROM members
            WHERE chamber = 'House' AND (district IS NULL OR district = '')
            GROUP BY state
            ORDER BY state
        """)
        
        non_voting_by_state = cursor.fetchall()
        
        print("\n📋 NON-VOTING DELEGATES/COMMISSIONERS:")
        territories = ['AS', 'DC', 'GU', 'MP', 'PR', 'VI']
        
        for territory in territories:
            found = False
            for state_data in non_voting_by_state:
                if state_data['state'] == territory:
                    print(f"   {territory}: {state_data['count']} delegate(s)")
                    found = True
                    break
            if not found:
                print(f"   {territory}: 0 delegates (MISSING)")
        
        # Get details of non-voting members
        cursor.execute("""
            SELECT state, first_name, last_name, party, district
            FROM members
            WHERE chamber = 'House' AND (district IS NULL OR district = '')
            ORDER BY state, last_name
        """)
        
        non_voting_details = cursor.fetchall()
        
        print("\n📋 NON-VOTING MEMBERS DETAILS:")
        for member in non_voting_details:
            print(f"   {member['first_name']} {member['last_name']} ({member['party']}-{member['state']})")
        
        cursor.close()
        conn.close()
        
        return total_house, 441 - total_house
        
    except Exception as e:
        print(f"Error analyzing House composition: {e}")
        cursor.close()
        conn.close()
        return False, 0

def fetch_house_members_from_api():
    """Fetch House members from Congress.gov API"""
    
    api_key = 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG'
    base_url = "https://api.congress.gov/v3"
    
    print(f"\n🔍 FETCHING HOUSE MEMBERS FROM CONGRESS.GOV API")
    
    all_representatives = []
    offset = 0
    limit = 250
    
    while True:
        url = f"{base_url}/member/congress/119"
        params = {
            'api_key': api_key,
            'format': 'json',
            'offset': offset,
            'limit': limit
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            members = data.get('members', [])
            
            print(f"   Fetched {len(members)} members (offset {offset})")
            
            # Filter for House members
            representatives_in_batch = []
            for member in members:
                terms = member.get('terms', {}).get('item', [])
                if terms:
                    # Get the most recent term
                    latest_term = terms[-1]
                    chamber = latest_term.get('chamber', '')
                    
                    if chamber == 'House of Representatives':
                        representatives_in_batch.append(member)
            
            print(f"   Found {len(representatives_in_batch)} House members in this batch")
            all_representatives.extend(representatives_in_batch)
            
            # Check if there are more pages
            if len(members) < limit:
                break
                
            offset += limit
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"   Error fetching data: {e}")
            break
    
    print(f"   Total House members fetched: {len(all_representatives)}")
    return all_representatives

def process_house_member_data(member_data):
    """Process House member data into database format"""
    
    # Extract basic information
    name = member_data.get('name', '')
    bio_guide_id = member_data.get('bioguideId', '')
    
    # Parse name (format: "Last, First Middle")
    name_parts = name.split(', ')
    last_name = name_parts[0] if len(name_parts) > 0 else ''
    first_part = name_parts[1] if len(name_parts) > 1 else ''
    
    # Split first part into first and middle names
    first_parts = first_part.split(' ')
    first_name = first_parts[0] if len(first_parts) > 0 else ''
    middle_name = ' '.join(first_parts[1:]) if len(first_parts) > 1 else ''
    
    # Handle terms and district
    terms = member_data.get('terms', {}).get('item', [])
    district = member_data.get('district')
    
    # Convert full state name to 2-character code
    state_mapping = get_state_mapping()
    full_state_name = member_data.get('state', '')
    state_code = state_mapping.get(full_state_name, full_state_name)
    
    # Build member record
    member = {
        'bioguide_id': bio_guide_id,
        'congress_gov_id': None,
        'first_name': first_name,
        'last_name': last_name,
        'middle_name': middle_name,
        'suffix': '',
        'nickname': '',
        'party': member_data.get('partyName', ''),
        'chamber': 'House',
        'state': state_code,
        'district': str(district) if district else None,
        'term_start': None,
        'term_end': None,
        'is_current': True,
        'birth_date': None,
        'birth_state': None,
        'birth_city': None,
        'official_photo_url': member_data.get('depiction', {}).get('imageUrl', ''),
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'last_scraped_at': datetime.now()
    }
    
    # Process term dates
    if terms:
        current_term = terms[-1]
        start_date = current_term.get('startYear')
        end_date = current_term.get('endYear')
        
        if start_date:
            member['term_start'] = f"{start_date}-01-01"
        if end_date:
            member['term_end'] = f"{end_date}-12-31"
        else:
            # House terms are 2 years
            member['term_end'] = f"{start_date + 2}-12-31"
    
    return member

def add_missing_house_members():
    """Add missing House members"""
    
    # Analyze current composition
    current_count, shortfall = analyze_house_composition()
    
    if not current_count:
        return False
    
    if shortfall <= 0:
        print("✅ House already has correct number of members")
        return True
    
    # Fetch House members from API
    api_house_members = fetch_house_members_from_api()
    
    if not api_house_members:
        print("❌ Failed to fetch House members from API")
        return False
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return False
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get existing House members
        cursor.execute("""
            SELECT bioguide_id, state, district
            FROM members
            WHERE chamber = 'House'
        """)
        existing_house = cursor.fetchall()
        existing_bioguide_ids = {m['bioguide_id'] for m in existing_house}
        
        # Process API House members
        processed_members = []
        for member_data in api_house_members:
            member = process_house_member_data(member_data)
            if member['bioguide_id'] not in existing_bioguide_ids:
                processed_members.append(member)
        
        print(f"\n📋 HOUSE MEMBERS TO ADD:")
        print(f"   API House Members: {len(api_house_members)}")
        print(f"   Existing House Members: {len(existing_house)}")
        print(f"   New House Members: {len(processed_members)}")
        print(f"   Shortfall to fix: {shortfall}")
        
        # Add new House members (up to shortfall)
        added_count = 0
        for member in processed_members[:shortfall]:
            cursor.execute("""
                INSERT INTO members (
                    bioguide_id, congress_gov_id, first_name, last_name, middle_name,
                    suffix, nickname, party, chamber, state, district, 
                    term_start, term_end, is_current, official_photo_url,
                    created_at, updated_at, last_scraped_at
                ) VALUES (
                    %(bioguide_id)s, %(congress_gov_id)s, %(first_name)s, %(last_name)s, %(middle_name)s,
                    %(suffix)s, %(nickname)s, %(party)s, %(chamber)s, %(state)s, %(district)s,
                    %(term_start)s, %(term_end)s, %(is_current)s, %(official_photo_url)s,
                    %(created_at)s, %(updated_at)s, %(last_scraped_at)s
                )
            """, member)
            
            district_str = f" District {member['district']}" if member['district'] else " (Non-voting)"
            print(f"   ✅ Added: {member['first_name']} {member['last_name']} ({member['party']}-{member['state']}{district_str})")
            added_count += 1
        
        # Commit changes
        conn.commit()
        
        print(f"\n🎉 Successfully added {added_count} House members")
        
        return True
        
    except Exception as e:
        print(f"Error adding House members: {e}")
        conn.rollback()
        return False
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=== FIXING HOUSE MEMBER COUNT ===\n")
    
    if add_missing_house_members():
        print("\n=== FINAL VERIFICATION ===")
        analyze_house_composition()
    else:
        print("\n❌ Failed to fix House member count!")