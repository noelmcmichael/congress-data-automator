#!/usr/bin/env python3
"""
Analyze current congressional data foundation to identify issues
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_database():
    """Connect to the production database via Cloud SQL proxy"""
    # Connect via Cloud SQL proxy on port 5433
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string, echo=False)
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None

def analyze_current_data():
    """Analyze current member counts and identify issues"""
    
    engine = connect_to_database()
    if not engine:
        print("❌ Failed to connect to database")
        return []
    
    conn = engine.raw_connection()
    cursor = conn.cursor()
    
    print("=== CONGRESSIONAL DATA FOUNDATION ANALYSIS ===\n")
    
    # Overall counts
    cursor.execute("""
        SELECT chamber, COUNT(*) as count
        FROM members
        GROUP BY chamber
        ORDER BY chamber
    """)
    chamber_counts = cursor.fetchall()
    
    print("📊 CURRENT MEMBER COUNTS BY CHAMBER:")
    total_members = 0
    for chamber, count in chamber_counts:
        print(f"  {chamber.upper()}: {count}")
        total_members += count
    print(f"  TOTAL: {total_members}")
    
    # Target counts
    print("\n🎯 TARGET COUNTS:")
    print("  SENATE: 100 (2 per state)")
    print("  HOUSE: 441 (435 voting + 5 delegates + 1 commissioner)")
    print("  TOTAL: 541")
    
    # Check Adam Schiff
    cursor.execute("""
        SELECT bioguide_id, first_name, last_name, chamber, state, district
        FROM members
        WHERE last_name = 'Schiff' AND first_name LIKE 'Adam%'
    """)
    schiff_records = cursor.fetchall()
    
    print("\n🔍 ADAM SCHIFF CURRENT RECORD:")
    if schiff_records:
        for record in schiff_records:
            bioguide_id, first_name, last_name, chamber, state, district = record
            print(f"  {first_name} {last_name} ({bioguide_id})")
            print(f"    Chamber: {chamber}")
            print(f"    State: {state}")
            print(f"    District: {district}")
    else:
        print("  ❌ Adam Schiff not found in database")
    
    # Check California senators
    cursor.execute("""
        SELECT bioguide_id, first_name, last_name, chamber, state
        FROM members
        WHERE state = 'CA' AND chamber = 'Senate'
        ORDER BY last_name
    """)
    ca_senators = cursor.fetchall()
    
    print("\n🏛️ CALIFORNIA SENATORS:")
    print(f"  Count: {len(ca_senators)}/2 (should be 2)")
    for record in ca_senators:
        bioguide_id, first_name, last_name, chamber, state = record
        print(f"    {first_name} {last_name} ({bioguide_id})")
    
    # Check states with missing senators
    cursor.execute("""
        SELECT state, COUNT(*) as senator_count
        FROM members
        WHERE chamber = 'Senate'
        GROUP BY state
        HAVING COUNT(*) < 2
        ORDER BY state
    """)
    missing_senators = cursor.fetchall()
    
    print("\n🚨 STATES WITH MISSING SENATORS:")
    if missing_senators:
        for state, count in missing_senators:
            print(f"  {state}: {count}/2 senators")
    else:
        print("  ✅ All states have 2 senators")
    
    # Check house composition
    cursor.execute("""
        SELECT 
            CASE 
                WHEN district IS NULL OR district = '' THEN 'Non-voting'
                ELSE 'Voting'
            END as member_type,
            COUNT(*) as count
        FROM members
        WHERE chamber = 'House'
        GROUP BY 
            CASE 
                WHEN district IS NULL OR district = '' THEN 'Non-voting'
                ELSE 'Voting'
            END
        ORDER BY member_type
    """)
    house_composition = cursor.fetchall()
    
    print("\n🏛️ HOUSE COMPOSITION:")
    house_total = 0
    for member_type, count in house_composition:
        print(f"  {member_type}: {count}")
        house_total += count
    print(f"  TOTAL: {house_total}")
    print("  TARGET: 441 (435 voting + 6 non-voting)")
    
    # Check for potential duplicates
    cursor.execute("""
        SELECT first_name, last_name, COUNT(*) as count
        FROM members
        GROUP BY first_name, last_name
        HAVING COUNT(*) > 1
        ORDER BY count DESC, last_name
    """)
    duplicates = cursor.fetchall()
    
    print("\n⚠️  POTENTIAL DUPLICATE NAMES:")
    if duplicates:
        for first_name, last_name, count in duplicates:
            print(f"  {first_name} {last_name}: {count} records")
            
            # Get details for each duplicate
            cursor.execute("""
                SELECT bioguide_id, chamber, state, district
                FROM members
                WHERE first_name = %s AND last_name = %s
                ORDER BY chamber, state, district
            """, (first_name, last_name))
            details = cursor.fetchall()
            
            for bioguide_id, chamber, state, district in details:
                print(f"    - {bioguide_id}: {chamber.upper()} {state} {district or 'N/A'}")
    else:
        print("  ✅ No duplicate names found")
    
    # Summary
    print("\n📋 SUMMARY OF ISSUES:")
    issues = []
    
    # Senate count
    senate_count = next((count for chamber, count in chamber_counts if chamber == 'Senate'), 0)
    if senate_count != 100:
        issues.append(f"Senate has {senate_count}/100 members (missing {100 - senate_count})")
    
    # House count  
    house_count = next((count for chamber, count in chamber_counts if chamber == 'House'), 0)
    if house_count != 441:
        issues.append(f"House has {house_count}/441 members (excess {house_count - 441})")
    
    # Schiff chamber
    if schiff_records:
        schiff_chamber = schiff_records[0][2]  # chamber is 3rd element
        if schiff_chamber != 'Senate':
            issues.append("Adam Schiff listed as House member, should be Senator")
    
    # CA senators
    if len(ca_senators) != 2:
        issues.append(f"California has {len(ca_senators)}/2 senators")
    
    if issues:
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("  ✅ No issues found")
    
    cursor.close()
    conn.close()
    return issues

if __name__ == "__main__":
    analyze_current_data()