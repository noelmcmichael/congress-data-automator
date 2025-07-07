#!/usr/bin/env python3
"""
Check Database Schema

Simple script to check the actual database schema.
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def check_schema():
    """Check the database schema"""
    print("🔍 Checking database schema...")
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5433,
            database='congress_data',
            user='postgres',
            password='mDf3S9ZnBpQqJvGsY1'
        )
        
        with conn.cursor() as cursor:
            # Check members table schema
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'members'
                ORDER BY ordinal_position;
            """)
            members_columns = cursor.fetchall()
            print(f"📋 Members table columns:")
            for col in members_columns:
                print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
            
            # Check sample member data
            cursor.execute("SELECT * FROM members LIMIT 3;")
            sample_members = cursor.fetchall()
            print(f"\n📊 Sample member data:")
            for member in sample_members:
                print(f"  {member}")
            
            # Check for Chuck Grassley
            cursor.execute("SELECT * FROM members WHERE bioguide_id = 'G000386';")
            grassley = cursor.fetchone()
            if grassley:
                print(f"\n🔍 Chuck Grassley data: {grassley}")
            else:
                print("\n❌ Chuck Grassley not found")
            
            # Check committees table schema
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'committees'
                ORDER BY ordinal_position;
            """)
            committees_columns = cursor.fetchall()
            print(f"\n📋 Committees table columns:")
            for col in committees_columns:
                print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
            
            # Check for Senate Judiciary Committee
            cursor.execute("SELECT * FROM committees WHERE name LIKE '%Judiciary%' AND chamber = 'Senate';")
            judiciary = cursor.fetchone()
            if judiciary:
                print(f"\n🔍 Senate Judiciary Committee: {judiciary}")
            else:
                print("\n❌ Senate Judiciary Committee not found")
            
            # Check committee memberships
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'committee_memberships'
                ORDER BY ordinal_position;
            """)
            memberships_columns = cursor.fetchall()
            print(f"\n📋 Committee memberships table columns:")
            for col in memberships_columns:
                print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Schema check failed: {str(e)}")
        return False

if __name__ == "__main__":
    check_schema()