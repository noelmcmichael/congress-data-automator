#!/usr/bin/env python3
"""
Check the database schema to understand the structure.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_schema():
    """Check the database schema."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            logger.info("Checking database schema...")
            
            # Check committees table structure
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'committees'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            
            logger.info("Committees table structure:")
            for column in columns:
                column_name, data_type, is_nullable, column_default = column
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                default = f" DEFAULT {column_default}" if column_default else ""
                logger.info(f"  {column_name}: {data_type} {nullable}{default}")
            
            # Check sample data
            result = conn.execute(text("SELECT * FROM committees LIMIT 3"))
            sample_data = result.fetchall()
            
            logger.info("\nSample committee data:")
            for row in sample_data:
                logger.info(f"  {row}")
            
            # Check the columns we need
            required_columns = ['id', 'name', 'chamber', 'jurisdiction', 'is_active', 'is_subcommittee']
            existing_columns = [col[0] for col in columns]
            
            logger.info("\nColumn check:")
            for col in required_columns:
                if col in existing_columns:
                    logger.info(f"  ✅ {col}")
                else:
                    logger.info(f"  ❌ {col} (missing)")
            
            # Check for extra columns
            extra_columns = [col for col in existing_columns if col not in required_columns]
            if extra_columns:
                logger.info(f"\nExtra columns: {extra_columns}")
            
    except Exception as e:
        logger.error(f"Error checking schema: {e}")

if __name__ == "__main__":
    check_schema()