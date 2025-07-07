#!/usr/bin/env python3
"""
Check what committees are currently in the database.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_committees():
    """Check what committees are currently in the database."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            logger.info("Current committees in database:")
            
            # Get all committees
            result = conn.execute(text("""
                SELECT id, name, chamber, is_subcommittee, is_active
                FROM committees 
                ORDER BY chamber, name
            """))
            
            committees = result.fetchall()
            
            house_count = 0
            senate_count = 0
            
            for committee in committees:
                id, name, chamber, is_subcommittee, is_active = committee
                committee_type = "Subcommittee" if is_subcommittee else "Main"
                status = "Active" if is_active else "Inactive"
                logger.info(f"{id}: {name} ({chamber}) [{committee_type}] [{status}]")
                
                if chamber == "House":
                    house_count += 1
                elif chamber == "Senate":
                    senate_count += 1
            
            logger.info(f"\nSummary:")
            logger.info(f"House committees: {house_count}")
            logger.info(f"Senate committees: {senate_count}")
            logger.info(f"Total committees: {len(committees)}")
            
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
            
            logger.info(f"\nMajor committees check:")
            for committee in major_committees:
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM committees WHERE name = :name"
                ), {"name": committee})
                found = result.scalar() > 0
                logger.info(f"{'✅' if found else '❌'} {committee}")
            
    except Exception as e:
        logger.error(f"Error checking committees: {e}")

if __name__ == "__main__":
    check_committees()