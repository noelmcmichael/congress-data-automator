#!/usr/bin/env python3
"""
Test database connection and basic schema setup
"""
import os
import sys
sys.path.append('backend')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base
from backend.app.models.member import Member
from backend.app.models.committee import Committee, CommitteeMembership

def test_db_connection():
    """Test database connection and create tables if needed"""
    
    # Load database URL from environment
    db_url = os.getenv('DATABASE_URL', 'postgresql://noelmcmichael@127.0.0.1:5432/congress_data')
    print(f"Testing connection to: {db_url}")
    
    try:
        # Create engine
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified!")
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Test basic queries
        member_count = session.query(Member).count()
        committee_count = session.query(Committee).count()
        membership_count = session.query(CommitteeMembership).count()
        
        print(f"📊 Current database state:")
        print(f"   Members: {member_count}")
        print(f"   Committees: {committee_count}")
        print(f"   Memberships: {membership_count}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1)