#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import RealDictCursor

def check_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if table exists
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'members';
        """)
        tables = cursor.fetchall()
        print(f"Members table exists: {len(tables) > 0}")
        
        # Check table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'members' AND table_schema = 'public'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print("Table columns:")
        for col in columns:
            print(f"  {col['column_name']}: {col['data_type']}")
        
        # Check total count
        cursor.execute("SELECT COUNT(*) FROM members;")
        total = cursor.fetchone()
        print(f"\nTotal members: {total['count']}")
        
        # Check chamber values
        cursor.execute("SELECT DISTINCT chamber FROM members;")
        chambers = cursor.fetchall()
        print(f"Distinct chamber values: {[c['chamber'] for c in chambers]}")
        
        # Check first 3 records
        cursor.execute("SELECT bioguide_id, first_name, last_name, chamber, state, district FROM members LIMIT 3;")
        sample = cursor.fetchall()
        print("\nSample records:")
        for record in sample:
            print(f"  {record['first_name']} {record['last_name']} ({record['bioguide_id']}) - {record['chamber']} {record['state']} {record['district']}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    check_database()