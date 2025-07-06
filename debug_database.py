#!/usr/bin/env python3
"""
Database inspection script to debug filter logic issues
"""
import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def connect_to_database():
    """Connect to the production database via Cloud SQL proxy"""
    # Connect via Cloud SQL proxy on port 5433
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string, echo=True)  # echo=True for SQL logging
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return None

def inspect_member_data(engine):
    """Inspect actual member data values"""
    print("\n" + "="*50)
    print("INSPECTING MEMBER DATA")
    print("="*50)
    
    with engine.connect() as conn:
        # Check total count
        result = conn.execute(text("SELECT COUNT(*) FROM members"))
        total_count = result.scalar()
        print(f"Total members in database: {total_count}")
        
        # Check distinct party values
        result = conn.execute(text("SELECT DISTINCT party FROM members ORDER BY party"))
        parties = [row[0] for row in result.fetchall()]
        print(f"Distinct party values: {parties}")
        
        # Check distinct chamber values
        result = conn.execute(text("SELECT DISTINCT chamber FROM members ORDER BY chamber"))
        chambers = [row[0] for row in result.fetchall()]
        print(f"Distinct chamber values: {chambers}")
        
        # Check distinct state values (first 10)
        result = conn.execute(text("SELECT DISTINCT state FROM members ORDER BY state LIMIT 10"))
        states = [row[0] for row in result.fetchall()]
        print(f"Sample state values: {states}")
        
        # Check party distribution
        result = conn.execute(text("SELECT party, COUNT(*) FROM members GROUP BY party ORDER BY COUNT(*) DESC"))
        party_counts = result.fetchall()
        print(f"Party distribution: {dict(party_counts)}")
        
        # Check chamber distribution
        result = conn.execute(text("SELECT chamber, COUNT(*) FROM members GROUP BY chamber ORDER BY COUNT(*) DESC"))
        chamber_counts = result.fetchall()
        print(f"Chamber distribution: {dict(chamber_counts)}")
        
        # Sample data with all relevant columns
        print("\nSample member data:")
        result = conn.execute(text("SELECT id, first_name, last_name, party, chamber, state FROM members LIMIT 5"))
        for row in result.fetchall():
            print(f"  ID: {row[0]}, Name: {row[1]} {row[2]}, Party: {row[3]}, Chamber: {row[4]}, State: {row[5]}")

def test_filter_queries(engine):
    """Test actual filter queries directly on database"""
    print("\n" + "="*50)
    print("TESTING FILTER QUERIES DIRECTLY")
    print("="*50)
    
    with engine.connect() as conn:
        # Test party filter
        print("\n1. Testing party filter (Republican):")
        result = conn.execute(text("SELECT COUNT(*) FROM members WHERE party = 'Republican'"))
        republican_count = result.scalar()
        print(f"   Republican members: {republican_count}")
        
        print("\n2. Testing party filter (Democratic):")
        result = conn.execute(text("SELECT COUNT(*) FROM members WHERE party = 'Democratic'"))
        democratic_count = result.scalar()
        print(f"   Democratic members: {democratic_count}")
        
        print("\n3. Testing chamber filter (house):")
        result = conn.execute(text("SELECT COUNT(*) FROM members WHERE chamber = 'house'"))
        house_count = result.scalar()
        print(f"   House members: {house_count}")
        
        print("\n4. Testing chamber filter (senate):")
        result = conn.execute(text("SELECT COUNT(*) FROM members WHERE chamber = 'senate'"))
        senate_count = result.scalar()
        print(f"   Senate members: {senate_count}")
        
        print("\n5. Testing state filter (CA):")
        result = conn.execute(text("SELECT COUNT(*) FROM members WHERE state = 'CA'"))
        ca_count = result.scalar()
        print(f"   California members: {ca_count}")
        
        print("\n6. Testing combined filter (Democratic + CA):")
        result = conn.execute(text("SELECT COUNT(*) FROM members WHERE party = 'Democratic' AND state = 'CA'"))
        dem_ca_count = result.scalar()
        print(f"   Democratic California members: {dem_ca_count}")
        
        print("\n7. Testing invalid party filter (XYZ):")
        result = conn.execute(text("SELECT COUNT(*) FROM members WHERE party = 'XYZ'"))
        invalid_count = result.scalar()
        print(f"   Invalid party members: {invalid_count}")

def test_sqlalchemy_queries(engine):
    """Test SQLAlchemy queries to compare with raw SQL"""
    print("\n" + "="*50)
    print("TESTING SQLALCHEMY QUERIES")
    print("="*50)
    
    # Add the backend directory to the path
    sys.path.insert(0, '/Users/noelmcmichael/Workspace/congress_data_automator/backend')
    
    try:
        from app.models.member import Member
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test basic query
        print("\n1. Testing basic SQLAlchemy query:")
        total_members = session.query(Member).count()
        print(f"   Total members via SQLAlchemy: {total_members}")
        
        # Test party filter
        print("\n2. Testing party filter via SQLAlchemy:")
        republican_members = session.query(Member).filter(Member.party == 'Republican').count()
        print(f"   Republican members via SQLAlchemy: {republican_members}")
        
        # Test chamber filter
        print("\n3. Testing chamber filter via SQLAlchemy:")
        house_members = session.query(Member).filter(Member.chamber == 'house').count()
        print(f"   House members via SQLAlchemy: {house_members}")
        
        # Test combined filter
        print("\n4. Testing combined filter via SQLAlchemy:")
        combined_members = session.query(Member).filter(
            Member.party == 'Democratic',
            Member.state == 'CA'
        ).count()
        print(f"   Democratic California members via SQLAlchemy: {combined_members}")
        
        session.close()
        
    except Exception as e:
        print(f"Error testing SQLAlchemy queries: {e}")

def main():
    """Main execution function"""
    print("Congressional Data API - Database Inspection Tool")
    print("="*60)
    
    # Connect to database
    engine = connect_to_database()
    if not engine:
        print("Failed to connect to database. Exiting.")
        return
    
    try:
        # Inspect member data
        inspect_member_data(engine)
        
        # Test filter queries directly
        test_filter_queries(engine)
        
        # Test SQLAlchemy queries
        test_sqlalchemy_queries(engine)
        
    except Exception as e:
        logger.error(f"Error during inspection: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        engine.dispose()

if __name__ == "__main__":
    main()