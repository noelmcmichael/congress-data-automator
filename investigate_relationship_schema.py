#!/usr/bin/env python3
"""
Investigate database schema and relationship structure
to understand why committee memberships and hearing relationships are missing
"""

import os
import json
from datetime import datetime
import keyring

def get_database_connection():
    """Get database connection details from environment or keyring"""
    try:
        # Load from .env file first
        from dotenv import load_dotenv
        load_dotenv()
        
        # Try environment variable first (from .env)
        db_url = os.getenv("DATABASE_URL")
        
        if not db_url:
            # Try to get from keyring as fallback
            db_url = keyring.get_password("memex", "DATABASE_URL")
        
        if not db_url:
            print("❌ No database URL found in keyring or environment")
            print("💡 Try setting DATABASE_URL in .env file or keyring")
            return None
            
        print(f"✅ Found database URL: {db_url[:30]}...")
        return db_url
    except Exception as e:
        print(f"❌ Error getting database credentials: {e}")
        return None

def investigate_schema_structure():
    """Investigate database schema for relationship tables"""
    print("🔍 Investigating Database Schema Structure...")
    
    try:
        import sqlalchemy
        from sqlalchemy import create_engine, text
        
        db_url = get_database_connection()
        if not db_url:
            return False
            
        # Create engine
        engine = create_engine(db_url)
        
        print("✅ Database connection established")
        
        # Check what tables exist
        with engine.connect() as conn:
            # Get all table names
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"\n📋 Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
            
            # Check for relationship-related tables
            relationship_tables = [t for t in tables if any(keyword in t.lower() for keyword in ['member', 'committee', 'hearing', 'relationship'])]
            print(f"\n🔗 Potential relationship tables ({len(relationship_tables)}):")
            for table in relationship_tables:
                print(f"  - {table}")
            
            # Examine key tables in detail
            key_tables = ['members', 'committees', 'hearings']
            
            for table_name in key_tables:
                if table_name in tables:
                    print(f"\n📊 Table: {table_name}")
                    
                    # Get column information
                    columns_result = conn.execute(text(f"""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}'
                        ORDER BY ordinal_position;
                    """))
                    
                    columns = columns_result.fetchall()
                    print(f"  Columns ({len(columns)}):")
                    for col in columns:
                        print(f"    - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
                    
                    # Get row count
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = count_result.fetchone()[0]
                    print(f"  Row count: {count}")
                    
                    # Check for relationship columns
                    relationship_cols = [col[0] for col in columns if any(keyword in col[0].lower() for keyword in ['committee', 'member', 'hearing'])]
                    if relationship_cols:
                        print(f"  Relationship columns: {relationship_cols}")
                        
                        # Sample data for relationship columns
                        for col in relationship_cols:
                            sample_result = conn.execute(text(f"SELECT {col}, COUNT(*) as count FROM {table_name} WHERE {col} IS NOT NULL GROUP BY {col} LIMIT 5"))
                            sample_data = sample_result.fetchall()
                            if sample_data:
                                print(f"    {col} sample values: {[row[0] for row in sample_data]}")
                            else:
                                print(f"    {col}: No non-null values found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error investigating schema: {e}")
        return False

def check_api_response_structure():
    """Check what the API actually returns for members and committees"""
    print("\n🔍 Investigating API Response Structure...")
    
    import requests
    
    base_url = "https://congressional-data-api-v3-1066017671167.us-central1.run.app/api/v1"
    
    # Check member response structure
    try:
        response = requests.get(f"{base_url}/members?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data:
                member = data[0] if isinstance(data, list) else data.get('members', [{}])[0]
                print(f"\n👤 Member object structure:")
                for key, value in member.items():
                    value_type = type(value).__name__
                    value_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"  - {key}: {value_type} = {value_preview}")
        else:
            print(f"❌ Members API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking members API: {e}")
    
    # Check committee response structure  
    try:
        response = requests.get(f"{base_url}/committees?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data:
                committee = data[0] if isinstance(data, list) else data.get('committees', [{}])[0]
                print(f"\n🏛️ Committee object structure:")
                for key, value in committee.items():
                    value_type = type(value).__name__
                    value_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"  - {key}: {value_type} = {value_preview}")
        else:
            print(f"❌ Committees API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking committees API: {e}")
    
    # Check hearing response structure
    try:
        response = requests.get(f"{base_url}/hearings?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data:
                hearing = data[0] if isinstance(data, list) else data.get('hearings', [{}])[0]
                print(f"\n🎤 Hearing object structure:")
                for key, value in hearing.items():
                    value_type = type(value).__name__
                    value_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"  - {key}: {value_type} = {value_preview}")
        else:
            print(f"❌ Hearings API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking hearings API: {e}")

def check_existing_relationships():
    """Check if any relationship data exists in database but isn't exposed by API"""
    print("\n🔍 Checking for Existing Relationship Data...")
    
    try:
        import sqlalchemy
        from sqlalchemy import create_engine, text
        
        db_url = get_database_connection()
        if not db_url:
            return False
            
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            # Look for junction/relationship tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND (table_name LIKE '%member%committee%' 
                     OR table_name LIKE '%committee%member%'
                     OR table_name LIKE '%hearing%committee%'
                     OR table_name LIKE '%committee%hearing%')
                ORDER BY table_name;
            """))
            
            junction_tables = [row[0] for row in result.fetchall()]
            print(f"📋 Junction/relationship tables found: {junction_tables}")
            
            if junction_tables:
                for table in junction_tables:
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = count_result.fetchone()[0]
                    print(f"  - {table}: {count} records")
                    
                    if count > 0:
                        # Show sample data
                        sample_result = conn.execute(text(f"SELECT * FROM {table} LIMIT 3"))
                        sample_data = sample_result.fetchall()
                        print(f"    Sample data: {sample_data}")
            else:
                print("❌ No dedicated relationship tables found")
                
                # Check if relationships are stored as JSON in main tables
                print("\n🔍 Checking for JSON relationship columns...")
                
                for table in ['members', 'committees', 'hearings']:
                    columns_result = conn.execute(text(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}' 
                        AND (data_type = 'json' OR data_type = 'jsonb' OR column_name LIKE '%committee%' OR column_name LIKE '%member%')
                    """))
                    
                    json_cols = [row[0] for row in columns_result.fetchall()]
                    if json_cols:
                        print(f"  {table} JSON/relationship columns: {json_cols}")
                        
                        # Check if these columns have data
                        for col in json_cols:
                            sample_result = conn.execute(text(f"SELECT {col} FROM {table} WHERE {col} IS NOT NULL LIMIT 2"))
                            sample_data = sample_result.fetchall()
                            if sample_data:
                                print(f"    {col} sample: {sample_data[0][0]}")
                            else:
                                print(f"    {col}: No data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking relationships: {e}")
        return False

def generate_investigation_report():
    """Generate comprehensive investigation report"""
    print("🏛️ Congressional Database Relationship Investigation")
    print("=" * 60)
    print(f"📅 Investigation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Phase 1: Schema investigation
    schema_success = investigate_schema_structure()
    
    # Phase 2: API response investigation  
    check_api_response_structure()
    
    # Phase 3: Relationship data investigation
    relationship_success = check_existing_relationships()
    
    # Summary and recommendations
    print("\n🎯 INVESTIGATION SUMMARY")
    print("-" * 40)
    
    if schema_success:
        print("✅ Database schema analysis completed")
    else:
        print("❌ Database schema analysis failed")
        
    if relationship_success:
        print("✅ Relationship data analysis completed")
    else:
        print("❌ Relationship data analysis failed")
    
    print("\n🔧 NEXT STEPS RECOMMENDATIONS")
    print("-" * 40)
    print("1. Review database schema findings above")
    print("2. Determine if relationships exist but API doesn't expose them")
    print("3. If no relationships exist, proceed with data collection plan")
    print("4. If relationships exist, fix API implementation")
    print("5. If schema issues, address database structure first")

if __name__ == "__main__":
    generate_investigation_report()