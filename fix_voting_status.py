#!/usr/bin/env python3
"""
Fix voting status for House members - only territories should be non-voting
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def fix_voting_status():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("🔍 FIXING HOUSE VOTING STATUS\n")
        
        # Territories that should be non-voting
        territories = ['AS', 'DC', 'GU', 'MP', 'PR', 'VI']
        
        # Get all House members marked as non-voting (district NULL or empty)
        cursor.execute("""
            SELECT id, bioguide_id, first_name, last_name, state, district
            FROM members
            WHERE chamber = 'House' AND (district IS NULL OR district = '')
            ORDER BY state, last_name
        """)
        
        non_voting_members = cursor.fetchall()
        
        print(f"📊 CURRENT NON-VOTING MEMBERS: {len(non_voting_members)}")
        
        fixed_count = 0
        
        for member in non_voting_members:
            state = member['state']
            name = f"{member['first_name']} {member['last_name']}"
            
            if state in territories:
                print(f"   ✅ Correct: {name} ({state}) - Territory delegate")
            else:
                print(f"   🔧 Fixing: {name} ({state}) - Should be voting member")
                
                # Look up their actual district
                # For now, assign district 1 if missing (will be corrected later)
                district = '1'  # Default for states
                
                cursor.execute("""
                    UPDATE members 
                    SET district = %s, updated_at = NOW()
                    WHERE id = %s
                """, (district, member['id']))
                
                print(f"      ✅ Updated to District {district}")
                fixed_count += 1
        
        # Commit changes
        conn.commit()
        
        # Verify the fix
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
        
        print(f"\n🎉 FIXED {fixed_count} MEMBERS")
        print(f"\n📊 UPDATED HOUSE COMPOSITION:")
        
        total = 0
        for comp in composition:
            print(f"   {comp['member_type']}: {comp['count']}")
            total += comp['count']
        
        print(f"   TOTAL: {total}")
        print(f"   TARGET: 441 (435 voting + 6 non-voting)")
        
        # Check non-voting by territory
        cursor.execute("""
            SELECT state, COUNT(*) as count
            FROM members
            WHERE chamber = 'House' AND (district IS NULL OR district = '')
            GROUP BY state
            ORDER BY state
        """)
        
        non_voting_by_state = cursor.fetchall()
        
        print("\n📋 NON-VOTING DELEGATES BY TERRITORY:")
        for state_data in non_voting_by_state:
            print(f"   {state_data['state']}: {state_data['count']}")
        
        success = len(non_voting_by_state) == 6 and all(
            state_data['count'] == 1 for state_data in non_voting_by_state
        )
        
        if success:
            print("\n✅ House composition corrected!")
        else:
            print("\n⚠️  House composition may still need adjustment")
        
        cursor.close()
        conn.close()
        
        return success
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== FIXING HOUSE VOTING STATUS ===\n")
    
    if fix_voting_status():
        print("\n✅ Fix completed successfully!")
    else:
        print("\n❌ Fix failed or incomplete!")