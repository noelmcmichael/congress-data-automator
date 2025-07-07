#!/usr/bin/env python3
"""
Database Inspector

Simple script to inspect the database structure and available data.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json

def inspect_database():
    """Inspect the database structure"""
    print("🔍 Inspecting database structure...")
    
    try:
        # Connect to postgres database first
        conn = psycopg2.connect(
            host='localhost',
            port=5433,
            database='congress_data',
            user='postgres',
            password='mDf3S9ZnBpQqJvGsY1'
        )
        
        with conn.cursor() as cursor:
            # List all databases
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = cursor.fetchall()
            print(f"Available databases: {[db[0] for db in databases]}")
        
        conn.close()
        
        # Try to connect to congressional databases
        for db_name in ['congress_data', 'postgres', 'congressional_data']:
            try:
                print(f"\n🔍 Trying to connect to database: {db_name}")
                conn = psycopg2.connect(
                    host='localhost',
                    port=5433,
                    database=db_name,
                    user='postgres',
                    password='mDf3S9ZnBpQqJvGsY1'
                )
                
                with conn.cursor() as cursor:
                    # List all tables
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        ORDER BY table_name;
                    """)
                    tables = cursor.fetchall()
                    print(f"📋 Tables in {db_name}: {[table[0] for table in tables]}")
                    
                    # If we have a members table, check it
                    if any('members' in table[0] for table in tables):
                        print(f"\n📊 Checking members table in {db_name}...")
                        
                        # Count total members
                        cursor.execute("SELECT COUNT(*) FROM members;")
                        member_count = cursor.fetchone()[0]
                        print(f"Total members: {member_count}")
                        
                        # Count members with NULL names
                        cursor.execute("SELECT COUNT(*) FROM members WHERE name IS NULL OR name = 'Unknown';")
                        null_count = cursor.fetchone()[0]
                        print(f"Members with NULL/Unknown names: {null_count}")
                        
                        # Check for Chuck Grassley
                        cursor.execute("SELECT id, first_name, last_name, name, bioguide_id FROM members WHERE bioguide_id = 'G000386';")
                        grassley = cursor.fetchone()
                        if grassley:
                            print(f"Chuck Grassley: ID={grassley[0]}, name='{grassley[3]}', bioguide={grassley[4]}")
                        else:
                            print("Chuck Grassley not found")
                        
                        # Sample of senators with name issues
                        cursor.execute("""
                            SELECT id, first_name, last_name, name, bioguide_id 
                            FROM members 
                            WHERE chamber = 'Senate' AND (name IS NULL OR name = 'Unknown')
                            LIMIT 5;
                        """)
                        sample_senators = cursor.fetchall()
                        print(f"Sample senators with name issues:")
                        for senator in sample_senators:
                            print(f"  ID={senator[0]}, '{senator[1]} {senator[2]}', name='{senator[3]}', bioguide={senator[4]}")
                        
                        # Check committees
                        if any('committees' in table[0] for table in tables):
                            cursor.execute("SELECT COUNT(*) FROM committees;")
                            committee_count = cursor.fetchone()[0]
                            print(f"Total committees: {committee_count}")
                            
                            # Check for Judiciary Committee
                            cursor.execute("SELECT id, name, chamber FROM committees WHERE name LIKE '%Judiciary%';")
                            judiciary = cursor.fetchall()
                            print(f"Judiciary committees: {judiciary}")
                
                conn.close()
                print(f"✅ Successfully connected to {db_name}")
                return db_name
                
            except Exception as e:
                print(f"❌ Could not connect to {db_name}: {str(e)}")
                continue
        
        print("❌ Could not connect to any database")
        return None
        
    except Exception as e:
        print(f"❌ Database inspection failed: {str(e)}")
        return None

if __name__ == "__main__":
    result = inspect_database()
    if result:
        print(f"\n🎉 Found working database: {result}")
    else:
        print("\n❌ No working database found")