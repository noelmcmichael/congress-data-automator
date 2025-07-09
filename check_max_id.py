#!/usr/bin/env python3
"""
Check Max Committee ID
======================

Check the current maximum committee ID.
"""

import subprocess
import time
import psycopg2

def check_max_id():
    """Check current max committee ID"""
    
    print("🔍 Checking current max committee ID")
    
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
        
        # Check max ID
        cursor.execute("SELECT MAX(id) FROM committees;")
        max_id = cursor.fetchone()[0]
        print(f"✅ Current max committee ID: {max_id}")
        
        # Check sequence value
        cursor.execute("SELECT nextval('committees_id_seq');")
        next_id = cursor.fetchone()[0]
        print(f"✅ Next auto-increment ID would be: {next_id}")
        
        # Reset sequence to correct value
        cursor.execute("SELECT setval('committees_id_seq', %s);", (max_id,))
        reset_result = cursor.fetchone()[0]
        print(f"✅ Reset sequence to: {reset_result}")
        
        cursor.close()
        conn.close()
        proxy.terminate()
        
        return max_id
        
    except Exception as e:
        print(f"❌ Failed to check max ID: {e}")
        if 'proxy' in locals():
            proxy.terminate()
        return None

def main():
    max_id = check_max_id()
    
    if max_id:
        print(f"\n🎯 Current max ID: {max_id}")
        print("   The sequence has been reset to continue from this point")

if __name__ == "__main__":
    main()