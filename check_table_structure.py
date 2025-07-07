#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import RealDictCursor

def check_table_structure():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="congress_data",
            user="postgres",
            password="mDf3S9ZnBpQqJvGsY1"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check committee_memberships table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'committee_memberships' AND table_schema = 'public'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print("committee_memberships table columns:")
        for col in columns:
            print(f"  {col['column_name']}: {col['data_type']}")
        
        # Check sample data
        cursor.execute("SELECT * FROM committee_memberships LIMIT 3;")
        sample = cursor.fetchall()
        print("\nSample records:")
        for record in sample:
            print(f"  {dict(record)}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_table_structure()