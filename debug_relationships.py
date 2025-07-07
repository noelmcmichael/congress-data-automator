#!/usr/bin/env python3
"""
Debug the relationships to understand why they're not showing up in API.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_relationships():
    """Debug the relationships in the database."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            logger.info("Debugging relationships...")
            
            # Check what member IDs exist
            result = conn.execute(text("SELECT id, first_name, last_name FROM members ORDER BY id LIMIT 10"))
            members = result.fetchall()
            
            logger.info("First 10 members:")
            for member in members:
                logger.info(f"  ID {member[0]}: {member[1]} {member[2]}")
            
            # Check what committee membership records exist
            result = conn.execute(text("SELECT member_id, committee_id, position FROM committee_memberships ORDER BY member_id LIMIT 10"))
            memberships = result.fetchall()
            
            logger.info("\nFirst 10 committee memberships:")
            for membership in memberships:
                logger.info(f"  Member {membership[0]} -> Committee {membership[1]} ({membership[2]})")
            
            # Check if the member IDs in relationships match actual member IDs
            result = conn.execute(text("""
                SELECT cm.member_id, cm.committee_id, cm.position, m.first_name, m.last_name, c.name
                FROM committee_memberships cm
                LEFT JOIN members m ON cm.member_id = m.id
                LEFT JOIN committees c ON cm.committee_id = c.id
                LIMIT 10
            """))
            
            joined_data = result.fetchall()
            
            logger.info("\nJoined relationship data:")
            for row in joined_data:
                member_id, committee_id, position, first_name, last_name, committee_name = row
                member_name = f"{first_name} {last_name}" if first_name else "UNKNOWN"
                logger.info(f"  {member_name} ({member_id}) -> {committee_name} ({committee_id}) [{position}]")
            
            # Check member ID ranges
            result = conn.execute(text("SELECT MIN(id), MAX(id) FROM members"))
            min_id, max_id = result.fetchone()
            logger.info(f"\nMember ID range: {min_id} to {max_id}")
            
            result = conn.execute(text("SELECT MIN(member_id), MAX(member_id) FROM committee_memberships"))
            min_member_id, max_member_id = result.fetchone()
            logger.info(f"Membership member_id range: {min_member_id} to {max_member_id}")
            
            # Check if there are any actual matches
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM committee_memberships cm
                JOIN members m ON cm.member_id = m.id
            """))
            
            valid_relationships = result.scalar()
            logger.info(f"\nValid relationships (with matching member IDs): {valid_relationships}")
            
    except Exception as e:
        logger.error(f"Error debugging relationships: {e}")

if __name__ == "__main__":
    debug_relationships()