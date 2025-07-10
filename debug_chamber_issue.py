#!/usr/bin/env python3
"""
Debug script to investigate the House chamber filtering issue.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_chamber_filtering():
    """Debug the chamber filtering issue."""
    
    # Try to get the production database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return
    
    print(f"🔍 Connecting to database: {database_url}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("\n📊 Committee Chamber Analysis:")
            
            # Check all chamber values
            result = conn.execute(text("SELECT DISTINCT chamber FROM committees ORDER BY chamber")).fetchall()
            print(f"📋 Distinct chamber values: {[row[0] for row in result]}")
            
            # Count by chamber
            for chamber_name in ["House", "Senate", "Joint", "house", "senate", "joint"]:
                count_result = conn.execute(text("SELECT COUNT(*) FROM committees WHERE chamber = :chamber"), {"chamber": chamber_name}).scalar()
                print(f"📊 {chamber_name}: {count_result} committees")
            
            # Get sample House committees
            print("\n🏛️ Sample House Committees:")
            house_result = conn.execute(text("SELECT name, chamber, is_active FROM committees WHERE chamber = 'House' LIMIT 5")).fetchall()
            for row in house_result:
                print(f"  - {row[0]} ({row[1]}, active: {row[2]})")
            
            # Check if there are any committees with different case variations
            print("\n🔤 Case Sensitivity Check:")
            case_variations = ["House", "house", "HOUSE", "Senate", "senate", "SENATE", "Joint", "joint", "JOINT"]
            for variation in case_variations:
                count = conn.execute(text("SELECT COUNT(*) FROM committees WHERE chamber = :chamber"), {"chamber": variation}).scalar()
                if count > 0:
                    print(f"  - '{variation}': {count} committees")
            
            # Check for any unusual chamber values
            print("\n🔍 All Chamber Values with Counts:")
            all_chambers = conn.execute(text("SELECT chamber, COUNT(*) FROM committees GROUP BY chamber ORDER BY chamber")).fetchall()
            for row in all_chambers:
                print(f"  - '{row[0]}': {row[1]} committees")
                
            # Check for any NULL or empty chamber values
            null_count = conn.execute(text("SELECT COUNT(*) FROM committees WHERE chamber IS NULL")).scalar()
            empty_count = conn.execute(text("SELECT COUNT(*) FROM committees WHERE chamber = ''")).scalar()
            print(f"\n⚠️  NULL chambers: {null_count}")
            print(f"⚠️  Empty chambers: {empty_count}")
            
            # Check active vs inactive
            print("\n📊 Active vs Inactive Committees:")
            active_house = conn.execute(text("SELECT COUNT(*) FROM committees WHERE chamber = 'House' AND is_active = true")).scalar()
            inactive_house = conn.execute(text("SELECT COUNT(*) FROM committees WHERE chamber = 'House' AND is_active = false")).scalar()
            print(f"🏛️  Active House: {active_house}")
            print(f"🏛️  Inactive House: {inactive_house}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"📋 Database URL: {database_url}")

if __name__ == "__main__":
    debug_chamber_filtering()