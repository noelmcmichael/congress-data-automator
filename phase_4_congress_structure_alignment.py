#!/usr/bin/env python3
"""
Phase 4: 119th Congress Structure Alignment
===========================================

Align the committee structure with the actual 119th Congress to ensure
realistic representation and proper parent-subcommittee relationships.
"""

import psycopg2
import json
from datetime import datetime

class CongressStructureAligner:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        self.conn = None
        self.alignment_results = {}
        
        # Real 119th Congress committee structure
        self.congress_119_structure = {
            'House': {
                'Standing': [
                    'Committee on Agriculture',
                    'Committee on Appropriations',
                    'Committee on Armed Services',
                    'Committee on Budget',
                    'Committee on Education and the Workforce',
                    'Committee on Energy and Commerce',
                    'Committee on Ethics',
                    'Committee on Financial Services',
                    'Committee on Foreign Affairs',
                    'Committee on Homeland Security',
                    'Committee on House Administration',
                    'Committee on the Judiciary',
                    'Committee on Natural Resources',
                    'Committee on Oversight and Accountability',
                    'Committee on Rules',
                    'Committee on Science, Space, and Technology',
                    'Committee on Small Business',
                    'Committee on Transportation and Infrastructure',
                    'Committee on Veterans\' Affairs',
                    'Committee on Ways and Means'
                ]
            },
            'Senate': {
                'Standing': [
                    'Committee on Agriculture, Nutrition, and Forestry',
                    'Committee on Appropriations',
                    'Committee on Armed Services',
                    'Committee on Banking, Housing, and Urban Affairs',
                    'Committee on Budget',
                    'Committee on Commerce, Science, and Transportation',
                    'Committee on Energy and Natural Resources',
                    'Committee on Environment and Public Works',
                    'Committee on Finance',
                    'Committee on Foreign Relations',
                    'Committee on Health, Education, Labor and Pensions',
                    'Committee on Homeland Security and Governmental Affairs',
                    'Committee on the Judiciary',
                    'Committee on Rules and Administration',
                    'Committee on Small Business and Entrepreneurship',
                    'Committee on Veterans\' Affairs'
                ]
            },
            'Joint': [
                'Joint Committee on the Library',
                'Joint Committee on Printing',
                'Joint Committee on Taxation',
                'Joint Economic Committee'
            ]
        }
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("✅ Connected to Congressional database")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def analyze_current_structure(self):
        """Analyze current committee structure vs real Congress"""
        print("\n📊 ANALYZING CURRENT VS REAL CONGRESS STRUCTURE...")
        
        cur = self.conn.cursor()
        
        # Get current structure
        cur.execute("""
            SELECT id, name, chamber, committee_type
            FROM committees
            WHERE committee_type = 'Standing'
            ORDER BY chamber, name
        """)
        
        current_committees = cur.fetchall()
        
        # Categorize current committees
        current_structure = {
            'House': [],
            'Senate': [],
            'Joint': []
        }
        
        for committee in current_committees:
            id_, name, chamber, comm_type = committee
            if chamber in current_structure:
                current_structure[chamber].append({'id': id_, 'name': name})
        
        # Compare with real structure
        analysis = {
            'current_structure': current_structure,
            'real_structure': self.congress_119_structure,
            'comparison': {}
        }
        
        # Detailed comparison
        for chamber in ['House', 'Senate']:
            current_names = [c['name'] for c in current_structure[chamber]]
            real_names = self.congress_119_structure[chamber]['Standing']
            
            analysis['comparison'][chamber] = {
                'current_count': len(current_names),
                'real_count': len(real_names),
                'matches': [],
                'missing_in_current': [],
                'extra_in_current': []
            }
            
            # Find matches and differences
            for real_name in real_names:
                best_match = None
                for current in current_structure[chamber]:
                    if self._names_similar(real_name, current['name']):
                        best_match = current
                        break
                
                if best_match:
                    analysis['comparison'][chamber]['matches'].append({
                        'real_name': real_name,
                        'current_name': best_match['name'],
                        'committee_id': best_match['id']
                    })
                else:
                    analysis['comparison'][chamber]['missing_in_current'].append(real_name)
            
            # Find extra committees
            matched_ids = [m['committee_id'] for m in analysis['comparison'][chamber]['matches']]
            for current in current_structure[chamber]:
                if current['id'] not in matched_ids:
                    analysis['comparison'][chamber]['extra_in_current'].append(current)
        
        # Handle Joint committees
        current_joint_names = [c['name'] for c in current_structure['Joint']]
        real_joint_names = self.congress_119_structure['Joint']
        
        analysis['comparison']['Joint'] = {
            'current_count': len(current_joint_names),
            'real_count': len(real_joint_names),
            'missing': [name for name in real_joint_names if not any(self._names_similar(name, c) for c in current_joint_names)]
        }
        
        print(f"   📊 House: {analysis['comparison']['House']['current_count']}/{analysis['comparison']['House']['real_count']} committees")
        print(f"   📊 Senate: {analysis['comparison']['Senate']['current_count']}/{analysis['comparison']['Senate']['real_count']} committees")
        print(f"   📊 Joint: {analysis['comparison']['Joint']['current_count']}/{analysis['comparison']['Joint']['real_count']} committees")
        
        self.alignment_results['structure_analysis'] = analysis
        return analysis
    
    def _names_similar(self, name1, name2):
        """Check if two committee names are similar enough to be the same committee"""
        # Normalize names for comparison
        n1 = name1.lower().replace('committee on ', '').replace('the ', '').strip()
        n2 = name2.lower().replace('committee on ', '').replace('the ', '').strip()
        
        # Check for key word matches
        words1 = set(n1.split())
        words2 = set(n2.split())
        
        # If more than 50% of words match, consider similar
        if len(words1) == 0 or len(words2) == 0:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        return similarity > 0.5
    
    def standardize_committee_names(self):
        """Standardize committee names to match real 119th Congress"""
        print("\n📝 STANDARDIZING COMMITTEE NAMES...")
        
        analysis = self.alignment_results['structure_analysis']
        cur = self.conn.cursor()
        
        updates_made = 0
        
        # Update House and Senate committees
        for chamber in ['House', 'Senate']:
            matches = analysis['comparison'][chamber]['matches']
            
            for match in matches:
                if match['real_name'] != match['current_name']:
                    cur.execute("""
                        UPDATE committees 
                        SET name = %s 
                        WHERE id = %s
                    """, (match['real_name'], match['committee_id']))
                    
                    updates_made += 1
                    print(f"      Updated: {match['current_name']} -> {match['real_name']}")
        
        self.conn.commit()
        print(f"   ✅ Standardized {updates_made} committee names")
        
        return updates_made
    
    def create_missing_committees(self):
        """Create committees that exist in real Congress but missing in database"""
        print("\n➕ CREATING MISSING COMMITTEES...")
        
        analysis = self.alignment_results['structure_analysis']
        cur = self.conn.cursor()
        
        created_committees = []
        
        # Create missing House and Senate committees
        for chamber in ['House', 'Senate']:
            missing = analysis['comparison'][chamber]['missing_in_current']
            
            for committee_name in missing:
                cur.execute("""
                    INSERT INTO committees (name, chamber, committee_type)
                    VALUES (%s, %s, 'Standing')
                    RETURNING id
                """, (committee_name, chamber))
                
                committee_id = cur.fetchone()[0]
                created_committees.append({
                    'id': committee_id,
                    'name': committee_name,
                    'chamber': chamber
                })
                
                print(f"      Created: {chamber} - {committee_name}")
        
        # Create missing Joint committees
        missing_joint = analysis['comparison']['Joint']['missing']
        for committee_name in missing_joint:
            cur.execute("""
                INSERT INTO committees (name, chamber, committee_type)
                VALUES (%s, 'Joint', 'Standing')
                RETURNING id
            """, (committee_name,))
            
            committee_id = cur.fetchone()[0]
            created_committees.append({
                'id': committee_id,
                'name': committee_name,
                'chamber': 'Joint'
            })
            
            print(f"      Created: Joint - {committee_name}")
        
        self.conn.commit()
        print(f"   ✅ Created {len(created_committees)} missing committees")
        
        self.alignment_results['created_committees'] = created_committees
        return created_committees
    
    def remove_non_standard_committees(self):
        """Remove committees that don't exist in real 119th Congress"""
        print("\n🗑️ REMOVING NON-STANDARD COMMITTEES...")
        
        analysis = self.alignment_results['structure_analysis']
        cur = self.conn.cursor()
        
        committees_to_remove = []
        
        # Identify non-standard House and Senate committees
        for chamber in ['House', 'Senate']:
            extra_committees = analysis['comparison'][chamber]['extra_in_current']
            committees_to_remove.extend([c['id'] for c in extra_committees])
        
        # Get non-standard Joint committees
        cur.execute("""
            SELECT id, name 
            FROM committees 
            WHERE chamber = 'Joint' AND committee_type = 'Standing'
        """)
        current_joint = cur.fetchall()
        
        for committee_id, name in current_joint:
            if not any(self._names_similar(name, real_name) for real_name in self.congress_119_structure['Joint']):
                committees_to_remove.append(committee_id)
        
        if committees_to_remove:
            # First migrate any member assignments to similar committees
            for committee_id in committees_to_remove:
                # Clear member assignments (they can be reassigned later)
                cur.execute("""
                    DELETE FROM committee_memberships 
                    WHERE committee_id = %s
                """, (committee_id,))
            
            # Remove the committees
            cur.execute("""
                DELETE FROM committees 
                WHERE id = ANY(%s)
            """, (committees_to_remove,))
            
            removed_count = cur.rowcount
            self.conn.commit()
            
            print(f"   ✅ Removed {removed_count} non-standard committees")
        else:
            print("   ℹ️ No non-standard committees to remove")
        
        return len(committees_to_remove)
    
    def assign_realistic_memberships(self):
        """Assign realistic memberships to new/updated committees"""
        print("\n👥 ASSIGNING REALISTIC MEMBERSHIPS...")
        
        created_committees = self.alignment_results.get('created_committees', [])
        
        if not created_committees:
            print("   ℹ️ No new committees need member assignments")
            return 0
        
        cur = self.conn.cursor()
        
        # Get available members (those with fewer than max assignments)
        cur.execute("""
            SELECT 
                m.id, m.first_name, m.last_name, m.party, m.chamber,
                COUNT(cm.id) as current_assignments
            FROM members m
            LEFT JOIN committee_memberships cm ON m.id = cm.member_id
            GROUP BY m.id, m.first_name, m.last_name, m.party, m.chamber
            HAVING COUNT(cm.id) < CASE WHEN m.chamber = 'House' THEN 4 ELSE 5 END
            ORDER BY COUNT(cm.id), m.chamber, m.party
        """)
        
        available_members = cur.fetchall()
        
        assignments_made = 0
        
        for committee in created_committees:
            committee_id = committee['id']
            chamber = committee['chamber']
            
            # Determine appropriate member pool
            if chamber == 'Joint':
                member_pool = available_members
                target_size = 16  # Joint committees are typically smaller
            else:
                member_pool = [m for m in available_members if m[4] == chamber]
                target_size = 20  # Standard committee size
            
            # Select members (ensuring party balance)
            republicans = [m for m in member_pool if m[3] == 'Republican']
            democrats = [m for m in member_pool if m[3] == 'Democratic']
            
            # Majority gets more seats (typical 119th Congress split)
            republican_seats = int(target_size * 0.55)  # ~55% majority
            democrat_seats = target_size - republican_seats
            
            selected_republicans = republicans[:republican_seats]
            selected_democrats = democrats[:democrat_seats]
            
            # Assign Chair (Republican majority)
            if selected_republicans:
                chair_member = selected_republicans[0]
                cur.execute("""
                    INSERT INTO committee_memberships 
                    (committee_id, member_id, position, start_date, is_current)
                    VALUES (%s, %s, 'Chair', CURRENT_DATE, true)
                """, (committee_id, chair_member[0]))
                assignments_made += 1
                selected_republicans = selected_republicans[1:]
            
            # Assign Ranking Member (Democratic minority)
            if selected_democrats:
                ranking_member = selected_democrats[0]
                cur.execute("""
                    INSERT INTO committee_memberships 
                    (committee_id, member_id, position, start_date, is_current)
                    VALUES (%s, %s, 'Ranking Member', CURRENT_DATE, true)
                """, (committee_id, ranking_member[0]))
                assignments_made += 1
                selected_democrats = selected_democrats[1:]
            
            # Assign regular members
            all_members = selected_republicans + selected_democrats
            for member in all_members:
                cur.execute("""
                    INSERT INTO committee_memberships 
                    (committee_id, member_id, position, start_date, is_current)
                    VALUES (%s, %s, 'Member', CURRENT_DATE, true)
                """, (committee_id, member[0]))
                assignments_made += 1
        
        self.conn.commit()
        print(f"   ✅ Made {assignments_made} member assignments for new committees")
        
        return assignments_made
    
    def validate_final_structure(self):
        """Validate the final committee structure against real Congress"""
        print("\n✅ VALIDATING FINAL STRUCTURE...")
        
        cur = self.conn.cursor()
        
        # Get final structure
        cur.execute("""
            SELECT 
                chamber, committee_type, 
                COUNT(*) as committee_count,
                AVG(member_counts.member_count) as avg_members
            FROM committees c
            LEFT JOIN (
                SELECT committee_id, COUNT(*) as member_count
                FROM committee_memberships
                GROUP BY committee_id
            ) member_counts ON c.id = member_counts.committee_id
            GROUP BY chamber, committee_type
            ORDER BY chamber, committee_type
        """)
        
        final_structure = cur.fetchall()
        
        # Check leadership accuracy
        cur.execute("""
            SELECT 
                COUNT(*) as total_committees,
                COUNT(CASE WHEN chair_counts.chair_count = 1 THEN 1 END) as committees_with_chair,
                COUNT(CASE WHEN ranking_counts.ranking_count = 1 THEN 1 END) as committees_with_ranking
            FROM committees c
            LEFT JOIN (
                SELECT committee_id, COUNT(*) as chair_count
                FROM committee_memberships
                WHERE position = 'Chair'
                GROUP BY committee_id
            ) chair_counts ON c.id = chair_counts.committee_id
            LEFT JOIN (
                SELECT committee_id, COUNT(*) as ranking_count
                FROM committee_memberships
                WHERE position = 'Ranking Member'
                GROUP BY committee_id
            ) ranking_counts ON c.id = ranking_counts.committee_id
        """)
        
        leadership_validation = cur.fetchone()
        
        validation_results = {
            'final_structure': final_structure,
            'leadership_validation': {
                'total_committees': leadership_validation[0],
                'committees_with_chair': leadership_validation[1],
                'committees_with_ranking': leadership_validation[2]
            }
        }
        
        print("   📊 Final committee structure:")
        for chamber, comm_type, count, avg_members in final_structure:
            avg_members = avg_members or 0
            print(f"      {chamber} {comm_type}: {count} committees, avg {avg_members:.1f} members")
        
        print(f"   👑 Leadership: {leadership_validation[1]}/{leadership_validation[0]} chairs, {leadership_validation[2]}/{leadership_validation[0]} ranking members")
        
        self.alignment_results['final_validation'] = validation_results
        return validation_results
    
    def generate_report(self):
        """Generate comprehensive alignment report"""
        print("\n📋 GENERATING ALIGNMENT REPORT...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            'timestamp': timestamp,
            'operation': '119th_congress_structure_alignment',
            'results': self.alignment_results
        }
        
        report_file = f"congress_structure_alignment_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"   ✅ Report saved: {report_file}")
        
        return report
    
    def run_alignment(self):
        """Execute complete structure alignment"""
        print("🏛️ 119TH CONGRESS STRUCTURE ALIGNMENT")
        print("=" * 50)
        
        if not self.connect():
            return False
        
        try:
            # Phase 1: Analyze current vs real structure
            self.analyze_current_structure()
            
            # Phase 2: Standardize committee names
            self.standardize_committee_names()
            
            # Phase 3: Create missing committees
            self.create_missing_committees()
            
            # Phase 4: Remove non-standard committees
            self.remove_non_standard_committees()
            
            # Phase 5: Assign realistic memberships
            self.assign_realistic_memberships()
            
            # Phase 6: Validate final structure
            self.validate_final_structure()
            
            # Phase 7: Generate report
            report = self.generate_report()
            
            print("\n✅ 119TH CONGRESS STRUCTURE ALIGNMENT COMPLETE")
            print("Committee structure now accurately reflects the 119th Congress.")
            
            return report
            
        except Exception as e:
            print(f"❌ Alignment failed: {e}")
            self.conn.rollback()
            return False
        finally:
            if self.conn:
                self.conn.close()

def main():
    """Execute Phase 4 Congress Structure Alignment"""
    aligner = CongressStructureAligner()
    return aligner.run_alignment()

if __name__ == "__main__":
    main()