#!/usr/bin/env python3
"""
Fix Adam Schiff's chamber assignment and committee memberships
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def fix_adam_schiff():
    """Fix Adam Schiff's chamber assignment and committee memberships"""
    
    conn = connect_to_database()
    if not conn:
        return False
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Find Adam Schiff
        cursor.execute("""
            SELECT * FROM members 
            WHERE last_name = 'Schiff' AND first_name LIKE 'Adam%'
        """)
        schiff = cursor.fetchone()
        
        if not schiff:
            logger.error("Adam Schiff not found in database")
            return False
        
        print(f"Found Adam Schiff: {schiff['bioguide_id']}")
        print(f"Current chamber: {schiff['chamber']}")
        print(f"Current state: {schiff['state']}")
        print(f"Current district: {schiff['district']}")
        
        # Update chamber to Senate
        cursor.execute("""
            UPDATE members 
            SET chamber = 'Senate',
                district = NULL,
                updated_at = NOW()
            WHERE bioguide_id = %s
        """, (schiff['bioguide_id'],))
        
        print(f"✅ Updated Adam Schiff to Senate")
        
        # Remove all existing committee memberships (House committees)
        cursor.execute("""
            DELETE FROM committee_memberships 
            WHERE member_id = %s
        """, (schiff['id'],))
        
        print(f"✅ Removed existing House committee memberships")
        
        # Find Senate committees for new assignments
        senate_committees = {
            'Judiciary': 'Senate Judiciary Committee',
            'Agriculture': 'Senate Agriculture, Nutrition, and Forestry Committee',
            'Environment': 'Senate Environment and Public Works Committee',
            'Small Business': 'Senate Small Business and Entrepreneurship Committee'
        }
        
        committee_assignments = []
        
        for short_name, full_name in senate_committees.items():
            cursor.execute("""
                SELECT id, name FROM committees 
                WHERE name ILIKE %s AND chamber = 'Senate'
                ORDER BY name
            """, (f"%{short_name}%",))
            
            matches = cursor.fetchall()
            
            if matches:
                committee = matches[0]  # Take first match
                committee_assignments.append({
                    'committee_id': committee['id'],
                    'committee_name': committee['name'],
                    'role': 'Member'
                })
                print(f"Found committee: {committee['name']}")
            else:
                print(f"⚠️ Could not find committee matching '{short_name}'")
        
        # Add new Senate committee memberships
        for assignment in committee_assignments:
            cursor.execute("""
                INSERT INTO committee_memberships 
                (member_id, committee_id, position, start_date, is_current)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                schiff['id'],
                assignment['committee_id'],
                assignment['role'],
                '2025-01-01',
                True
            ))
            
            print(f"✅ Added membership: {assignment['committee_name']}")
        
        # Add specific subcommittee roles if available
        # Try to find and assign ranking member roles
        ranking_subcommittees = [
            'Intellectual Property',
            'Fisheries, Water, and Wildlife'
        ]
        
        for subcommittee_name in ranking_subcommittees:
            cursor.execute("""
                SELECT id, name FROM committees 
                WHERE name ILIKE %s AND chamber = 'Senate'
                ORDER BY name
            """, (f"%{subcommittee_name}%",))
            
            matches = cursor.fetchall()
            
            if matches:
                subcommittee = matches[0]
                cursor.execute("""
                    INSERT INTO committee_memberships 
                    (member_id, committee_id, position, start_date, is_current)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    schiff['id'],
                    subcommittee['id'],
                    'Ranking Member',
                    '2025-01-01',
                    True
                ))
                
                print(f"✅ Added ranking member role: {subcommittee['name']}")
        
        # Commit changes
        conn.commit()
        
        print(f"\n🎉 Successfully fixed Adam Schiff's record:")
        print(f"   Chamber: House → Senate")
        print(f"   Committee Assignments: {len(committee_assignments)} main committees")
        print(f"   Special Roles: Ranking Member positions assigned")
        
        return True
        
    except Exception as e:
        logger.error(f"Error fixing Adam Schiff: {e}")
        conn.rollback()
        return False
    
    finally:
        cursor.close()
        conn.close()

def verify_fix():
    """Verify the fix was applied correctly"""
    
    conn = connect_to_database()
    if not conn:
        return False
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Check Adam Schiff's current record
        cursor.execute("""
            SELECT bioguide_id, first_name, last_name, chamber, state, district
            FROM members 
            WHERE last_name = 'Schiff' AND first_name LIKE 'Adam%'
        """)
        schiff = cursor.fetchone()
        
        if schiff:
            print(f"\n📋 VERIFICATION - Adam Schiff Record:")
            print(f"   Name: {schiff['first_name']} {schiff['last_name']}")
            print(f"   Chamber: {schiff['chamber']}")
            print(f"   State: {schiff['state']}")
            print(f"   District: {schiff['district']}")
            
            # Check committee memberships
            cursor.execute("""
                SELECT c.name, cm.position
                FROM committee_memberships cm
                JOIN committees c ON cm.committee_id = c.id
                JOIN members m ON cm.member_id = m.id
                WHERE m.bioguide_id = %s AND cm.is_current = TRUE
                ORDER BY c.name
            """, (schiff['bioguide_id'],))
            
            memberships = cursor.fetchall()
            print(f"   Committee Memberships: {len(memberships)}")
            
            for membership in memberships:
                print(f"     - {membership['name']} ({membership['position']})")
            
            # Check CA senators count
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM members
                WHERE state = 'CA' AND chamber = 'Senate'
            """)
            ca_senators = cursor.fetchone()
            
            print(f"\n📊 California Senators: {ca_senators['count']}/2")
            
            return schiff['chamber'] == 'Senate' and ca_senators['count'] == 2
        
        return False
        
    except Exception as e:
        logger.error(f"Error verifying fix: {e}")
        return False
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=== FIXING ADAM SCHIFF RECORD ===\n")
    
    if fix_adam_schiff():
        print("\n=== VERIFICATION ===")
        if verify_fix():
            print("\n✅ Fix applied successfully!")
        else:
            print("\n❌ Fix verification failed!")
    else:
        print("\n❌ Fix failed!")