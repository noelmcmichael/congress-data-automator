#!/usr/bin/env python3
"""
Complete Senate representation by fetching missing senators
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import logging
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API key from keyring
import keyring

def get_api_key():
    """Get Congress API key from keyring"""
    try:
        # Try different case variations
        for key_name in ['CONGRESS_API_KEY', 'congress_api_key', 'Congress API Key']:
            try:
                api_key = keyring.get_password('memex', key_name)
                if api_key:
                    return api_key
            except:
                continue
        
        # Fallback to environment variable
        return os.getenv('CONGRESS_API_KEY', 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG')
    except:
        return 'NcMVmULsduvTXfEIXhKgAb1uWDDFdzOcPI57jpRG'

def connect_to_database():
    """Connect to the production database via Cloud SQL proxy"""
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
        logger.error(f"Database connection error: {e}")
        return None

def get_missing_senators():
    """Get list of states that need senators"""
    
    conn = connect_to_database()
    if not conn:
        return []
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get states with only 1 senator
        cursor.execute("""
            SELECT state, COUNT(*) as senator_count
            FROM members
            WHERE chamber = 'Senate'
            GROUP BY state
            HAVING COUNT(*) < 2
            ORDER BY state
        """)
        
        missing_states = cursor.fetchall()
        
        # Get existing senators by state
        cursor.execute("""
            SELECT state, first_name, last_name, party, bioguide_id
            FROM members
            WHERE chamber = 'Senate'
            ORDER BY state, last_name
        """)
        
        existing_senators = cursor.fetchall()
        
        # Group by state
        senators_by_state = {}
        for senator in existing_senators:
            state = senator['state']
            if state not in senators_by_state:
                senators_by_state[state] = []
            senators_by_state[state].append(senator)
        
        print(f"📊 SENATE REPRESENTATION ANALYSIS:")
        print(f"   States with 1 senator: {len(missing_states)}")
        print(f"   States with 2 senators: {50 - len(missing_states)}")
        
        print(f"\n🚨 STATES NEEDING SENATORS:")
        for state_info in missing_states:
            state = state_info['state']
            existing = senators_by_state.get(state, [])
            print(f"   {state}: {len(existing)}/2 senators")
            for senator in existing:
                print(f"     - {senator['first_name']} {senator['last_name']} ({senator['party']})")
        
        return missing_states
        
    except Exception as e:
        logger.error(f"Error getting missing senators: {e}")
        return []
    
    finally:
        cursor.close()
        conn.close()

def fetch_senators_from_api(congress_num=119):
    """Fetch all senators from Congress.gov API"""
    
    api_key = get_api_key()
    base_url = "https://api.congress.gov/v3"
    
    print(f"\n🔍 FETCHING SENATORS FROM CONGRESS.GOV API")
    print(f"   Congress: {congress_num}")
    print(f"   API Key: {'*' * 20}...{api_key[-4:]}")
    
    all_senators = []
    offset = 0
    limit = 250
    
    while True:
        url = f"{base_url}/member/congress/{congress_num}"
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
            
            # Filter for senators
            senators_in_batch = []
            for member in members:
                terms = member.get('terms', {}).get('item', [])
                if terms:
                    # Get the most recent term
                    latest_term = terms[-1]
                    chamber = latest_term.get('chamber', '')
                    
                    if chamber == 'Senate':
                        senators_in_batch.append(member)
            
            print(f"   Found {len(senators_in_batch)} senators in this batch")
            all_senators.extend(senators_in_batch)
            
            # Check if there are more pages
            if len(members) < limit:
                break
                
            offset += limit
            time.sleep(0.5)  # Rate limiting
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            break
    
    print(f"   Total senators fetched: {len(all_senators)}")
    return all_senators

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

def process_senator_data(senator_data):
    """Process a senator's data into database format"""
    
    # Extract basic information
    name = senator_data.get('name', '')
    bio_guide_id = senator_data.get('bioguideId', '')
    
    # Parse name (format: "Last, First Middle")
    name_parts = name.split(', ')
    last_name = name_parts[0] if len(name_parts) > 0 else ''
    first_part = name_parts[1] if len(name_parts) > 1 else ''
    
    # Split first part into first and middle names
    first_parts = first_part.split(' ')
    first_name = first_parts[0] if len(first_parts) > 0 else ''
    middle_name = ' '.join(first_parts[1:]) if len(first_parts) > 1 else ''
    
    # Handle terms
    terms = senator_data.get('terms', {}).get('item', [])
    current_term = None
    
    if terms:
        # Get the most recent term
        current_term = terms[-1]
    
    # Convert full state name to 2-character code
    state_mapping = get_state_mapping()
    full_state_name = senator_data.get('state', '')
    state_code = state_mapping.get(full_state_name, full_state_name)
    
    # Build member record
    member = {
        'bioguide_id': bio_guide_id,
        'congress_gov_id': None,  # Set to None to avoid constraint issues
        'first_name': first_name,
        'last_name': last_name,
        'middle_name': middle_name,
        'suffix': '',
        'nickname': '',
        'party': senator_data.get('partyName', ''),
        'chamber': 'Senate',
        'state': state_code,
        'district': None,  # Senators don't have districts
        'term_start': None,
        'term_end': None,
        'is_current': True,
        'birth_date': None,
        'birth_state': None,
        'birth_city': None,
        'official_photo_url': senator_data.get('depiction', {}).get('imageUrl', ''),
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'last_scraped_at': datetime.now()
    }
    
    # Process term dates
    if current_term:
        start_date = current_term.get('startYear')
        end_date = current_term.get('endYear')
        
        if start_date:
            member['term_start'] = f"{start_date}-01-01"
        if end_date:
            member['term_end'] = f"{end_date}-12-31"
        else:
            # If no end date, assume it's current term ending in 2031 (6-year term)
            member['term_end'] = f"{start_date + 6}-12-31"
    
    return member

