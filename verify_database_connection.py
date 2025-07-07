#!/usr/bin/env python3
"""
Verify database connection and check current state before implementing fix.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_database_connection():
    """Verify we can connect to the production database."""
    
    # Try multiple connection strings
    connection_strings = [
        "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data",
        "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5432/congress_data?host=/cloudsql/chefgavin:us-central1:congressional-db",
        "postgresql://postgres@localhost:5433/congress_data"
    ]
    
    for conn_str in connection_strings:
        try:
            logger.info(f"Attempting connection with: {conn_str}")
            engine = create_engine(conn_str)
            
            with engine.connect() as conn:
                # Test basic query
                result = conn.execute(text("SELECT 1 as test"))
                test_value = result.scalar()
                
                if test_value == 1:
                    logger.info(f"✅ Database connection successful!")
                    return engine
                    
        except OperationalError as e:
            logger.warning(f"Connection failed: {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            continue
    
    logger.error("❌ Could not connect to database with any connection string")
    return None

def check_current_database_state(engine):
    """Check the current state of the database."""
    
    try:
        with engine.connect() as conn:
            logger.info("Checking current database state...")
            
            # Check members count
            result = conn.execute(text("SELECT COUNT(*) FROM members"))
            member_count = result.scalar()
            logger.info(f"Current members: {member_count}")
            
            # Check committees count
            result = conn.execute(text("SELECT COUNT(*) FROM committees"))
            committee_count = result.scalar()
            logger.info(f"Current committees: {committee_count}")
            
            # Check relationships count
            result = conn.execute(text("SELECT COUNT(*) FROM committee_memberships"))
            relationship_count = result.scalar()
            logger.info(f"Current committee memberships: {relationship_count}")
            
            # Check committee types
            result = conn.execute(text("""
                SELECT is_subcommittee, COUNT(*) as count 
                FROM committees 
                GROUP BY is_subcommittee
            """))
            committee_types = result.fetchall()
            logger.info(f"Committee types: {dict(committee_types)}")
            
            # Check major committees
            major_committees = [
                'Committee on Appropriations',
                'Committee on Armed Services', 
                'Committee on the Judiciary',
                'Committee on Foreign Affairs',
                'Committee on Energy and Commerce'
            ]
            
            found_major = 0
            for committee in major_committees:
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM committees WHERE name = :name"
                ), {"name": committee})
                if result.scalar() > 0:
                    found_major += 1
            
            logger.info(f"Major committees found: {found_major}/{len(major_committees)}")
            
            return {
                "members": member_count,
                "committees": committee_count,
                "relationships": relationship_count,
                "committee_types": dict(committee_types),
                "major_committees_found": found_major
            }
            
    except Exception as e:
        logger.error(f"Error checking database state: {e}")
        return None

def main():
    """Main function to verify database connection and state."""
    
    logger.info("=== Database Connection Verification ===")
    
    # Step 1: Verify database connection
    engine = verify_database_connection()
    if not engine:
        logger.error("Cannot proceed without database connection")
        return False
    
    # Step 2: Check current database state
    state = check_current_database_state(engine)
    if not state:
        logger.error("Could not check database state")
        return False
    
    # Step 3: Analyze state
    logger.info("=== Database State Analysis ===")
    logger.info(f"Members: {state['members']}")
    logger.info(f"Committees: {state['committees']}")
    logger.info(f"Relationships: {state['relationships']}")
    logger.info(f"Committee types: {state['committee_types']}")
    logger.info(f"Major committees: {state['major_committees_found']}")
    
    # Determine if fix is needed
    issues = []
    if state['relationships'] == 0:
        issues.append("No member-committee relationships")
    if state['major_committees_found'] < 3:
        issues.append("Missing major committees")
    if state['committee_types'].get(False, 0) < 30:
        issues.append("Insufficient main committees")
    
    if issues:
        logger.warning("=== Issues Found ===")
        for issue in issues:
            logger.warning(f"⚠️  {issue}")
        logger.info("Database fix is needed")
        return True
    else:
        logger.info("✅ Database appears to be in good state")
        return False

if __name__ == "__main__":
    needs_fix = main()
    sys.exit(0 if needs_fix else 1)