#!/usr/bin/env python3
"""
Fix duplicate senators by removing extras
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def fix_duplicate_senators():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("🔍 IDENTIFYING DUPLICATE SENATORS\n")
        
        # Check states with more than 2 senators
        cursor.execute("""
            SELECT state, COUNT(*) as senator_count
            FROM members
            WHERE chamber = 'Senate'
            GROUP BY state
            HAVING COUNT(*) > 2
            ORDER BY state
        """)
        
        excess_states = cursor.fetchall()
        
        for state_info in excess_states:
            state = state_info['state']
            count = state_info['senator_count']
            
            print(f"📊 {state}: {count} senators (excess: {count - 2})")
            
            # Get senators for this state
            cursor.execute("""
                SELECT id, bioguide_id, first_name, last_name, party, 
                       term_start, term_end, created_at
                FROM members
                WHERE state = %s AND chamber = 'Senate'
                ORDER BY term_start DESC, created_at DESC
            """, (state,))
            
            senators = cursor.fetchall()
            
            for i, senator in enumerate(senators):
                status = "KEEP" if i < 2 else "REMOVE"
                print(f"   {i+1}. {senator['first_name']} {senator['last_name']} ({senator['party']}) - {status}")
                print(f"      Term: {senator['term_start']} to {senator['term_end']}")
                print(f"      Created: {senator['created_at']}")
                
                # Remove excess senators (keep the first 2)
                if i >= 2:
                    print(f"      🗑️  Removing {senator['first_name']} {senator['last_name']}")
                    
                    # Remove committee memberships first
                    cursor.execute("""
                        DELETE FROM committee_memberships 
                        WHERE member_id = %s
                    """, (senator['id'],))
                    
                    # Remove the member
                    cursor.execute("""
                        DELETE FROM members 
                        WHERE id = %s
                    """, (senator['id'],))
                    
                    print(f"      ✅ Removed")
            
            print()
        
        # Commit changes
        conn.commit()
        
        # Verify the fix
        cursor.execute("""
            SELECT COUNT(*) as total_senators
            FROM members
            WHERE chamber = 'Senate'
        """)
        total = cursor.fetchone()
        
        cursor.execute("""
            SELECT state, COUNT(*) as senator_count
            FROM members
            WHERE chamber = 'Senate'
            GROUP BY state
            HAVING COUNT(*) != 2
            ORDER BY state
        """)
        problem_states = cursor.fetchall()
        
        print(f"🎉 CLEANUP COMPLETE")
        print(f"   Total Senators: {total['total_senators']}")
        print(f"   Problem States: {len(problem_states)}")
        
        if problem_states:
            print("\n⚠️  REMAINING ISSUES:")
            for state in problem_states:
                print(f"   {state['state']}: {state['senator_count']} senators")
        else:
            print("\n✅ All states now have exactly 2 senators")
        
        cursor.close()
        conn.close()
        
        return total['total_senators'] == 100
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== FIXING DUPLICATE SENATORS ===\n")
    
    if fix_duplicate_senators():
        print("\n✅ Fix completed successfully!")
    else:
        print("\n❌ Fix failed or incomplete!")