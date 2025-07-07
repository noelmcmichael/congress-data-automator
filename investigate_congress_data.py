#!/usr/bin/env python3
"""
Investigate the current congressional data to understand what needs to be corrected.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def investigate_congress_data():
    """Investigate current congressional data for accuracy."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            logger.info("🔍 INVESTIGATING CONGRESSIONAL DATA")
            logger.info("="*60)
            
            # Check current congress number context
            logger.info("1. Current Congress Context:")
            current_year = datetime.now().year
            logger.info(f"   Current year: {current_year}")
            logger.info(f"   119th Congress: 2025-2027 (Current)")
            logger.info(f"   118th Congress: 2023-2025 (Previous)")
            
            # Check member data for congress indicators
            result = conn.execute(text("""
                SELECT COUNT(*) as total_members,
                       COUNT(CASE WHEN chamber = 'Senate' THEN 1 END) as senate_count,
                       COUNT(CASE WHEN chamber = 'House' THEN 1 END) as house_count
                FROM members
            """))
            
            counts = result.fetchone()
            logger.info(f"\n2. Member Counts:")
            logger.info(f"   Total members: {counts.total_members}")
            logger.info(f"   Senate: {counts.senate_count}")
            logger.info(f"   House: {counts.house_count}")
            logger.info(f"   Expected: 535 total (100 Senate + 435 House)")
            
            # Check if we have senator term information
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'members' AND column_name LIKE '%term%'
                ORDER BY column_name
            """))
            
            term_columns = result.fetchall()
            logger.info(f"\n3. Senator Term Information:")
            if term_columns:
                for col in term_columns:
                    logger.info(f"   {col.column_name}: {col.data_type} ({col.is_nullable})")
            else:
                logger.warning("   ❌ No term information columns found")
            
            # Check committee hierarchy
            result = conn.execute(text("""
                SELECT COUNT(*) as total_committees,
                       COUNT(CASE WHEN is_subcommittee = false THEN 1 END) as main_committees,
                       COUNT(CASE WHEN is_subcommittee = true THEN 1 END) as subcommittees,
                       COUNT(CASE WHEN parent_committee_id IS NOT NULL THEN 1 END) as with_parent
                FROM committees
            """))
            
            committee_counts = result.fetchone()
            logger.info(f"\n4. Committee Hierarchy:")
            logger.info(f"   Total committees: {committee_counts.total_committees}")
            logger.info(f"   Main committees: {committee_counts.main_committees}")
            logger.info(f"   Subcommittees: {committee_counts.subcommittees}")
            logger.info(f"   With parent links: {committee_counts.with_parent}")
            
            # Check for missing parent relationships
            if committee_counts.subcommittees > committee_counts.with_parent:
                logger.warning(f"   ⚠️  Missing parent links: {committee_counts.subcommittees - committee_counts.with_parent}")
            
            # Check relationship coverage by chamber
            result = conn.execute(text("""
                SELECT m.chamber,
                       COUNT(DISTINCT m.id) as total_members,
                       COUNT(DISTINCT cm.member_id) as members_with_committees
                FROM members m
                LEFT JOIN committee_memberships cm ON m.id = cm.member_id
                GROUP BY m.chamber
            """))
            
            chamber_coverage = result.fetchall()
            logger.info(f"\n5. Relationship Coverage by Chamber:")
            for chamber, total, with_committees in chamber_coverage:
                coverage_pct = (with_committees / total * 100) if total > 0 else 0
                logger.info(f"   {chamber}: {with_committees}/{total} ({coverage_pct:.1f}%)")
            
            # Check for senators and their states (to determine term classes)
            result = conn.execute(text("""
                SELECT state, COUNT(*) as senator_count
                FROM members 
                WHERE chamber = 'Senate'
                GROUP BY state
                ORDER BY state
            """))
            
            senate_by_state = result.fetchall()
            logger.info(f"\n6. Senate Representation:")
            states_with_two_senators = 0
            for state, count in senate_by_state:
                if count == 2:
                    states_with_two_senators += 1
                logger.info(f"   {state}: {count} senators")
            
            logger.info(f"   States with 2 senators: {states_with_two_senators}")
            logger.info(f"   Expected: 50 states with 2 senators each")
            
            # Sample some member data to see what we have
            result = conn.execute(text("""
                SELECT first_name, last_name, chamber, state, party, district
                FROM members 
                WHERE chamber = 'Senate'
                ORDER BY state, last_name
                LIMIT 10
            """))
            
            sample_senators = result.fetchall()
            logger.info(f"\n7. Sample Senator Data:")
            for senator in sample_senators:
                first_name, last_name, chamber, state, party, district = senator
                logger.info(f"   {first_name} {last_name} ({party}-{state})")
            
            # Check committee data sample
            result = conn.execute(text("""
                SELECT name, chamber, committee_type, is_subcommittee, parent_committee_id
                FROM committees 
                WHERE chamber = 'Senate' AND is_subcommittee = false
                ORDER BY name
                LIMIT 5
            """))
            
            sample_committees = result.fetchall()
            logger.info(f"\n8. Sample Senate Committee Data:")
            for committee in sample_committees:
                name, chamber, committee_type, is_subcommittee, parent_id = committee
                logger.info(f"   {name} ({committee_type}) - Parent: {parent_id}")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Error investigating data: {e}")
        return False

if __name__ == "__main__":
    investigate_congress_data()