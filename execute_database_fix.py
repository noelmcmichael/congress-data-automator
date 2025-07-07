#!/usr/bin/env python3
"""
Execute the database fix to replace current committees with real congressional structure.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_database_fix():
    """Execute the database fix SQL script."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        # Read the SQL fix file
        with open('simple_database_fix.sql', 'r') as f:
            sql_script = f.read()
        
        logger.info("Starting database fix...")
        
        with engine.connect() as conn:
            # Begin transaction
            trans = conn.begin()
            
            try:
                # Split the SQL script into individual statements
                statements = sql_script.split(';')
                
                for i, statement in enumerate(statements):
                    statement = statement.strip()
                    if statement:
                        logger.info(f"Executing statement {i+1}/{len(statements)}")
                        conn.execute(text(statement))
                
                # Commit transaction
                trans.commit()
                logger.info("✅ Database fix completed successfully!")
                
                # Verify the fix
                return verify_fix(conn)
                
            except Exception as e:
                trans.rollback()
                logger.error(f"❌ Error executing database fix: {e}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error connecting to database: {e}")
        return False

def verify_fix(conn):
    """Verify the database fix was successful."""
    
    try:
        logger.info("Verifying database fix...")
        
        # Check committee count
        result = conn.execute(text("SELECT COUNT(*) FROM committees"))
        committee_count = result.scalar()
        logger.info(f"Total committees: {committee_count}")
        
        # Check main committees vs subcommittees
        result = conn.execute(text("""
            SELECT is_subcommittee, COUNT(*) as count 
            FROM committees 
            GROUP BY is_subcommittee 
            ORDER BY is_subcommittee
        """))
        committee_types = result.fetchall()
        
        main_committees = 0
        subcommittees = 0
        
        for is_sub, count in committee_types:
            if is_sub:
                subcommittees = count
                logger.info(f"Subcommittees: {count}")
            else:
                main_committees = count
                logger.info(f"Main committees: {count}")
        
        # Check for major committees
        major_committees = [
            'Committee on Appropriations',
            'Committee on Armed Services', 
            'Committee on the Judiciary',
            'Committee on Foreign Affairs',
            'Committee on Energy and Commerce',
            'Committee on Ways and Means',
            'Committee on Financial Services'
        ]
        
        major_found = 0
        logger.info("Checking for major committees:")
        for committee in major_committees:
            result = conn.execute(text(
                "SELECT COUNT(*) FROM committees WHERE name = :name"
            ), {"name": committee})
            found = result.scalar() > 0
            if found:
                major_found += 1
            logger.info(f"{'✅' if found else '❌'} {committee}")
        
        # Check relationships
        result = conn.execute(text("SELECT COUNT(*) FROM committee_memberships"))
        relationship_count = result.scalar()
        logger.info(f"Committee memberships: {relationship_count}")
        
        # Success criteria
        success = (
            committee_count >= 150 and  # Should have ~199 committees
            main_committees >= 30 and   # Should have 35 main committees
            major_found >= 5 and        # Should have most major committees
            relationship_count >= 50    # Should have ~74 relationships
        )
        
        if success:
            logger.info("✅ Database fix verification successful!")
            return True
        else:
            logger.warning("⚠️  Database fix verification shows issues")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error verifying database fix: {e}")
        return False

def main():
    """Main function to execute the database fix."""
    
    logger.info("=== Congressional Database Fix ===")
    
    # Check if SQL file exists
    if not os.path.exists('simple_database_fix.sql'):
        logger.error("❌ SQL fix file not found!")
        return False
    
    # Execute the database fix
    success = execute_database_fix()
    
    if success:
        logger.info("🎉 Database fix completed successfully!")
        return True
    else:
        logger.error("❌ Database fix failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)