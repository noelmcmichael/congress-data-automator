#!/usr/bin/env python3
"""
Fix 119th Congress Senate Committee Leadership
Update from 118th Democratic leadership to 119th Republican leadership
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'congress_data',
    'user': 'postgres',
    'password': 'mDf3S9ZnBpQqJvGsY1'
}

# 119th Congress Senate Committee Leadership Updates
# Based on Republican majority control (51-49)
LEADERSHIP_UPDATES = {
    # Committee ID 189: Senate Judiciary
    189: {
        'new_chair': {'name': 'Chuck Grassley', 'party': 'Republican', 'state': 'IA'},
        'new_ranking': {'name': 'Richard Durbin', 'party': 'Democratic', 'state': 'IL'},
        'committee_name': 'Committee on the Judiciary'
    },
    # Committee ID 149: Commerce, Science, and Transportation  
    149: {
        'new_chair': {'name': 'Ted Cruz', 'party': 'Republican', 'state': 'TX'},
        'new_ranking': {'name': 'Maria Cantwell', 'party': 'Democratic', 'state': 'WA'},
        'committee_name': 'Committee on Commerce, Science, and Transportation'
    }
}

def connect_to_database():
    """Connect to the production database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def find_member_by_name_state(cursor, first_name, last_name, state):
    """Find member ID by name and state"""
    cursor.execute("""
        SELECT id, first_name, last_name, party, state 
        FROM members 
        WHERE LOWER(first_name) = LOWER(%s) 
        AND LOWER(last_name) = LOWER(%s) 
        AND state = %s
        AND chamber = 'Senate'
    """, (first_name, last_name, state))
    
    result = cursor.fetchone()
    return result

def get_current_leadership(cursor, committee_id):
    """Get current committee leadership"""
    cursor.execute("""
        SELECT cm.member_id, cm.position, m.first_name, m.last_name, m.party, m.state
        FROM committee_memberships cm
        JOIN members m ON cm.member_id = m.id
        WHERE cm.committee_id = %s 
        AND cm.position IN ('chair', 'ranking_member')
        AND cm.is_current = true
    """, (committee_id,))
    
    return cursor.fetchall()

def update_leadership_position(cursor, committee_id, member_id, new_position):
    """Update member's leadership position on committee"""
    # First, remove any existing leadership positions for this committee
    cursor.execute("""
        UPDATE committee_memberships 
        SET position = 'member'
        WHERE committee_id = %s 
        AND position IN ('chair', 'ranking_member')
        AND is_current = true
    """, (committee_id,))
    
    # Check if member already has a membership record
    cursor.execute("""
        SELECT id FROM committee_memberships 
        WHERE committee_id = %s AND member_id = %s
    """, (committee_id, member_id))
    
    existing = cursor.fetchone()
    
    if existing:
        # Update existing membership
        cursor.execute("""
            UPDATE committee_memberships 
            SET position = %s, is_current = true
            WHERE committee_id = %s AND member_id = %s
        """, (new_position, committee_id, member_id))
    else:
        # Insert new membership
        cursor.execute("""
            INSERT INTO committee_memberships (committee_id, member_id, position, is_current)
            VALUES (%s, %s, %s, true)
        """, (committee_id, member_id, new_position))

def fix_committee_leadership():
    """Fix all Senate committee leadership for 119th Congress"""
    print("=" * 60)
    print("119TH CONGRESS SENATE LEADERSHIP FIX")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    conn = connect_to_database()
    if not conn:
        print("Failed to connect to database")
        return False
    
    results = []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            for committee_id, update_info in LEADERSHIP_UPDATES.items():
                print(f"Updating: {update_info['committee_name']}")
                print("-" * 40)
                
                # Get current leadership
                current = get_current_leadership(cursor, committee_id)
                print("Current leadership:")
                for leader in current:
                    print(f"  {leader['position']}: {leader['first_name']} {leader['last_name']} ({leader['party'][0]}) - {leader['state']}")
                
                # Find new chair
                chair_info = update_info['new_chair']
                chair_member = find_member_by_name_state(
                    cursor, 
                    chair_info['name'].split()[0],  # First name
                    chair_info['name'].split()[-1], # Last name  
                    chair_info['state']
                )
                
                if not chair_member:
                    print(f"  ❌ Chair not found: {chair_info['name']} ({chair_info['state']})")
                    continue
                
                # Find new ranking member
                ranking_info = update_info['new_ranking']
                ranking_member = find_member_by_name_state(
                    cursor,
                    ranking_info['name'].split()[0],  # First name
                    ranking_info['name'].split()[-1], # Last name
                    ranking_info['state']
                )
                
                if not ranking_member:
                    print(f"  ❌ Ranking Member not found: {ranking_info['name']} ({ranking_info['state']})")
                    continue
                
                # Update leadership positions
                print("Updating to 119th Congress leadership:")
                
                # Update chair
                update_leadership_position(cursor, committee_id, chair_member['id'], 'chair')
                print(f"  ✅ Chair: {chair_member['first_name']} {chair_member['last_name']} (R) - {chair_member['state']}")
                
                # Update ranking member  
                update_leadership_position(cursor, committee_id, ranking_member['id'], 'ranking_member')
                print(f"  ✅ Ranking: {ranking_member['first_name']} {ranking_member['last_name']} (D) - {ranking_member['state']}")
                
                results.append({
                    'committee_id': committee_id,
                    'committee_name': update_info['committee_name'],
                    'new_chair': f"{chair_member['first_name']} {chair_member['last_name']} (R)",
                    'new_ranking': f"{ranking_member['first_name']} {ranking_member['last_name']} (D)",
                    'status': 'updated'
                })
                
                print()
            
            # Commit all changes
            conn.commit()
            print("✅ All leadership updates committed to database")
            
    except Exception as e:
        print(f"❌ Error during update: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
    
    # Save results
    update_log = {
        'update_time': datetime.now().isoformat(),
        'target': '119th Congress Republican Leadership',
        'committees_updated': len(results),
        'updates': results
    }
    
    with open('leadership_fix_results.json', 'w') as f:
        json.dump(update_log, f, indent=2)
    
    print(f"Update log saved to: leadership_fix_results.json")
    return True

def verify_updates():
    """Verify the leadership updates were successful"""
    print("\n" + "=" * 60)
    print("VERIFICATION: 119TH CONGRESS LEADERSHIP")
    print("=" * 60)
    
    import requests
    API_BASE = "https://congressional-data-api-v2-1066017671167.us-central1.run.app"
    
    for committee_id in LEADERSHIP_UPDATES.keys():
        response = requests.get(f"{API_BASE}/api/v1/committees/{committee_id}/members")
        if response.status_code == 200:
            members = response.json()
            committee_name = LEADERSHIP_UPDATES[committee_id]['committee_name']
            
            print(f"{committee_name}:")
            
            for member_info in members:
                position = member_info.get('position', 'member').lower()
                if position in ['chair', 'ranking_member']:
                    member = member_info['member']
                    name = f"{member['first_name']} {member['last_name']}"
                    party = member['party'][0]  # R or D
                    print(f"  {position.title()}: {name} ({party})")
            print()

if __name__ == "__main__":
    success = fix_committee_leadership()
    if success:
        print("\n🎉 119th Congress leadership fix completed successfully!")
        verify_updates()
    else:
        print("\n❌ Leadership fix failed")