#!/usr/bin/env python3
"""
Check Database Constraints
==========================

Check what constraints exist on the committees table.
"""

import subprocess
import time
import psycopg2

def check_constraints():
    """Check database constraints"""
    
    print("🔍 Checking database constraints")
    
    try:
        # Start proxy
        proxy = subprocess.Popen([
            "./cloud-sql-proxy", "chefgavin:us-central1:congressional-db", "--port=5433"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        
        # Connect
        conn = psycopg2.connect(
            host="localhost", port=5433, database="congress_data",
            user="postgres", password="mDf3S9ZnBpQqJvGsY1"
        )
        
        cursor = conn.cursor()
        
        # Check unique constraints
        cursor.execute("""
            SELECT conname, contype, pg_get_constraintdef(oid) as definition
            FROM pg_constraint 
            WHERE conrelid = 'committees'::regclass;
        """)
        
        constraints = cursor.fetchall()
        
        print("📋 Constraints on committees table:")
        for name, type_code, definition in constraints:
            constraint_type = {
                'p': 'PRIMARY KEY',
                'u': 'UNIQUE',
                'f': 'FOREIGN KEY',
                'c': 'CHECK'
            }.get(type_code, type_code)
            print(f"  {name}: {constraint_type}")
            print(f"    {definition}")
        
        # Check indexes
        cursor.execute("""
            SELECT indexname, indexdef 
            FROM pg_indexes 
            WHERE tablename = 'committees';
        """)
        
        indexes = cursor.fetchall()
        
        print("\n📋 Indexes on committees table:")
        for name, definition in indexes:
            print(f"  {name}: {definition}")
        
        cursor.close()
        conn.close()
        proxy.terminate()
        
        return constraints, indexes
        
    except Exception as e:
        print(f"❌ Failed to check constraints: {e}")
        if 'proxy' in locals():
            proxy.terminate()
        return None, None

def main():
    check_constraints()

if __name__ == "__main__":
    main()