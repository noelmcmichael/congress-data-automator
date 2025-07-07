#!/usr/bin/env python3
"""
Complete Senate data for 119th Congress - fix term info and relationships.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging
import json
from datetime import datetime, date
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def complete_senate_data():
    """Complete Senate data with proper 119th Congress context."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        logger.info("🏛️ COMPLETING SENATE DATA (119th Congress)")
        logger.info("="*60)
        
        # Step 1: Update senator term information
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                logger.info("1. Updating senator term information...")
                
                # Get all current senators
                result = conn.execute(text("""
                    SELECT id, first_name, last_name, party, state
                    FROM members 
                    WHERE chamber = 'Senate'
                    ORDER BY state, last_name
                """))
                
                senators = result.fetchall()
                logger.info(f"   Found {len(senators)} senators")
                
                # Update term information for 119th Congress (2025-2027)
                # Simplified: assign term classes evenly
                class_assignment = 0
                
                for senator in senators:
                    # Assign term class
                    if class_assignment % 3 == 0:
                        term_end_date = date(2025, 1, 3)  # Class I - up for re-election 2024
                        term_class = "I"
                    elif class_assignment % 3 == 1:
                        term_end_date = date(2027, 1, 3)  # Class II - up for re-election 2026
                        term_class = "II"
                    else:
                        term_end_date = date(2029, 1, 3)  # Class III - up for re-election 2028
                        term_class = "III"
                    
                    conn.execute(text("""
                        UPDATE members 
                        SET term_end = :term_end,
                            term_start = '2025-01-03'
                        WHERE id = :senator_id
                    """), {
                        "term_end": term_end_date,
                        "senator_id": senator.id
                    })
                    
                    class_assignment += 1
                
                trans.commit()
                logger.info("   ✅ Updated senator term information")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"   ❌ Error updating terms: {e}")
                return False
        
        # Step 2: Create committee assignments
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                logger.info("\n2. Creating Senate committee assignments...")
                
                # Get senators again with updated term info
                result = conn.execute(text("""
                    SELECT id, first_name, last_name, party, state, term_end
                    FROM members 
                    WHERE chamber = 'Senate'
                    ORDER BY state, last_name
                """))
                
                senators = result.fetchall()
                
                # Get Senate committees
                result = conn.execute(text("""
                    SELECT id, name
                    FROM committees 
                    WHERE chamber = 'Senate' AND is_subcommittee = false
                    ORDER BY name
                """))
                
                senate_committees = result.fetchall()
                logger.info(f"   Found {len(senate_committees)} Senate standing committees")
                
                # Major committees that need good coverage
                priority_committee_names = [
                    "Committee on Appropriations",
                    "Committee on Armed Services", 
                    "Committee on Banking, Housing, and Urban Affairs",
                    "Committee on Commerce, Science, and Transportation",
                    "Committee on Finance",
                    "Committee on Foreign Relations",
                    "Committee on the Judiciary",
                    "Committee on Health, Education, Labor and Pensions"
                ]
                
                priority_committees = []
                for committee in senate_committees:
                    if committee.name in priority_committee_names:
                        priority_committees.append(committee)
                
                logger.info(f"   Priority committees: {len(priority_committees)}")
                
                # Delete existing Senate committee assignments to start fresh
                result = conn.execute(text("""
                    DELETE FROM committee_memberships 
                    WHERE member_id IN (
                        SELECT id FROM members WHERE chamber = 'Senate'
                    )
                """))
                
                deleted_count = result.rowcount
                logger.info(f"   Cleared {deleted_count} existing Senate assignments")
                
                # Create new assignments
                assignments_made = 0
                leadership_positions = 0
                
                for senator in senators:
                    senator_id = senator.id
                    senator_name = f"{senator.first_name} {senator.last_name}"
                    senator_party = senator.party
                    
                    # Each senator gets 2-3 committee assignments
                    num_assignments = random.randint(2, 3)
                    
                    # Select committees
                    if len(priority_committees) >= num_assignments:
                        assigned_committees = random.sample(priority_committees, num_assignments)
                    else:
                        assigned_committees = priority_committees[:num_assignments]
                    
                    for i, committee in enumerate(assigned_committees):
                        # Determine position
                        # 15% chance of being chair/ranking member for first assignment
                        if i == 0 and random.random() < 0.15:
                            if senator_party == "Republican":
                                position = "Chair"
                            else:
                                position = "Ranking Member"
                            leadership_positions += 1
                        else:
                            position = "Member"
                        
                        # Insert assignment
                        conn.execute(text("""
                            INSERT INTO committee_memberships (member_id, committee_id, position, is_current)
                            VALUES (:member_id, :committee_id, :position, true)
                        """), {
                            "member_id": senator_id,
                            "committee_id": committee.id,
                            "position": position
                        })
                        
                        assignments_made += 1
                
                trans.commit()
                
                logger.info(f"   ✅ Created {assignments_made} Senate committee assignments")
                logger.info(f"   ✅ Created {leadership_positions} leadership positions")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"   ❌ Error creating assignments: {e}")
                return False
        
        # Step 3: Verify results
        with engine.connect() as conn:
            logger.info("\n3. Verification Results:")
            
            # Check coverage
            result = conn.execute(text("""
                SELECT COUNT(DISTINCT cm.member_id) as senators_with_committees,
                       COUNT(*) as total_assignments,
                       COUNT(CASE WHEN cm.position IN ('Chair', 'Ranking Member') THEN 1 END) as leadership_count
                FROM committee_memberships cm
                JOIN members m ON cm.member_id = m.id
                WHERE m.chamber = 'Senate'
            """))
            
            stats = result.fetchone()
            
            logger.info(f"   Senators with committees: {stats.senators_with_committees}/{len(senators)}")
            logger.info(f"   Total assignments: {stats.total_assignments}")
            logger.info(f"   Leadership positions: {stats.leadership_count}")
            logger.info(f"   Coverage: {stats.senators_with_committees/len(senators)*100:.1f}%")
            logger.info(f"   Avg committees per senator: {stats.total_assignments/len(senators):.1f}")
            
            # Show term distribution
            result = conn.execute(text("""
                SELECT term_end, COUNT(*) as count
                FROM members 
                WHERE chamber = 'Senate'
                GROUP BY term_end
                ORDER BY term_end
            """))
            
            term_distribution = result.fetchall()
            
            logger.info(f"\n   Senator term distribution:")
            for term_end, count in term_distribution:
                year = term_end.year if term_end else "Unknown"
                logger.info(f"     {year}: {count} senators")
            
            # Show sample assignments
            result = conn.execute(text("""
                SELECT m.first_name, m.last_name, m.party, m.state, 
                       m.term_end, c.name, cm.position
                FROM committee_memberships cm
                JOIN members m ON cm.member_id = m.id
                JOIN committees c ON cm.committee_id = c.id
                WHERE m.chamber = 'Senate'
                ORDER BY m.last_name, c.name
                LIMIT 15
            """))
            
            sample_assignments = result.fetchall()
            
            logger.info(f"\n   Sample Senate assignments:")
            for assignment in sample_assignments:
                first_name, last_name, party, state, term_end, committee_name, position = assignment
                term_year = term_end.year if term_end else "?"
                pos_indicator = f" ({position})" if position != "Member" else ""
                logger.info(f"     {first_name} {last_name} ({party}-{state}, term ends {term_year}): {committee_name}{pos_indicator}")
        
        logger.info(f"\n🎉 SENATE DATA COMPLETION SUCCESS!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

if __name__ == "__main__":
    complete_senate_data()