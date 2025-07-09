#!/usr/bin/env python3
"""
Check Committee Types
====================

Check what committee_type values exist in current data.
"""

import subprocess
import time
import psycopg2

def check_committee_types():
    """Check existing committee types"""
    
    print("🔍 Checking existing committee types")
    
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
        
        # Check distinct committee types
        cursor.execute("""
            SELECT committee_type, COUNT(*) 
            FROM committees 
            GROUP BY committee_type 
            ORDER BY COUNT(*) DESC;
        """)
        
        types = cursor.fetchall()
        
        print("📋 Current committee_type values:")
        for committee_type, count in types:
            print(f"  '{committee_type}': {count} committees")
        
        # Check some example committees
        cursor.execute("""
            SELECT name, chamber, committee_type, is_subcommittee
            FROM committees 
            WHERE committee_type IS NOT NULL
            LIMIT 10;
        """)
        
        examples = cursor.fetchall()
        
        print("\n📋 Example committees:")
        for name, chamber, committee_type, is_sub in examples:
            sub_indicator = " (SUB)" if is_sub else ""
            print(f"  {name[:40]}... ({chamber}) - {committee_type}{sub_indicator}")
        
        cursor.close()
        conn.close()
        proxy.terminate()
        
        return types
        
    except Exception as e:
        print(f"❌ Failed to check committee types: {e}")
        if 'proxy' in locals():
            proxy.terminate()
        return None

def main():
    types = check_committee_types()
    
    if types:
        print(f"\n🎯 Found {len(types)} different committee types")
        print("   Most common types can be used as defaults for new committees")

if __name__ == "__main__":
    main()