def add_missing_senators():
    """Add missing senators to database"""
    
    # Get missing senators
    missing_states = get_missing_senators()
    if not missing_states:
        print("✅ All states have 2 senators")
        return True
    
    # Fetch all senators from API
    api_senators = fetch_senators_from_api()
    if not api_senators:
        print("❌ Failed to fetch senators from API")
        return False
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return False
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get existing senators
        cursor.execute("""
            SELECT bioguide_id, state
            FROM members
            WHERE chamber = 'Senate'
        """)
        existing_senators = cursor.fetchall()
        existing_bioguide_ids = {s['bioguide_id'] for s in existing_senators}
        
        # Process API senators
        processed_senators = []
        for senator_data in api_senators:
            member = process_senator_data(senator_data)
            if member['bioguide_id'] not in existing_bioguide_ids:
                processed_senators.append(member)
        
        print(f"\n📋 SENATORS TO ADD:")
        print(f"   API Senators: {len(api_senators)}")
        print(f"   Existing Senators: {len(existing_senators)}")
        print(f"   New Senators: {len(processed_senators)}")
        
        # Add new senators or update existing ones
        added_count = 0
        updated_count = 0
        
        for member in processed_senators:
            # Check if this senator already exists
            cursor.execute("""
                SELECT id, chamber FROM members 
                WHERE bioguide_id = %s
            """, (member['bioguide_id'],))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record if it's not already a senator
                if existing['chamber'] != 'Senate':
                    cursor.execute("""
                        UPDATE members SET
                            chamber = 'Senate',
                            district = NULL,
                            term_start = %(term_start)s,
                            term_end = %(term_end)s,
                            official_photo_url = %(official_photo_url)s,
                            updated_at = %(updated_at)s,
                            last_scraped_at = %(last_scraped_at)s
                        WHERE bioguide_id = %(bioguide_id)s
                    """, member)
                    
                    print(f"   🔄 Updated: {member['first_name']} {member['last_name']} ({member['party']}-{member['state']}) - House → Senate")
                    updated_count += 1
                else:
                    print(f"   ✅ Already exists: {member['first_name']} {member['last_name']} ({member['party']}-{member['state']})")
            else:
                # Insert new record
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
                
                print(f"   ✅ Added: {member['first_name']} {member['last_name']} ({member['party']}-{member['state']})")
                added_count += 1
        
        # Commit changes
        conn.commit()
        
        print(f"\n🎉 Successfully processed senators:")
        print(f"   Added: {added_count}")
        print(f"   Updated: {updated_count}")
        print(f"   Total: {added_count + updated_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding senators: {e}")
        conn.rollback()
        return False
    
    finally:
        cursor.close()
        conn.close()

def verify_senate_completion():
    """Verify that all 50 states have 2 senators"""
    
    conn = connect_to_database()
    if not conn:
        return False
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Check total senate count
        cursor.execute("""
            SELECT COUNT(*) as total_senators
            FROM members
            WHERE chamber = 'Senate'
        """)
        total = cursor.fetchone()
        
        # Check states with missing senators
        cursor.execute("""
            SELECT state, COUNT(*) as senator_count
            FROM members
            WHERE chamber = 'Senate'
            GROUP BY state
            HAVING COUNT(*) < 2
            ORDER BY state
        """)
        missing_states = cursor.fetchall()
        
        # Check states with too many senators
        cursor.execute("""
            SELECT state, COUNT(*) as senator_count
            FROM members
            WHERE chamber = 'Senate'
            GROUP BY state
            HAVING COUNT(*) > 2
            ORDER BY state
        """)
        excess_states = cursor.fetchall()
        
        print(f"\n📊 SENATE COMPLETION VERIFICATION:")
        print(f"   Total Senators: {total['total_senators']}/100")
        print(f"   States with 1 senator: {len(missing_states)}")
        print(f"   States with >2 senators: {len(excess_states)}")
        
        if missing_states:
            print(f"\n🚨 STATES STILL MISSING SENATORS:")
            for state in missing_states:
                print(f"   {state['state']}: {state['senator_count']}/2")
        
        if excess_states:
            print(f"\n⚠️  STATES WITH EXCESS SENATORS:")
            for state in excess_states:
                print(f"   {state['state']}: {state['senator_count']}/2")
        
        success = total['total_senators'] == 100 and len(missing_states) == 0 and len(excess_states) == 0
        
        if success:
            print(f"\n✅ Senate representation complete: 100/100 senators")
        else:
            print(f"\n❌ Senate representation incomplete")
        
        return success
        
    except Exception as e:
        logger.error(f"Error verifying senate completion: {e}")
        return False
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=== COMPLETING SENATE REPRESENTATION ===\n")
    
    if add_missing_senators():
        print("\n=== VERIFICATION ===")
        verify_senate_completion()
    else:
        print("\n❌ Failed to complete Senate representation!")