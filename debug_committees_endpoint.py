#!/usr/bin/env python3
"""
Debug the committees endpoint failure
"""

import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'congress_data',
    'user': 'postgres',
    'password': 'mDf3S9ZnBpQqJvGsY1'
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

def test_raw_database_connection():
    """Test raw database connection"""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Test committees table
                cursor.execute("SELECT COUNT(*) FROM committees")
                count = cursor.fetchone()[0]
                print(f"✅ Raw DB connection works: {count} committees")
                
                # Test a simple query
                cursor.execute("SELECT id, name, chamber, is_active FROM committees LIMIT 5")
                committees = cursor.fetchall()
                print("Sample committees:")
                for committee in committees:
                    print(f"  - {committee[1]} ({committee[2]}) - Active: {committee[3]}")
                
                return True
    except Exception as e:
        print(f"❌ Raw DB connection failed: {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test raw SQL through SQLAlchemy
        result = session.execute(text("SELECT COUNT(*) FROM committees")).scalar()
        print(f"✅ SQLAlchemy connection works: {result} committees")
        
        # Test the exact query from the endpoint
        result = session.execute(text("""
            SELECT id, name, chamber, is_active 
            FROM committees 
            WHERE is_active = true 
            ORDER BY name ASC 
            LIMIT 5
        """)).fetchall()
        
        print("Sample committees via SQLAlchemy:")
        for row in result:
            print(f"  - {row[1]} ({row[2]}) - Active: {row[3]}")
            
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

def test_orm_query():
    """Test ORM query simulation"""
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Simulate the ORM query from the endpoint
        from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean
        
        metadata = MetaData()
        committees_table = Table(
            'committees', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('chamber', String),
            Column('is_active', Boolean),
            autoload_with=engine
        )
        
        # Build the query like the endpoint does
        query = session.query(committees_table).filter(committees_table.c.is_active == True)
        query = query.order_by(committees_table.c.name)
        query = query.limit(5)
        
        committees = query.all()
        print(f"✅ ORM-style query works: {len(committees)} committees")
        
        for committee in committees:
            print(f"  - {committee.name} ({committee.chamber})")
            
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ ORM query failed: {e}")
        return False

def test_endpoint_simulation():
    """Simulate the exact endpoint logic"""
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Simulate the endpoint parameters
        page = 1
        limit = 50
        active_only = True
        sort_by = "name"
        sort_order = "asc"
        
        # Build query like endpoint
        query_sql = """
            SELECT id, congress_gov_id, committee_code, name, chamber, committee_type,
                   parent_committee_id, is_subcommittee, description, jurisdiction,
                   chair_member_id, ranking_member_id, phone, email, website, 
                   office_location, is_active, congress_session, created_at, 
                   updated_at, last_scraped_at, hearings_url, members_url, 
                   official_website_url, last_url_update
            FROM committees 
            WHERE is_active = :active_only
            ORDER BY name ASC
            LIMIT :limit OFFSET :offset
        """
        
        offset = (page - 1) * limit
        result = session.execute(text(query_sql), {
            "active_only": active_only,
            "limit": limit,
            "offset": offset
        }).fetchall()
        
        print(f"✅ Endpoint simulation works: {len(result)} committees")
        
        if result:
            first_committee = result[0]
            print(f"First committee: {first_committee[3]} ({first_committee[4]})")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Endpoint simulation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Congressional Data System Diagnosis ===")
    print()
    
    print("1. Testing raw database connection...")
    raw_success = test_raw_database_connection()
    print()
    
    print("2. Testing SQLAlchemy connection...")
    sqlalchemy_success = test_sqlalchemy_connection()
    print()
    
    print("3. Testing ORM query...")
    orm_success = test_orm_query()
    print()
    
    print("4. Testing endpoint simulation...")
    endpoint_success = test_endpoint_simulation()
    print()
    
    print("=== DIAGNOSIS SUMMARY ===")
    print(f"Raw DB Connection: {'✅ PASS' if raw_success else '❌ FAIL'}")
    print(f"SQLAlchemy Connection: {'✅ PASS' if sqlalchemy_success else '❌ FAIL'}")
    print(f"ORM Query: {'✅ PASS' if orm_success else '❌ FAIL'}")
    print(f"Endpoint Simulation: {'✅ PASS' if endpoint_success else '❌ FAIL'}")
    
    if all([raw_success, sqlalchemy_success, orm_success, endpoint_success]):
        print("\n🎉 ALL TESTS PASSED - Issue may be in deployment or environment variables")
    else:
        print("\n⚠️  SOME TESTS FAILED - Database connectivity issues identified")

if __name__ == "__main__":
    main()