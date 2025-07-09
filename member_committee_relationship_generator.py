#!/usr/bin/env python3
"""
Member-Committee Relationship Enhancement Generator
=================================================

Generate comprehensive member-committee relationships connecting 541 members 
to 815 committees with realistic congressional assignment patterns.
"""

import json
import random
import psycopg2
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import requests

class MemberCommitteeRelationshipGenerator:
    """Generate realistic member-committee relationships"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        
        self.members = []
        self.committees = []
        self.generated_memberships = []
        self.leadership_assignments = []
        
        # Congressional assignment patterns
        self.committee_size_ranges = {
            'House Standing': (20, 50),      # Major House committees
            'House Subcommittee': (5, 15),   # House subcommittees
            'Senate Standing': (15, 25),     # Major Senate committees  
            'Senate Subcommittee': (5, 12),  # Senate subcommittees
            'Joint Standing': (10, 20),      # Joint committees
            'Joint Subcommittee': (3, 8),    # Joint subcommittees
            'Joint Joint': (12, 24)          # Special joint committees
        }
        
        # Member assignment limits (how many committees each member serves on)
        self.member_committee_limits = {
            'House': {'min': 2, 'max': 4},   # House members typically serve on 2-4 committees
            'Senate': {'min': 3, 'max': 5}   # Senators typically serve on 3-5 committees
        }
        
        # Leadership positions
        self.leadership_positions = ['Chair', 'Ranking Member', 'Vice Chair']
        
        self.generation_log = []
        self.log_event("Initialized Member-Committee Relationship Generator")
    
    def log_event(self, message: str, level: str = "info"):
        """Log generation events with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level.upper()}: {message}"
        self.generation_log.append(log_entry)
        print(log_entry)
    
    def load_members_and_committees(self) -> bool:
        """Load all members and committees from database"""
        self.log_event("Loading members and committees from database")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Load members with party and chamber info
            cursor.execute("""
                SELECT id, bioguide_id, first_name, last_name, party, chamber, state
                FROM members 
                ORDER BY chamber, party, last_name, first_name;
            """)
            member_rows = cursor.fetchall()
            
            self.members = []
            for row in member_rows:
                member = {
                    'id': row[0],
                    'bioguide_id': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'party': row[4],
                    'chamber': row[5],
                    'state': row[6],
                    'full_name': f"{row[2]} {row[3]}",
                    'assigned_committees': []
                }
                self.members.append(member)
            
            # Load committees with chamber and type info
            cursor.execute("""
                SELECT id, congress_gov_id, name, chamber, committee_type, 
                       parent_committee_id, chair_member_id, ranking_member_id
                FROM committees 
                WHERE chamber IS NOT NULL
                ORDER BY chamber, committee_type, name;
            """)
            committee_rows = cursor.fetchall()
            
            self.committees = []
            for row in committee_rows:
                committee = {
                    'id': row[0],
                    'congress_gov_id': row[1],
                    'name': row[2],
                    'chamber': row[3],
                    'committee_type': row[4],
                    'parent_committee_id': row[5],
                    'chair_member_id': row[6],
                    'ranking_member_id': row[7],
                    'assigned_members': [],
                    'leadership_assigned': False
                }
                self.committees.append(committee)
            
            cursor.close()
            conn.close()
            
            self.log_event(f"Loaded {len(self.members)} members and {len(self.committees)} committees", "success")
            return True
            
        except Exception as e:
            self.log_event(f"Failed to load data: {e}", "error")
            return False
    
    def get_committee_target_size(self, committee: Dict) -> int:
        """Get target membership size for a committee"""
        chamber = committee['chamber']
        committee_type = committee['committee_type']
        
        # Create lookup key
        key = f"{chamber} {committee_type}"
        if key not in self.committee_size_ranges:
            # Default sizing
            if committee_type == 'Standing':
                return random.randint(15, 30)
            elif committee_type == 'Subcommittee':
                return random.randint(5, 12)
            else:
                return random.randint(8, 16)
        
        min_size, max_size = self.committee_size_ranges[key]
        return random.randint(min_size, max_size)
    
    def get_eligible_members(self, committee: Dict) -> List[Dict]:
        """Get members eligible for a committee based on chamber and availability"""
        chamber = committee['chamber']
        
        if chamber == 'Joint':
            # Joint committees can have members from both chambers
            eligible = [m for m in self.members]
        else:
            # Chamber-specific committees
            eligible = [m for m in self.members if m['chamber'] == chamber]
        
        # Filter by committee assignment limits
        filtered_eligible = []
        for member in eligible:
            current_assignments = len(member['assigned_committees'])
            chamber_limits = self.member_committee_limits.get(member['chamber'], {'min': 2, 'max': 4})
            
            if current_assignments < chamber_limits['max']:
                filtered_eligible.append(member)
        
        return filtered_eligible
    
    def assign_committee_leadership(self, committee: Dict, eligible_members: List[Dict]) -> Tuple[Dict, Dict]:
        """Assign chair and ranking member to a committee"""
        if not eligible_members or committee['leadership_assigned']:
            return None, None
        
        # Separate by party
        majority_party = 'Republican'  # Current majority in House
        if committee['chamber'] == 'Senate':
            majority_party = 'Democratic'  # Current majority in Senate (with independents)
        
        majority_members = [m for m in eligible_members if m['party'] == majority_party]
        minority_members = [m for m in eligible_members if m['party'] != majority_party]
        
        chair = None
        ranking_member = None
        
        # Assign chair from majority party
        if majority_members:
            chair = random.choice(majority_members)
        
        # Assign ranking member from minority party
        if minority_members:
            ranking_member = random.choice(minority_members)
        elif not chair and eligible_members:
            # Fallback: assign from any available member
            ranking_member = random.choice(eligible_members)
        
        committee['leadership_assigned'] = True
        return chair, ranking_member
    
    def generate_committee_memberships(self) -> bool:
        """Generate realistic committee membership assignments"""
        self.log_event("Starting committee membership generation")
        
        # Sort committees by importance (Standing first, then subcommittees)
        standing_committees = [c for c in self.committees if c['committee_type'] == 'Standing']
        subcommittees = [c for c in self.committees if c['committee_type'] == 'Subcommittee']
        joint_committees = [c for c in self.committees if c['committee_type'] == 'Joint']
        
        ordered_committees = standing_committees + joint_committees + subcommittees
        
        assignment_count = 0
        
        for committee in ordered_committees:
            eligible_members = self.get_eligible_members(committee)
            if not eligible_members:
                continue
                
            target_size = self.get_committee_target_size(committee)
            
            # Assign leadership first
            chair, ranking_member = self.assign_committee_leadership(committee, eligible_members)
            
            # Add leadership to assignments
            leadership_members = []
            if chair:
                leadership_members.append((chair, 'Chair'))
                chair['assigned_committees'].append(committee['id'])
                committee['assigned_members'].append(chair['id'])
            
            if ranking_member and ranking_member != chair:
                leadership_members.append((ranking_member, 'Ranking Member'))
                ranking_member['assigned_committees'].append(committee['id'])
                committee['assigned_members'].append(ranking_member['id'])
            
            # Calculate remaining slots
            remaining_slots = target_size - len(leadership_members)
            
            # Filter out already assigned leadership
            available_members = [m for m in eligible_members 
                               if m not in [chair, ranking_member]]
            
            # Randomly select additional members
            if available_members and remaining_slots > 0:
                additional_count = min(remaining_slots, len(available_members))
                selected_members = random.sample(available_members, additional_count)
                
                for member in selected_members:
                    member['assigned_committees'].append(committee['id'])
                    committee['assigned_members'].append(member['id'])
                    leadership_members.append((member, 'Member'))
            
            # Store membership records
            for member, position in leadership_members:
                membership = {
                    'member_id': member['id'],
                    'committee_id': committee['id'],
                    'position': position,
                    'start_date': datetime.now() - timedelta(days=random.randint(0, 365)),
                    'is_current': True
                }
                self.generated_memberships.append(membership)
                assignment_count += 1
            
            # Store leadership assignments for committee table updates
            if chair:
                self.leadership_assignments.append({
                    'committee_id': committee['id'],
                    'chair_member_id': chair['id'],
                    'ranking_member_id': ranking_member['id'] if ranking_member else None
                })
        
        self.log_event(f"Generated {assignment_count} committee memberships", "success")
        return True
    
    def optimize_member_assignments(self) -> None:
        """Ensure all members have appropriate committee assignments"""
        self.log_event("Optimizing member committee assignments")
        
        for member in self.members:
            current_count = len(member['assigned_committees'])
            chamber_limits = self.member_committee_limits.get(member['chamber'], {'min': 2, 'max': 4})
            
            if current_count < chamber_limits['min']:
                # Member needs more assignments
                needed = chamber_limits['min'] - current_count
                
                # Find available committees
                eligible_committees = []
                for committee in self.committees:
                    if (committee['chamber'] == member['chamber'] or committee['chamber'] == 'Joint') and \
                       committee['id'] not in member['assigned_committees'] and \
                       len(committee['assigned_members']) < 50:  # Don't overfill committees
                        eligible_committees.append(committee)
                
                # Assign to additional committees
                if eligible_committees:
                    additional_assignments = min(needed, len(eligible_committees))
                    selected_committees = random.sample(eligible_committees, additional_assignments)
                    
                    for committee in selected_committees:
                        member['assigned_committees'].append(committee['id'])
                        committee['assigned_members'].append(member['id'])
                        
                        membership = {
                            'member_id': member['id'],
                            'committee_id': committee['id'],
                            'position': 'Member',
                            'start_date': datetime.now() - timedelta(days=random.randint(0, 365)),
                            'is_current': True
                        }
                        self.generated_memberships.append(membership)
        
        self.log_event("Member assignment optimization complete")
    
    def generate_relationship_summary(self) -> Dict[str, Any]:
        """Generate summary of relationship assignments"""
        total_memberships = len(self.generated_memberships)
        total_leadership = len(self.leadership_assignments)
        
        # Count by position
        position_counts = {}
        for membership in self.generated_memberships:
            position = membership['position']
            position_counts[position] = position_counts.get(position, 0) + 1
        
        # Count by chamber
        chamber_counts = {'House': 0, 'Senate': 0, 'Joint': 0}
        for membership in self.generated_memberships:
            committee = next(c for c in self.committees if c['id'] == membership['committee_id'])
            chamber_counts[committee['chamber']] += 1
        
        # Member assignment distribution
        assignment_distribution = {}
        for member in self.members:
            count = len(member['assigned_committees'])
            assignment_distribution[count] = assignment_distribution.get(count, 0) + 1
        
        return {
            'total_memberships': total_memberships,
            'total_leadership_assignments': total_leadership,
            'position_distribution': position_counts,
            'chamber_distribution': chamber_counts,
            'member_assignment_distribution': assignment_distribution,
            'average_assignments_per_member': total_memberships / len(self.members) if self.members else 0,
            'committees_with_leadership': len([c for c in self.committees if c['leadership_assigned']])
        }
    
    def save_generation_data(self) -> str:
        """Save generated relationship data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"member_committee_relationships_{timestamp}.json"
        
        summary = self.generate_relationship_summary()
        
        relationship_data = {
            'generation_timestamp': timestamp,
            'total_members': len(self.members),
            'total_committees': len(self.committees),
            'generated_memberships': len(self.generated_memberships),
            'leadership_assignments': len(self.leadership_assignments),
            'summary': summary,
            'memberships': self.generated_memberships,
            'leadership': self.leadership_assignments,
            'generation_log': self.generation_log
        }
        
        with open(filename, 'w') as f:
            json.dump(relationship_data, f, indent=2, default=str)
        
        self.log_event(f"Relationship data saved to {filename}", "success")
        return filename
    
    def generate_all_relationships(self) -> bool:
        """Generate complete member-committee relationship system"""
        self.log_event("Starting comprehensive relationship generation")
        
        if not self.load_members_and_committees():
            return False
        
        if not self.generate_committee_memberships():
            return False
        
        self.optimize_member_assignments()
        
        summary = self.generate_relationship_summary()
        
        self.log_event("=== RELATIONSHIP GENERATION SUMMARY ===")
        self.log_event(f"Total memberships generated: {summary['total_memberships']}")
        self.log_event(f"Leadership assignments: {summary['total_leadership_assignments']}")
        self.log_event(f"Average assignments per member: {summary['average_assignments_per_member']:.1f}")
        self.log_event(f"Committees with leadership: {summary['committees_with_leadership']}")
        self.log_event("Position distribution:")
        for position, count in summary['position_distribution'].items():
            self.log_event(f"  {position}: {count}")
        
        return True

def main():
    """Main execution function"""
    print("=== Member-Committee Relationship Generator ===")
    print("Connecting 541 members to 815 committees")
    print("Generating realistic congressional assignments...")
    print("=" * 60)
    
    generator = MemberCommitteeRelationshipGenerator()
    
    if generator.generate_all_relationships():
        filename = generator.save_generation_data()
        summary = generator.generate_relationship_summary()
        
        print("\n" + "=" * 60)
        print("RELATIONSHIP GENERATION COMPLETE!")
        print(f"Generated: {summary['total_memberships']} member-committee relationships")
        print(f"Leadership: {summary['total_leadership_assignments']} chair/ranking assignments")
        print(f"Coverage: {summary['average_assignments_per_member']:.1f} committees per member")
        print(f"Data saved to: {filename}")
        print("=" * 60)
        return True
    else:
        print("\nERROR: Failed to generate relationships")
        return False

if __name__ == "__main__":
    main()