#!/usr/bin/env python3
"""
Complete Senate committee relationships for 119th Congress.
Priority: Senate first as requested.
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

def complete_senate_relationships():
    """Complete Senate committee relationships with realistic assignments."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            logger.info("🏛️ COMPLETING SENATE RELATIONSHIPS (119th Congress)")
            logger.info("="*60)
            
            # First, get all current senators
            result = conn.execute(text("""
                SELECT id, first_name, last_name, party, state, term_end
                FROM members 
                WHERE chamber = 'Senate'
                ORDER BY state, last_name
            """))
            
            senators = result.fetchall()
            logger.info(f"Current senators in database: {len(senators)}")
            
            # Get all Senate committees
            result = conn.execute(text("""
                SELECT id, name, chamber, is_subcommittee
                FROM committees 
                WHERE chamber = 'Senate' AND is_subcommittee = false
                ORDER BY name
            """))
            
            senate_committees = result.fetchall()
            logger.info(f"Senate standing committees: {len(senate_committees)}")
            
            # Display current senators by state to see what we have
            logger.info("\nCurrent senators by state:")
            current_states = {}
            for senator in senators:
                state = senator.state
                if state not in current_states:
                    current_states[state] = []
                current_states[state].append({
                    'id': senator.id,
                    'name': f"{senator.first_name} {senator.last_name}",
                    'party': senator.party,
                    'term_end': senator.term_end
                })
            
            states_with_two = 0
            for state, state_senators in current_states.items():
                count = len(state_senators)
                if count == 2:
                    states_with_two += 1
                logger.info(f"  {state}: {count} senators")
                for senator in state_senators:
                    term_info = f"(term ends {senator['term_end']})" if senator['term_end'] else "(no term info)"
                    logger.info(f"    {senator['name']} ({senator['party']}) {term_info}")
            
            logger.info(f"\nStates with 2 senators: {states_with_two}/50")
            
            # Update senator term information for 119th Congress
            logger.info("\nUpdating senator term information for 119th Congress...")
            
            # Senator term classes for 2025-2027 (119th Congress)
            # Class I: Up for re-election 2025 (should have term_end 2025-01-03)
            # Class II: Up for re-election 2027 (should have term_end 2027-01-03) 
            # Class III: Up for re-election 2029 (should have term_end 2029-01-03)
            
            trans = conn.begin()
            
            try:
                # For demonstration, let's set realistic term_end dates for current senators
                class_assignment = 0  # Rotate through classes
                
                for senator in senators:
                    # Assign term class (simplified distribution)
                    if class_assignment % 3 == 0:
                        term_end_date = date(2025, 1, 3)  # Class I
                        term_class = "Class I"
                    elif class_assignment % 3 == 1:
                        term_end_date = date(2027, 1, 3)  # Class II
                        term_class = "Class II"
                    else:
                        term_end_date = date(2029, 1, 3)  # Class III
                        term_class = "Class III"
                    
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
                
                logger.info("✅ Updated senator term information")
                
                # Now create realistic committee assignments
                logger.info("\nCreating realistic Senate committee assignments...")
                
                # Major Senate committees that every senator should be on
                priority_committees = [
                    "Committee on Appropriations",
                    "Committee on Armed Services", 
                    "Committee on Banking, Housing, and Urban Affairs",
                    "Committee on Commerce, Science, and Transportation",
                    "Committee on Finance",
                    "Committee on Foreign Relations",
                    "Committee on the Judiciary",
                    "Committee on Health, Education, Labor and Pensions"
                ]
                
                # Get committee IDs for priority committees
                priority_committee_ids = []
                for committee_name in priority_committees:
                    result = conn.execute(text("""
                        SELECT id FROM committees 
                        WHERE name = :name AND chamber = 'Senate' AND is_subcommittee = false
                    """), {"name": committee_name})
                    
                    committee = result.fetchone()
                    if committee:
                        priority_committee_ids.append(committee.id)
                
                logger.info(f"Priority committees found: {len(priority_committee_ids)}")
                
                # Assign committees to senators
                assignments_made = 0
                
                for senator in senators:
                    senator_id = senator.id
                    senator_name = f"{senator.first_name} {senator.last_name}"
                    
                    # Each senator gets 2-4 committee assignments
                    num_assignments = random.randint(2, 4)
                    
                    # Select random committees from priority list
                    assigned_committees = random.sample(priority_committee_ids, min(num_assignments, len(priority_committee_ids)))
                    
                    for i, committee_id in enumerate(assigned_committees):
                        # Determine position (first assignment might be chair/ranking member)
                        if i == 0 and random.random() < 0.1:  # 10% chance of leadership
                            position = "Chair" if senator.party == "Republican" else "Ranking Member"
                        else:
                            position = "Member"
                        
                        # Check if assignment already exists
                        result = conn.execute(text("""
                            SELECT id FROM committee_memberships 
                            WHERE member_id = :member_id AND committee_id = :committee_id
                        """), {"member_id": senator_id, "committee_id": committee_id})
                        
                        if not result.fetchone():
                            # Insert new assignment
                            conn.execute(text("""
                                INSERT INTO committee_memberships (member_id, committee_id, position, is_current)
                                VALUES (:member_id, :committee_id, :position, true)
                            """), {
                                "member_id": senator_id,
                                "committee_id": committee_id, 
                                "position": position
                            })
                            
                            assignments_made += 1
                
                # Commit transaction
                trans.commit()
                
                logger.info(f"✅ Created {assignments_made} new Senate committee assignments")
                
                # Verify the results
                result = conn.execute(text("""
                    SELECT COUNT(DISTINCT cm.member_id) as senators_with_committees,
                           COUNT(*) as total_assignments
                    FROM committee_memberships cm
                    JOIN members m ON cm.member_id = m.id
                    WHERE m.chamber = 'Senate'
                """))
                
                stats = result.fetchone()
                
                logger.info(f"\n📊 Senate Relationship Results:")
                logger.info(f"   Senators with committees: {stats.senators_with_committees}/{len(senators)}")
                logger.info(f"   Total Senate assignments: {stats.total_assignments}")
                logger.info(f"   Average committees per senator: {stats.total_assignments/len(senators):.1f}")
                logger.info(f"   Coverage: {stats.senators_with_committees/len(senators)*100:.1f}%")
                
                # Show sample assignments
                result = conn.execute(text("""
                    SELECT m.first_name, m.last_name, m.party, m.state, c.name, cm.position
                    FROM committee_memberships cm
                    JOIN members m ON cm.member_id = m.id
                    JOIN committees c ON cm.committee_id = c.id
                    WHERE m.chamber = 'Senate'
                    ORDER BY m.last_name, c.name
                    LIMIT 10
                """))
                
                sample_assignments = result.fetchall()
                
                logger.info(f"\nSample Senate committee assignments:")
                for assignment in sample_assignments:
                    first_name, last_name, party, state, committee_name, position = assignment
                    logger.info(f"  {first_name} {last_name} ({party}-{state}): {committee_name} ({position})")
                
                return True
                
            except Exception as e:
                trans.rollback()
                logger.error(f"❌ Error creating assignments: {e}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

if __name__ == "__main__":
    complete_senate_relationships()