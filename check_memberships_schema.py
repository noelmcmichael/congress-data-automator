#!/usr/bin/env python3
"""
Check the committee_memberships table schema.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_memberships_schema():
    """Check the committee_memberships table schema."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            logger.info("Checking committee_memberships schema...")
            
            # Check committee_memberships table structure
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'committee_memberships'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            
            logger.info("committee_memberships table structure:")
            for column in columns:
                column_name, data_type, is_nullable, column_default = column
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                default = f" DEFAULT {column_default}" if column_default else ""
                logger.info(f"  {column_name}: {data_type} {nullable}{default}")
            
            # Check sample data
            result = conn.execute(text("SELECT * FROM committee_memberships LIMIT 3"))
            sample_data = result.fetchall()
            
            logger.info("\nSample committee_memberships data:")
            for row in sample_data:
                logger.info(f"  {row}")
            
    except Exception as e:
        logger.error(f"Error checking schema: {e}")

if __name__ == "__main__":
    check_memberships_schema()