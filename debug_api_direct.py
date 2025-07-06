#!/usr/bin/env python3
"""
Direct API debugging - create a minimal test version to debug the issue
"""
import sys
sys.path.insert(0, '/Users/noelmcmichael/Workspace/congress_data_automator/backend')

from typing import List, Optional
from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, create_engine
from sqlalchemy.orm import sessionmaker

from app.models.member import Member
from app.schemas.member import MemberResponse

# Create a test database connection
def get_test_db():
    """Create test database session"""
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    engine = create_engine(connection_string, echo=True)  # echo=True for debugging
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_filter_logic_direct():
    """Test filter logic directly with database"""
    print("Testing Filter Logic Directly")
    print("="*40)
    
    # Create database session
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    engine = create_engine(connection_string, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Test 1: Basic query (should return all 538 members)
        print("\n1. Testing basic query (no filters):")
        query = db.query(Member)
        all_members = query.all()
        print(f"   Total members: {len(all_members)}")
        
        # Test 2: Party filter
        print("\n2. Testing party filter (Republican):")
        query = db.query(Member)
        query = query.filter(Member.party == 'Republican')
        republican_members = query.all()
        print(f"   Republican members: {len(republican_members)}")
        
        # Test 3: Chamber filter
        print("\n3. Testing chamber filter (House):")
        query = db.query(Member)
        query = query.filter(Member.chamber == 'House')
        house_members = query.all()
        print(f"   House members: {len(house_members)}")
        
        # Test 4: Combined filters
        print("\n4. Testing combined filters (Democratic + CA):")
        query = db.query(Member)
        query = query.filter(Member.party == 'Democratic')
        query = query.filter(Member.state == 'CA')
        dem_ca_members = query.all()
        print(f"   Democratic California members: {len(dem_ca_members)}")
        
        # Test 5: Pagination
        print("\n5. Testing pagination (limit 50):")
        query = db.query(Member)
        paginated_members = query.limit(50).all()
        print(f"   Paginated members: {len(paginated_members)}")
        
        # Test 6: Simulate the exact API logic
        print("\n6. Simulating exact API logic:")
        
        # Parameters from failing API call
        page = 1
        limit = 50
        party = "Republican"
        chamber = None
        state = None
        
        query = db.query(Member)
        
        # Apply filters exactly as in the API
        if party:
            print(f"   Applying party filter: {party}")
            query = query.filter(Member.party == party)
        if chamber:
            print(f"   Applying chamber filter: {chamber}")
            query = query.filter(Member.chamber == chamber)
        if state:
            print(f"   Applying state filter: {state}")
            query = query.filter(Member.state == state)
        
        # Apply sorting
        query = query.order_by(Member.last_name)
        
        # Apply pagination
        offset = (page - 1) * limit
        members = query.offset(offset).limit(limit).all()
        
        print(f"   Final result count: {len(members)}")
        print("   Sample results:")
        for i, member in enumerate(members[:3]):
            print(f"     {i+1}. {member.first_name} {member.last_name} ({member.party}, {member.chamber}, {member.state})")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def main():
    """Main execution function"""
    test_filter_logic_direct()

if __name__ == "__main__":
    main()