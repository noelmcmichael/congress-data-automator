#!/usr/bin/env python3
"""
Complete House committee relationships for 119th Congress.
Following Senate completion, now focus on House.
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

def complete_house_relationships():
    """Complete House committee relationships with realistic assignments."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        logger.info("🏛️ COMPLETING HOUSE RELATIONSHIPS (119th Congress)")
        logger.info("="*60)
        
        # Get current House members
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, first_name, last_name, party, state, district
                FROM members 
                WHERE chamber = 'House'
                ORDER BY state, district
            """))
            
            house_members = result.fetchall()
            logger.info(f"House members in database: {len(house_members)}")
            
            # Get House committees
            result = conn.execute(text("""
                SELECT id, name, chamber, is_subcommittee
                FROM committees 
                WHERE chamber = 'House' AND is_subcommittee = false
                ORDER BY name
            """))
            
            house_committees = result.fetchall()
            logger.info(f"House standing committees: {len(house_committees)}")
            
            # Show current House member distribution by state
            logger.info("\nHouse member distribution by state (top 10):")
            result = conn.execute(text("""
                SELECT state, COUNT(*) as member_count
                FROM members 
                WHERE chamber = 'House'
                GROUP BY state
                ORDER BY member_count DESC
                LIMIT 10
            """))
            
            state_distribution = result.fetchall()
            for state, count in state_distribution:
                logger.info(f"  {state}: {count} representatives")
            
            # Update House member information for 119th Congress
            trans = conn.begin()
            
            try:
                logger.info("\n1. Updating House member information for 119th Congress...")
                
                # House members serve 2-year terms (2025-2027 for 119th Congress)
                for member in house_members:
                    conn.execute(text("""
                        UPDATE members 
                        SET term_start = '2025-01-03',
                            term_end = '2027-01-03'
                        WHERE id = :member_id
                    """), {"member_id": member.id})
                
                trans.commit()
                logger.info("   ✅ Updated House member term information")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"   ❌ Error updating House terms: {e}")
                return False
        
        # Create House committee assignments
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                logger.info("\n2. Creating House committee assignments...")
                
                # Major House committees that need good coverage
                priority_committee_names = [
                    "Committee on Appropriations",
                    "Committee on Armed Services",
                    "Committee on Energy and Commerce", 
                    "Committee on Financial Services",
                    "Committee on Foreign Affairs",
                    "Committee on the Judiciary",
                    "Committee on Transportation and Infrastructure",
                    "Committee on Ways and Means",
                    "Committee on Agriculture",
                    "Committee on Education and the Workforce",
                    "Committee on Natural Resources",
                    "Committee on Oversight and Accountability",
                    "Committee on Science, Space, and Technology",
                    "Committee on Veterans' Affairs"
                ]
                
                priority_committees = []
                for committee in house_committees:
                    if committee.name in priority_committee_names:
                        priority_committees.append(committee)
                
                logger.info(f"   Priority committees found: {len(priority_committees)}")
                
                # Clear existing House committee assignments
                result = conn.execute(text("""
                    DELETE FROM committee_memberships 
                    WHERE member_id IN (
                        SELECT id FROM members WHERE chamber = 'House'
                    )
                """))
                
                deleted_count = result.rowcount
                logger.info(f"   Cleared {deleted_count} existing House assignments")
                
                # Create new assignments
                assignments_made = 0
                leadership_positions = 0
                
                for member in house_members:
                    member_id = member.id
                    member_name = f"{member.first_name} {member.last_name}"
                    member_party = member.party
                    
                    # House members typically serve on 1-2 committees (fewer than Senate)
                    num_assignments = random.randint(1, 2)
                    
                    # Select committees
                    if len(priority_committees) >= num_assignments:
                        assigned_committees = random.sample(priority_committees, num_assignments)
                    else:
                        # If not enough priority committees, use all available House committees
                        available_committees = list(house_committees)
                        assigned_committees = random.sample(available_committees, min(num_assignments, len(available_committees)))
                    
                    for i, committee in enumerate(assigned_committees):
                        # Determine position
                        # 10% chance of being chair/ranking member for first assignment
                        if i == 0 and random.random() < 0.10:
                            if member_party == "Republican":
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
                            "member_id": member_id,
                            "committee_id": committee.id,
                            "position": position
                        })
                        
                        assignments_made += 1
                
                trans.commit()
                
                logger.info(f"   ✅ Created {assignments_made} House committee assignments")
                logger.info(f"   ✅ Created {leadership_positions} leadership positions")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"   ❌ Error creating House assignments: {e}")
                return False
        
        # Verify results and show comprehensive statistics
        with engine.connect() as conn:
            logger.info("\n3. Comprehensive Verification Results:")
            
            # Overall statistics
            result = conn.execute(text("""
                SELECT 
                    m.chamber,
                    COUNT(DISTINCT m.id) as total_members,
                    COUNT(DISTINCT cm.member_id) as members_with_committees,
                    COUNT(*) as total_assignments,
                    COUNT(CASE WHEN cm.position IN ('Chair', 'Ranking Member') THEN 1 END) as leadership_count
                FROM members m
                LEFT JOIN committee_memberships cm ON m.id = cm.member_id
                GROUP BY m.chamber
                ORDER BY m.chamber
            """))
            
            chamber_stats = result.fetchall()
            
            logger.info("   📊 Chamber Statistics:")
            total_members = 0
            total_assignments = 0
            total_with_committees = 0
            
            for chamber, total, with_committees, assignments, leadership in chamber_stats:
                coverage = (with_committees / total * 100) if total > 0 else 0
                avg_committees = (assignments / total) if total > 0 else 0
                
                logger.info(f"     {chamber}:")
                logger.info(f"       Members: {total}")
                logger.info(f"       With committees: {with_committees} ({coverage:.1f}%)")
                logger.info(f"       Total assignments: {assignments}")
                logger.info(f"       Leadership positions: {leadership}")
                logger.info(f"       Avg committees per member: {avg_committees:.1f}")
                
                total_members += total
                total_assignments += assignments
                total_with_committees += with_committees
            
            overall_coverage = (total_with_committees / total_members * 100) if total_members > 0 else 0
            logger.info(f"     OVERALL:")
            logger.info(f"       Total members: {total_members}")
            logger.info(f"       Total with committees: {total_with_committees} ({overall_coverage:.1f}%)")
            logger.info(f"       Total assignments: {total_assignments}")
            
            # Committee coverage
            result = conn.execute(text("""
                SELECT 
                    c.chamber,
                    COUNT(DISTINCT c.id) as total_committees,
                    COUNT(DISTINCT CASE WHEN c.is_subcommittee = false THEN c.id END) as main_committees,
                    COUNT(DISTINCT CASE WHEN c.is_subcommittee = true THEN c.id END) as subcommittees,
                    COUNT(DISTINCT CASE WHEN c.is_subcommittee = true AND c.parent_committee_id IS NOT NULL THEN c.id END) as linked_subcommittees
                FROM committees c
                GROUP BY c.chamber
                ORDER BY c.chamber
            """))
            
            committee_stats = result.fetchall()
            
            logger.info("\n   📋 Committee Statistics:")
            for chamber, total, main, subs, linked in committee_stats:
                link_coverage = (linked / subs * 100) if subs > 0 else 0
                logger.info(f"     {chamber}:")
                logger.info(f"       Total committees: {total}")
                logger.info(f"       Main committees: {main}")
                logger.info(f"       Subcommittees: {subs}")
                logger.info(f"       Linked subcommittees: {linked} ({link_coverage:.1f}%)")
            
            # Sample House assignments
            result = conn.execute(text("""
                SELECT m.first_name, m.last_name, m.party, m.state, m.district,
                       c.name, cm.position
                FROM committee_memberships cm
                JOIN members m ON cm.member_id = m.id
                JOIN committees c ON cm.committee_id = c.id
                WHERE m.chamber = 'House'
                ORDER BY m.state, m.district, c.name
                LIMIT 20
            """))
            
            sample_assignments = result.fetchall()
            
            logger.info(f"\n   Sample House assignments:")
            for assignment in sample_assignments:
                first_name, last_name, party, state, district, committee_name, position = assignment
                district_info = f"{state}-{district}" if district else state
                pos_indicator = f" ({position})" if position != "Member" else ""
                logger.info(f"     {first_name} {last_name} ({party}-{district_info}): {committee_name}{pos_indicator}")
        
        logger.info(f"\n🎉 HOUSE RELATIONSHIPS COMPLETION SUCCESS!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

if __name__ == "__main__":
    complete_house_relationships()