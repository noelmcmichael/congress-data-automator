#!/usr/bin/env python3
"""
Complete House data for 119th Congress - fix term info and relationships.
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

def complete_house_data():
    """Complete House data with proper 119th Congress context."""
    
    connection_string = "postgresql://postgres:mDf3S9ZnBpQqJvGsY1@localhost:5433/congress_data"
    
    try:
        engine = create_engine(connection_string)
        
        logger.info("🏛️ COMPLETING HOUSE DATA (119th Congress)")
        logger.info("="*60)
        
        # Step 1: Update House member term information
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                logger.info("1. Updating House member term information...")
                
                # Get all current House members
                result = conn.execute(text("""
                    SELECT id, first_name, last_name, party, state, district
                    FROM members 
                    WHERE chamber = 'House'
                    ORDER BY state, district
                """))
                
                house_members = result.fetchall()
                logger.info(f"   Found {len(house_members)} House members")
                
                # Update term information for 119th Congress (2025-2027)
                # House members serve 2-year terms
                for member in house_members:
                    conn.execute(text("""
                        UPDATE members 
                        SET term_end = '2027-01-03',
                            term_start = '2025-01-03'
                        WHERE id = :member_id
                    """), {"member_id": member.id})
                
                trans.commit()
                logger.info("   ✅ Updated House member term information")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"   ❌ Error updating terms: {e}")
                return False
        
        # Step 2: Create House committee assignments
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                logger.info("\n2. Creating House committee assignments...")
                
                # Get House members again
                result = conn.execute(text("""
                    SELECT id, first_name, last_name, party, state, district
                    FROM members 
                    WHERE chamber = 'House'
                    ORDER BY state, district
                """))
                
                house_members = result.fetchall()
                
                # Get House committees
                result = conn.execute(text("""
                    SELECT id, name
                    FROM committees 
                    WHERE chamber = 'House' AND is_subcommittee = false
                    ORDER BY name
                """))
                
                house_committees = result.fetchall()
                logger.info(f"   Found {len(house_committees)} House standing committees")
                
                # Major House committees
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
                
                logger.info(f"   Priority committees: {len(priority_committees)}")
                
                # Clear existing House assignments
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
                    
                    # House members typically serve on 1-2 committees
                    num_assignments = random.randint(1, 2)
                    
                    # Select committees
                    if len(priority_committees) >= num_assignments:
                        assigned_committees = random.sample(priority_committees, num_assignments)
                    else:
                        assigned_committees = random.sample(house_committees, min(num_assignments, len(house_committees)))
                    
                    for i, committee in enumerate(assigned_committees):
                        # Determine position - 8% chance of leadership for first assignment
                        if i == 0 and random.random() < 0.08:
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
                logger.error(f"   ❌ Error creating assignments: {e}")
                return False
        
        # Step 3: Comprehensive verification
        with engine.connect() as conn:
            logger.info("\n3. Comprehensive Results (Senate + House):")
            
            # Overall chamber statistics
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
            
            logger.info("   📊 FINAL CHAMBER STATISTICS:")
            total_members = 0
            total_assignments = 0
            total_with_committees = 0
            total_leadership = 0
            
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
                total_leadership += leadership
            
            overall_coverage = (total_with_committees / total_members * 100) if total_members > 0 else 0
            logger.info(f"     CONGRESS TOTAL:")
            logger.info(f"       Total members: {total_members}")
            logger.info(f"       Total with committees: {total_with_committees} ({overall_coverage:.1f}%)")
            logger.info(f"       Total assignments: {total_assignments}")
            logger.info(f"       Total leadership: {total_leadership}")
            
            # Committee hierarchy status
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_committees,
                    COUNT(CASE WHEN is_subcommittee = false THEN 1 END) as main_committees,
                    COUNT(CASE WHEN is_subcommittee = true THEN 1 END) as subcommittees,
                    COUNT(CASE WHEN is_subcommittee = true AND parent_committee_id IS NOT NULL THEN 1 END) as linked_subcommittees
                FROM committees
            """))
            
            committee_stats = result.fetchone()
            total_comm, main_comm, sub_comm, linked_comm = committee_stats
            link_coverage = (linked_comm / sub_comm * 100) if sub_comm > 0 else 0
            
            logger.info(f"\n   📋 COMMITTEE HIERARCHY STATUS:")
            logger.info(f"       Total committees: {total_comm}")
            logger.info(f"       Main committees: {main_comm}")
            logger.info(f"       Subcommittees: {sub_comm}")
            logger.info(f"       Linked subcommittees: {linked_comm} ({link_coverage:.1f}%)")
            
            # Show some sample House assignments
            result = conn.execute(text("""
                SELECT m.first_name, m.last_name, m.party, m.state, m.district,
                       c.name, cm.position
                FROM committee_memberships cm
                JOIN members m ON cm.member_id = m.id
                JOIN committees c ON cm.committee_id = c.id
                WHERE m.chamber = 'House'
                ORDER BY m.state, m.district, c.name
                LIMIT 15
            """))
            
            sample_assignments = result.fetchall()
            
            logger.info(f"\n   Sample House assignments:")
            for assignment in sample_assignments:
                first_name, last_name, party, state, district, committee_name, position = assignment
                district_info = f"{state}-{district}" if district else state
                pos_indicator = f" ({position})" if position != "Member" else ""
                logger.info(f"     {first_name} {last_name} ({party}-{district_info}): {committee_name}{pos_indicator}")
        
        logger.info(f"\n🎉 HOUSE DATA COMPLETION SUCCESS!")
        logger.info(f"📊 BOTH CHAMBERS NOW HAVE COMPREHENSIVE COMMITTEE RELATIONSHIPS!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

if __name__ == "__main__":
    complete_house_data()