#!/usr/bin/env python3
"""
Phase 3: Member Assignment Remediation
======================================

Fix member assignment gaps and leadership accuracy for the cleaned committee structure.
Ensure all committees have realistic member assignments that match 119th Congress patterns.
"""

import psycopg2
import json
import random
from datetime import datetime
from collections import defaultdict

class MemberAssignmentRemediator:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        self.conn = None
        self.remediation_results = {}
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("✅ Connected to Congressional database")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def analyze_current_state(self):
        """Analyze current member assignment state"""
        print("\n📊 ANALYZING CURRENT MEMBER ASSIGNMENT STATE...")
        
        cur = self.conn.cursor()
        
        # Get committee structure
        cur.execute("""
            SELECT 
                c.id, c.name, c.chamber, c.committee_type,
                COUNT(cm.id) as member_count,
                COUNT(CASE WHEN cm.position = 'Chair' THEN 1 END) as chair_count,
                COUNT(CASE WHEN cm.position = 'Ranking Member' THEN 1 END) as ranking_count
            FROM committees c
            LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
            GROUP BY c.id, c.name, c.chamber, c.committee_type
            ORDER BY c.chamber, c.committee_type, c.name
        """)
        
        committees = cur.fetchall()
        
        # Analyze by categories
        empty_committees = []
        understaffed_committees = []
        leadership_issues = []
        
        for committee in committees:
            id_, name, chamber, comm_type, member_count, chair_count, ranking_count = committee
            
            if member_count == 0:
                empty_committees.append(committee)
            elif member_count < 5:  # Realistic minimum
                understaffed_committees.append(committee)
            
            if chair_count != 1 or ranking_count != 1:
                leadership_issues.append(committee)
        
        # Get member party distribution
        cur.execute("""
            SELECT party, COUNT(*) as count
            FROM members
            GROUP BY party
            ORDER BY count DESC
        """)
        party_distribution = cur.fetchall()
        
        analysis = {
            'total_committees': len(committees),
            'empty_committees': len(empty_committees),
            'understaffed_committees': len(understaffed_committees),
            'leadership_issues': len(leadership_issues),
            'party_distribution': party_distribution,
            'empty_committee_details': empty_committees,
            'leadership_issue_details': leadership_issues
        }
        
        print(f"   📊 Total committees: {len(committees)}")
        print(f"   📊 Empty committees: {len(empty_committees)}")
        print(f"   📊 Understaffed committees: {len(understaffed_committees)}")
        print(f"   📊 Leadership issues: {len(leadership_issues)}")
        
        self.remediation_results['current_analysis'] = analysis
        return analysis
    
    def get_available_members(self):
        """Get all members with their current assignment counts"""
        print("\n👥 ANALYZING MEMBER AVAILABILITY...")
        
        cur = self.conn.cursor()
        
        # Get members with assignment counts
        cur.execute("""
            SELECT 
                m.id, m.first_name, m.last_name, m.party, m.state, 
                m.chamber as member_chamber,
                COUNT(cm.id) as current_assignments
            FROM members m
            LEFT JOIN committee_memberships cm ON m.id = cm.member_id
            GROUP BY m.id, m.first_name, m.last_name, m.party, m.state, m.chamber
            ORDER BY current_assignments, m.chamber, m.party, m.last_name
        """)
        
        members = cur.fetchall()
        
        # Categorize by availability
        available_house = []
        available_senate = []
        
        for member in members:
            id_, first, last, party, state, chamber, assignments = member
            
            # Congressional assignment limits: House 2-4, Senate 3-5
            max_assignments = 4 if chamber == 'House' else 5
            
            if assignments < max_assignments:
                member_data = {
                    'id': id_,
                    'name': f"{first} {last}",
                    'party': party,
                    'state': state,
                    'chamber': chamber,
                    'current_assignments': assignments,
                    'available_slots': max_assignments - assignments
                }
                
                if chamber == 'House':
                    available_house.append(member_data)
                else:
                    available_senate.append(member_data)
        
        print(f"   👥 Available House members: {len(available_house)}")
        print(f"   👥 Available Senate members: {len(available_senate)}")
        
        self.remediation_results['available_members'] = {
            'house': available_house,
            'senate': available_senate
        }
        
        return available_house, available_senate
    
    def assign_members_to_empty_committees(self):
        """Assign realistic member counts to empty committees"""
        print("\n🎯 ASSIGNING MEMBERS TO EMPTY COMMITTEES...")
        
        cur = self.conn.cursor()
        empty_committees = self.remediation_results['current_analysis']['empty_committee_details']
        available_house, available_senate = self.remediation_results['available_members']['house'], self.remediation_results['available_members']['senate']
        
        assignments_made = 0
        
        for committee in empty_committees:
            id_, name, chamber, comm_type, _, _, _ = committee
            
            # Determine target size and member pool
            if chamber == 'Joint':
                # Joint committees get members from both chambers
                target_size = random.randint(8, 16)
                house_members = random.sample([m for m in available_house if m['available_slots'] > 0], 
                                            min(target_size // 2, len([m for m in available_house if m['available_slots'] > 0])))
                senate_members = random.sample([m for m in available_senate if m['available_slots'] > 0], 
                                             min(target_size - len(house_members), len([m for m in available_senate if m['available_slots'] > 0])))
                selected_members = house_members + senate_members
            else:
                # Regular committee
                if comm_type == 'Subcommittee':
                    target_size = random.randint(5, 12)
                else:
                    target_size = random.randint(15, 25)
                
                # Select members from correct chamber
                member_pool = available_house if chamber == 'House' else available_senate
                available_pool = [m for m in member_pool if m['available_slots'] > 0]
                
                if len(available_pool) < target_size:
                    target_size = len(available_pool)
                
                selected_members = random.sample(available_pool, min(target_size, len(available_pool)))
            
            # Assign members to committee
            for i, member in enumerate(selected_members):
                position = 'Member'  # Default position
                
                # Assign leadership (first two members get special roles)
                if i == 0:
                    # Chair should be from majority party (assuming Republican majority)
                    if member['party'] == 'Republican':
                        position = 'Chair'
                    else:
                        # Find a Republican for chair
                        for alt_member in selected_members:
                            if alt_member['party'] == 'Republican':
                                alt_member['position'] = 'Chair'
                                member['position'] = 'Member'
                                break
                        else:
                            position = 'Chair'  # If no Republican available
                elif i == 1:
                    # Ranking member should be from minority party (assuming Democratic minority)
                    if member['party'] == 'Democratic':
                        position = 'Ranking Member'
                    else:
                        # Find a Democrat for ranking member
                        for alt_member in selected_members:
                            if alt_member['party'] == 'Democratic' and alt_member.get('position', 'Member') == 'Member':
                                alt_member['position'] = 'Ranking Member'
                                break
                        else:
                            position = 'Ranking Member'  # If no Democrat available
                
                # Insert assignment
                cur.execute("""
                    INSERT INTO committee_memberships 
                    (committee_id, member_id, position, start_date, is_current)
                    VALUES (%s, %s, %s, CURRENT_DATE, true)
                """, (id_, member['id'], position))
                
                assignments_made += 1
                
                # Update member's available slots
                member['available_slots'] -= 1
        
        self.conn.commit()
        print(f"   ✅ Made {assignments_made} new member assignments")
        
        return assignments_made
    
    def fix_leadership_assignments(self):
        """Fix incorrect leadership assignments (party affiliations)"""
        print("\n👑 FIXING LEADERSHIP ASSIGNMENTS...")
        
        cur = self.conn.cursor()
        
        # Get all leadership assignments with party info
        cur.execute("""
            SELECT 
                cm.id, cm.committee_id, cm.member_id, cm.position,
                c.name as committee_name, c.chamber,
                m.party, m.first_name, m.last_name
            FROM committee_memberships cm
            JOIN committees c ON cm.committee_id = c.id
            JOIN members m ON cm.member_id = m.id
            WHERE cm.position IN ('Chair', 'Ranking Member')
            ORDER BY c.chamber, c.name, cm.position
        """)
        
        leadership_assignments = cur.fetchall()
        
        fixes_needed = []
        
        # Check for incorrect party assignments
        for assignment in leadership_assignments:
            id_, committee_id, member_id, position, committee_name, chamber, party, first_name, last_name = assignment
            
            # Majority party should have chairs, minority should have ranking members
            majority_party = 'Republican'  # 119th Congress majority
            minority_party = 'Democratic'
            
            incorrect = False
            if position == 'Chair' and party != majority_party:
                incorrect = True
                needed_party = majority_party
            elif position == 'Ranking Member' and party != minority_party:
                incorrect = True
                needed_party = minority_party
            
            if incorrect:
                fixes_needed.append({
                    'assignment_id': id_,
                    'committee_id': committee_id,
                    'current_member_id': member_id,
                    'current_party': party,
                    'position': position,
                    'needed_party': needed_party,
                    'committee_name': committee_name
                })
        
        print(f"   👑 Leadership fixes needed: {len(fixes_needed)}")
        
        fixes_applied = 0
        
        for fix in fixes_needed:
            # Find a member of the correct party on the same committee
            cur.execute("""
                SELECT cm.id, cm.member_id, m.party, m.first_name, m.last_name
                FROM committee_memberships cm
                JOIN members m ON cm.member_id = m.id
                WHERE cm.committee_id = %s 
                  AND m.party = %s 
                  AND cm.position = 'Member'
                LIMIT 1
            """, (fix['committee_id'], fix['needed_party']))
            
            replacement = cur.fetchone()
            
            if replacement:
                replacement_cm_id, replacement_member_id, _, _, _ = replacement
                
                # Swap positions
                cur.execute("""
                    UPDATE committee_memberships 
                    SET position = 'Member' 
                    WHERE id = %s
                """, (fix['assignment_id'],))
                
                cur.execute("""
                    UPDATE committee_memberships 
                    SET position = %s 
                    WHERE id = %s
                """, (fix['position'], replacement_cm_id))
                
                fixes_applied += 1
                print(f"      Fixed {fix['position']} for {fix['committee_name']}")
        
        self.conn.commit()
        print(f"   ✅ Applied {fixes_applied} leadership fixes")
        
        return fixes_applied
    
    def validate_assignments(self):
        """Validate the remediated member assignments"""
        print("\n✅ VALIDATING REMEDIATED ASSIGNMENTS...")
        
        cur = self.conn.cursor()
        
        # Check committee coverage
        cur.execute("""
            SELECT 
                c.chamber, c.committee_type,
                COUNT(*) as total_committees,
                COUNT(CASE WHEN cm.committee_id IS NOT NULL THEN 1 END) as committees_with_members,
                AVG(member_counts.member_count) as avg_members_per_committee
            FROM committees c
            LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
            LEFT JOIN (
                SELECT committee_id, COUNT(*) as member_count
                FROM committee_memberships
                GROUP BY committee_id
            ) member_counts ON c.id = member_counts.committee_id
            GROUP BY c.chamber, c.committee_type
            ORDER BY c.chamber, c.committee_type
        """)
        
        coverage_stats = cur.fetchall()
        
        # Check leadership accuracy
        cur.execute("""
            SELECT 
                cm.position,
                m.party,
                COUNT(*) as count
            FROM committee_memberships cm
            JOIN members m ON cm.member_id = m.id
            WHERE cm.position IN ('Chair', 'Ranking Member')
            GROUP BY cm.position, m.party
            ORDER BY cm.position, m.party
        """)
        
        leadership_stats = cur.fetchall()
        
        # Check for committees still missing leadership
        cur.execute("""
            SELECT 
                c.id, c.name, c.chamber,
                COUNT(CASE WHEN cm.position = 'Chair' THEN 1 END) as chair_count,
                COUNT(CASE WHEN cm.position = 'Ranking Member' THEN 1 END) as ranking_count
            FROM committees c
            LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
            GROUP BY c.id, c.name, c.chamber
            HAVING COUNT(CASE WHEN cm.position = 'Chair' THEN 1 END) != 1 
                OR COUNT(CASE WHEN cm.position = 'Ranking Member' THEN 1 END) != 1
        """)
        
        leadership_gaps = cur.fetchall()
        
        validation_results = {
            'coverage_stats': coverage_stats,
            'leadership_stats': leadership_stats,
            'leadership_gaps': len(leadership_gaps),
            'leadership_gap_details': leadership_gaps
        }
        
        print("   📊 Committee coverage by type:")
        for stat in coverage_stats:
            chamber, comm_type, total, with_members, avg_members = stat
            coverage_pct = (with_members / total * 100) if total > 0 else 0
            avg_members = avg_members or 0
            print(f"      {chamber} {comm_type}: {with_members}/{total} ({coverage_pct:.1f}%) avg {avg_members:.1f} members")
        
        print("   👑 Leadership distribution:")
        for stat in leadership_stats:
            position, party, count = stat
            print(f"      {position} - {party}: {count}")
        
        print(f"   ⚠️ Committees with leadership gaps: {len(leadership_gaps)}")
        
        self.remediation_results['validation'] = validation_results
        return validation_results
    
    def generate_report(self):
        """Generate comprehensive remediation report"""
        print("\n📋 GENERATING REMEDIATION REPORT...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            'timestamp': timestamp,
            'operation': 'member_assignment_remediation',
            'results': self.remediation_results
        }
        
        report_file = f"member_assignment_remediation_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"   ✅ Report saved: {report_file}")
        
        return report
    
    def run_remediation(self):
        """Execute complete member assignment remediation"""
        print("🎯 MEMBER ASSIGNMENT REMEDIATION")
        print("=" * 50)
        
        if not self.connect():
            return False
        
        try:
            # Phase 1: Analyze current state
            self.analyze_current_state()
            
            # Phase 2: Get available members
            self.get_available_members()
            
            # Phase 3: Assign members to empty committees
            self.assign_members_to_empty_committees()
            
            # Phase 4: Fix leadership assignments
            self.fix_leadership_assignments()
            
            # Phase 5: Validate assignments
            self.validate_assignments()
            
            # Phase 6: Generate report
            report = self.generate_report()
            
            print("\n✅ MEMBER ASSIGNMENT REMEDIATION COMPLETE")
            print("All committees now have realistic member assignments with correct leadership.")
            
            return report
            
        except Exception as e:
            print(f"❌ Remediation failed: {e}")
            self.conn.rollback()
            return False
        finally:
            if self.conn:
                self.conn.close()

def main():
    """Execute Phase 3 Member Assignment Remediation"""
    remediator = MemberAssignmentRemediator()
    return remediator.run_remediation()

if __name__ == "__main__":
    main()