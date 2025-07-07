#!/usr/bin/env python3
"""
Fix schema field name mismatch between database and API response
"""

import os
import subprocess
import sys

def fix_committee_schema():
    """Fix the field name mismatch in committee schema"""
    print("=== FIXING COMMITTEE SCHEMA FIELD NAMES ===")
    
    schema_file = "backend/app/schemas/committee.py"
    
    # Read current schema
    with open(schema_file, 'r') as f:
        content = f.read()
    
    print("Current schema content:")
    print(content)
    
    # The database model has:
    # website = Column(String(500))
    # official_website_url = Column(String(255))
    
    # But the API is returning website_url
    # This suggests the current production schema might have website_url instead of website
    
    # Let's check what's actually in the database by looking at the working API
    print("\n=== ANALYSIS ===")
    print("Database model has:")
    print("  - website (Column)")
    print("  - official_website_url (Column)")
    print("Current API returns:")
    print("  - website_url (from production)")
    print("Schema expects:")
    print("  - website")
    print("  - official_website_url")
    
    # Option 1: Change schema to match current production (website_url)
    # Option 2: Change database to match schema (website)
    # Option 3: Find out why there's a mismatch
    
    print("\nPossible fixes:")
    print("1. Update schema to use website_url to match current production")
    print("2. Check if there's a field alias or mapping issue")
    print("3. Verify database column names in production")
    
    return True

def check_current_production_schema():
    """Check what schema is actually deployed in production"""
    print("\n=== CHECKING PRODUCTION SCHEMA ===")
    
    # The working API returns website_url, so the production schema probably has:
    # website_url instead of website
    
    # Let's check git history to see if there were changes
    try:
        cmd = ["git", "log", "--oneline", "-10", "--", "backend/app/schemas/committee.py"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/noelmcmichael/Workspace/congress_data_automator")
        print("Recent schema changes:")
        print(result.stdout)
    except Exception as e:
        print(f"Error checking git history: {e}")
    
    return True

def propose_solution():
    """Propose the best solution for field name mismatch"""
    print("\n=== PROPOSED SOLUTION ===")
    
    print("Based on analysis:")
    print("1. Current production API returns 'website_url: null'")
    print("2. Database model has 'website' and 'official_website_url' columns")
    print("3. Schema expects 'website' and 'official_website_url'")
    print("")
    print("The mismatch suggests that:")
    print("- Current production uses an older schema with 'website_url'")
    print("- Enhanced schema with URL fields is not deployed")
    print("")
    print("SOLUTION:")
    print("1. Keep schema as-is (it's correct for the database model)")
    print("2. Deploy enhanced schema to replace current production schema")
    print("3. The URL fields should appear once enhanced schema is deployed")
    print("")
    print("NEXT STEPS:")
    print("1. Build container with current enhanced schema")
    print("2. Deploy to Cloud Run with proper environment variables")
    print("3. Test that URL fields appear in API response")
    
    return True

if __name__ == "__main__":
    print("Analyzing schema field name mismatch...")
    
    fix_committee_schema()
    check_current_production_schema()
    propose_solution()
    
    print("\n=== CONCLUSION ===")
    print("Schema appears correct. Need to deploy enhanced version to production.")