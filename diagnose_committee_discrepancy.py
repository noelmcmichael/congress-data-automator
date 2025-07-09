#!/usr/bin/env python3
"""
Diagnose Committee Count Discrepancy
===================================

Investigate why API returns 50 committees while deployment reported 199.
"""

import subprocess
import json
import requests
from datetime import datetime

def execute_sql_via_gcloud(sql_query):
    """Execute SQL query via gcloud"""
    try:
        import os
        env = os.environ.copy()
        env["PGPASSWORD"] = "mDf3S9ZnBpQqJvGsY1"
        result = subprocess.run([
            "/opt/homebrew/bin/gcloud", "sql", "connect", "congressional-db", 
            "--user=postgres", "--quiet"
        ], 
        input=f"{sql_query}\n\\q", 
        text=True, 
        capture_output=True,
        env=env
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }

def main():
    print("🔍 Diagnosing Committee Count Discrepancy")
    print("=" * 50)
    
    # 1. Check total committee count in database
    print("\n1. Checking total committee count in database...")
    result = execute_sql_via_gcloud("SELECT COUNT(*) FROM committees;")
    if result["returncode"] == 0:
        # Extract count from output
        lines = result["stdout"].strip().split('\n')
        for line in lines:
            if line.strip().isdigit():
                db_count = int(line.strip())
                print(f"   Database committee count: {db_count}")
                break
    else:
        print(f"   ❌ Error querying database: {result['stderr']}")
        return
    
    # 2. Check API committee count
    print("\n2. Checking API committee count...")
    try:
        response = requests.get("https://politicalequity.io/api/v1/committees", timeout=10)
        if response.status_code == 200:
            api_data = response.json()
            api_count = len(api_data) if isinstance(api_data, list) else 0
            print(f"   API committee count: {api_count}")
        else:
            print(f"   ❌ API error: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ API request failed: {e}")
        return
    
    # 3. Check if there are pagination or filtering issues
    print("\n3. Checking for active committees only...")
    result = execute_sql_via_gcloud("SELECT COUNT(*) FROM committees WHERE is_active = true;")
    if result["returncode"] == 0:
        lines = result["stdout"].strip().split('\n')
        for line in lines:
            if line.strip().isdigit():
                active_count = int(line.strip())
                print(f"   Active committees in database: {active_count}")
                break
    
    # 4. Check committee distribution by chamber
    print("\n4. Checking committee distribution by chamber...")
    result = execute_sql_via_gcloud("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber ORDER BY chamber;")
    if result["returncode"] == 0:
        print("   Database distribution:")
        lines = result["stdout"].strip().split('\n')
        for line in lines:
            if '|' in line and not line.startswith('-'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2 and not parts[0].lower() in ['chamber', 'chamber']:
                    print(f"     {parts[0]}: {parts[1]}")
    
    # 5. Check if API has any filtering or limits
    print("\n5. Testing API pagination...")
    try:
        response = requests.get("https://politicalequity.io/api/v1/committees?limit=1000", timeout=10)
        if response.status_code == 200:
            api_data_unlimited = response.json()
            unlimited_count = len(api_data_unlimited) if isinstance(api_data_unlimited, list) else 0
            print(f"   API with high limit: {unlimited_count}")
        else:
            print(f"   API with limit parameter: {response.status_code}")
    except Exception as e:
        print(f"   Pagination test failed: {e}")
    
    # 6. Check recent committees added
    print("\n6. Checking recently added committees...")
    result = execute_sql_via_gcloud("""
        SELECT name, chamber, created_at 
        FROM committees 
        ORDER BY created_at DESC 
        LIMIT 5;
    """)
    if result["returncode"] == 0:
        print("   Recent committees:")
        lines = result["stdout"].strip().split('\n')
        for line in lines:
            if '|' in line and not line.startswith('-'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3 and not parts[0].lower() in ['name', '']:
                    print(f"     {parts[0][:50]}... ({parts[1]}) - {parts[2][:10]}")
    
    print(f"\n🎯 Summary:")
    print(f"   Database Count: {db_count if 'db_count' in locals() else 'Unknown'}")
    print(f"   API Count: {api_count if 'api_count' in locals() else 'Unknown'}")
    print(f"   Discrepancy: {db_count - api_count if 'db_count' in locals() and 'api_count' in locals() else 'Unknown'}")

if __name__ == "__main__":
    main()