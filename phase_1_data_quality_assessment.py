#!/usr/bin/env python3
"""
Phase 1: Congressional Data Quality Assessment
Comprehensive analysis of committee duplicates, member assignments, and hierarchy issues.
"""

import psycopg2
import pandas as pd
from collections import defaultdict, Counter
import json
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'congress_data',
    'user': 'postgres',
    'password': 'mDf3S9ZnBpQqJvGsY1'
}

class CongressionalDataQualityAnalyzer:
    def __init__(self):
        self.conn = None
        self.analysis_results = {}
        
    def connect(self):
        """Establish database connection via Cloud SQL Proxy"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            print("✅ Connected to Congressional database")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def analyze_committee_duplicates(self):
        """Identify potential committee duplicates based on name, chamber, type"""
        print("\n📊 ANALYZING COMMITTEE DUPLICATES...")
        
        query = """
        SELECT 
            id,
            name,
            chamber,
            committee_type,
            congress_gov_id,
            parent_committee_id,
            created_at
        FROM committees 
        ORDER BY name, chamber, committee_type;
        """
        
        df = pd.read_sql(query, self.conn)
        total_committees = len(df)
        
        # Group by similar attributes to find duplicates
        duplicate_groups = defaultdict(list)
        
        for _, row in df.iterrows():
            # Normalize committee name for comparison
            name_normalized = row['name'].lower().strip()
            key = (name_normalized, row['chamber'], row['committee_type'])
            duplicate_groups[key].append(row.to_dict())
        
        # Find groups with multiple entries
        duplicates_found = []
        for key, committees in duplicate_groups.items():
            if len(committees) > 1:
                duplicates_found.append({
                    'normalized_key': key,
                    'count': len(committees),
                    'committees': committees
                })
        
        duplicate_count = sum(group['count'] - 1 for group in duplicates_found)
        
        self.analysis_results['committee_duplicates'] = {
            'total_committees': total_committees,
            'duplicate_groups': len(duplicates_found),
            'total_duplicates': duplicate_count,
            'duplicate_details': duplicates_found[:10]  # Show first 10 for review
        }
        
        print(f"   Total Committees: {total_committees}")
        print(f"   Duplicate Groups: {len(duplicates_found)}")
        print(f"   Total Duplicates: {duplicate_count}")
        print(f"   Potential Savings: {duplicate_count} committees could be removed")
        
        return duplicates_found
    
    def analyze_member_assignments(self):
        """Analyze committee member assignment coverage and gaps"""
        print("\n📊 ANALYZING MEMBER ASSIGNMENTS...")
        
        # Get committees without any members
        query_empty = """
        SELECT c.id, c.name, c.chamber, c.committee_type
        FROM committees c
        LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
        WHERE cm.committee_id IS NULL
        ORDER BY c.chamber, c.name;
        """
        
        empty_committees = pd.read_sql(query_empty, self.conn)
        
        # Get member assignment distribution
        query_distribution = """
        SELECT 
            c.chamber,
            c.committee_type,
            COUNT(DISTINCT cm.member_id) as member_count,
            COUNT(*) as assignment_count
        FROM committees c
        LEFT JOIN committee_memberships cm ON c.id = cm.committee_id
        GROUP BY c.chamber, c.committee_type
        ORDER BY c.chamber, c.committee_type;
        """
        
        distribution = pd.read_sql(query_distribution, self.conn)
        
        # Get total member coverage
        query_coverage = """
        SELECT 
            COUNT(DISTINCT m.id) as total_members,
            COUNT(DISTINCT cm.member_id) as assigned_members,
            COUNT(*) as total_assignments
        FROM members m
        LEFT JOIN committee_memberships cm ON m.id = cm.member_id;
        """
        
        coverage = pd.read_sql(query_coverage, self.conn).iloc[0]
        
        self.analysis_results['member_assignments'] = {
            'empty_committees': len(empty_committees),
            'empty_committee_details': empty_committees.to_dict('records'),
            'total_members': int(coverage['total_members']),
            'assigned_members': int(coverage['assigned_members']) if coverage['assigned_members'] else 0,
            'total_assignments': int(coverage['total_assignments']) if coverage['total_assignments'] else 0,
            'coverage_percentage': (coverage['assigned_members'] / coverage['total_members'] * 100) if coverage['assigned_members'] else 0,
            'distribution': distribution.to_dict('records')
        }
        
        print(f"   Empty Committees: {len(empty_committees)}")
        print(f"   Member Coverage: {coverage['assigned_members']}/{coverage['total_members']} ({coverage['assigned_members']/coverage['total_members']*100:.1f}%)")
        print(f"   Total Assignments: {coverage['total_assignments']}")
        
        return empty_committees
    
    def analyze_leadership_assignments(self):
        """Analyze chair and ranking member assignments for accuracy"""
        print("\n📊 ANALYZING LEADERSHIP ASSIGNMENTS...")
        
        # Get all leadership assignments with member party info from committee_memberships
        query = """
        SELECT 
            cm.id,
            cm.committee_id,
            cm.member_id,
            cm.position as leadership_role,
            c.name as committee_name,
            c.chamber,
            m.party,
            m.first_name,
            m.last_name
        FROM committee_memberships cm
        JOIN committees c ON cm.committee_id = c.id
        JOIN members m ON cm.member_id = m.id
        WHERE cm.position IN ('Chair', 'Ranking Member')
        ORDER BY c.chamber, c.name, cm.position;
        """
        
        leadership_df = pd.read_sql(query, self.conn)
        
        # Analyze chair/ranking member party distribution
        party_analysis = leadership_df.groupby(['leadership_role', 'party']).size().unstack(fill_value=0)
        
        # Find committees with multiple chairs or ranking members
        role_counts = leadership_df.groupby(['committee_id', 'leadership_role']).size()
        multiple_roles = role_counts[role_counts > 1]
        
        # Find committees missing chair or ranking member
        committee_leadership = leadership_df.groupby('committee_id')['leadership_role'].apply(list)
        missing_chair = []
        missing_ranking = []
        
        for committee_id, roles in committee_leadership.items():
            if 'Chair' not in roles:
                missing_chair.append(committee_id)
            if 'Ranking Member' not in roles:
                missing_ranking.append(committee_id)
        
        # Get party control info (simplified - assuming Republicans are majority)
        majority_party = 'Republican'
        minority_party = 'Democratic'
        
        # Check for incorrect party assignments
        incorrect_assignments = []
        for _, row in leadership_df.iterrows():
            if row['leadership_role'] == 'Chair' and row['party'] != majority_party:
                incorrect_assignments.append(f"Chair {row['first_name']} {row['last_name']} is {row['party']} (should be {majority_party})")
            elif row['leadership_role'] == 'Ranking Member' and row['party'] != minority_party:
                incorrect_assignments.append(f"Ranking Member {row['first_name']} {row['last_name']} is {row['party']} (should be {minority_party})")
        
        self.analysis_results['leadership_assignments'] = {
            'total_leadership_roles': len(leadership_df),
            'party_distribution': party_analysis.to_dict() if not party_analysis.empty else {},
            'multiple_roles_count': len(multiple_roles),
            'missing_chairs': len(missing_chair),
            'missing_ranking_members': len(missing_ranking),
            'incorrect_party_assignments': len(incorrect_assignments),
            'incorrect_assignment_details': incorrect_assignments[:10]
        }
        
        print(f"   Total Leadership Roles: {len(leadership_df)}")
        print(f"   Multiple Role Conflicts: {len(multiple_roles)}")
        print(f"   Missing Chairs: {len(missing_chair)}")
        print(f"   Missing Ranking Members: {len(missing_ranking)}")
        print(f"   Incorrect Party Assignments: {len(incorrect_assignments)}")
        
        return leadership_df
    
    def analyze_committee_hierarchy(self):
        """Analyze parent-subcommittee relationships"""
        print("\n📊 ANALYZING COMMITTEE HIERARCHY...")
        
        # Get all committees with parent relationships
        query = """
        SELECT 
            c.id,
            c.name,
            c.chamber,
            c.committee_type,
            c.parent_committee_id,
            p.name as parent_name,
            p.committee_type as parent_type
        FROM committees c
        LEFT JOIN committees p ON c.parent_committee_id = p.id
        ORDER BY c.chamber, c.parent_committee_id NULLS FIRST, c.name;
        """
        
        hierarchy_df = pd.read_sql(query, self.conn)
        
        # Analyze hierarchy structure
        top_level_committees = hierarchy_df[hierarchy_df['parent_committee_id'].isna()]
        subcommittees = hierarchy_df[hierarchy_df['parent_committee_id'].notna()]
        
        # Find orphaned subcommittees (parent doesn't exist)
        orphaned_subs = subcommittees[subcommittees['parent_name'].isna()]
        
        # Find incorrect hierarchy (subcommittee has subcommittees)
        subcommittee_parents = subcommittees[subcommittees['committee_type'] != 'Subcommittee']
        
        # Analyze hierarchy depth
        hierarchy_stats = {
            'total_committees': len(hierarchy_df),
            'top_level_committees': len(top_level_committees),
            'subcommittees': len(subcommittees),
            'orphaned_subcommittees': len(orphaned_subs),
            'hierarchy_errors': len(subcommittee_parents)
        }
        
        self.analysis_results['committee_hierarchy'] = {
            **hierarchy_stats,
            'orphaned_details': orphaned_subs.to_dict('records'),
            'hierarchy_error_details': subcommittee_parents.to_dict('records')
        }
        
        print(f"   Total Committees: {len(hierarchy_df)}")
        print(f"   Top-Level Committees: {len(top_level_committees)}")
        print(f"   Subcommittees: {len(subcommittees)}")
        print(f"   Orphaned Subcommittees: {len(orphaned_subs)}")
        print(f"   Hierarchy Errors: {len(subcommittee_parents)}")
        
        return hierarchy_df
    
    def analyze_119th_congress_accuracy(self):
        """Compare against known 119th Congress structure"""
        print("\n📊 ANALYZING 119th CONGRESS ACCURACY...")
        
        # Known 119th Congress committee counts (approximate)
        expected_structure = {
            'House': {
                'Standing': 20,  # Actual House standing committees
                'Subcommittee': 80,  # Approximate subcommittees
                'Joint': 4  # House participation in joint committees
            },
            'Senate': {
                'Standing': 16,  # Actual Senate standing committees
                'Subcommittee': 70,  # Approximate subcommittees
                'Joint': 4  # Senate participation in joint committees
            }
        }
        
        # Get current structure
        query = """
        SELECT 
            chamber,
            committee_type,
            COUNT(*) as count
        FROM committees
        GROUP BY chamber, committee_type
        ORDER BY chamber, committee_type;
        """
        
        current_structure = pd.read_sql(query, self.conn)
        current_dict = {}
        for _, row in current_structure.iterrows():
            if row['chamber'] not in current_dict:
                current_dict[row['chamber']] = {}
            current_dict[row['chamber']][row['committee_type']] = row['count']
        
        # Compare structures
        accuracy_analysis = {}
        for chamber in expected_structure:
            accuracy_analysis[chamber] = {}
            for comm_type in expected_structure[chamber]:
                expected = expected_structure[chamber][comm_type]
                actual = current_dict.get(chamber, {}).get(comm_type, 0)
                accuracy_analysis[chamber][comm_type] = {
                    'expected': expected,
                    'actual': actual,
                    'difference': actual - expected,
                    'percentage': (actual / expected * 100) if expected > 0 else 0
                }
        
        self.analysis_results['congress_accuracy'] = {
            'expected_structure': expected_structure,
            'current_structure': current_dict,
            'accuracy_analysis': accuracy_analysis
        }
        
        print(f"   Structure comparison completed")
        for chamber in accuracy_analysis:
            print(f"   {chamber}:")
            for comm_type in accuracy_analysis[chamber]:
                data = accuracy_analysis[chamber][comm_type]
                print(f"     {comm_type}: {data['actual']}/{data['expected']} ({data['percentage']:.1f}%)")
        
        return accuracy_analysis
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n📋 GENERATING SUMMARY REPORT...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = {
            'analysis_timestamp': timestamp,
            'executive_summary': {
                'total_committees': self.analysis_results['committee_duplicates']['total_committees'],
                'duplicate_committees': self.analysis_results['committee_duplicates']['total_duplicates'],
                'empty_committees': self.analysis_results['member_assignments']['empty_committees'],
                'leadership_errors': self.analysis_results['leadership_assignments']['incorrect_party_assignments'],
                'hierarchy_issues': self.analysis_results['committee_hierarchy']['orphaned_subcommittees']
            },
            'detailed_analysis': self.analysis_results
        }
        
        # Save report
        report_file = f"data_quality_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"   Report saved: {report_file}")
        
        # Print executive summary
        print("\n🎯 EXECUTIVE SUMMARY:")
        print(f"   Total Committees: {report['executive_summary']['total_committees']}")
        print(f"   Duplicate Committees: {report['executive_summary']['duplicate_committees']}")
        print(f"   Empty Committees: {report['executive_summary']['empty_committees']}")
        print(f"   Leadership Errors: {report['executive_summary']['leadership_errors']}")
        print(f"   Hierarchy Issues: {report['executive_summary']['hierarchy_issues']}")
        
        return report
    
    def run_full_analysis(self):
        """Execute complete data quality analysis"""
        print("🔍 CONGRESSIONAL DATA QUALITY ANALYSIS")
        print("=" * 50)
        
        if not self.connect():
            return False
        
        try:
            # Run all analysis phases
            self.analyze_committee_duplicates()
            self.analyze_member_assignments()
            self.analyze_leadership_assignments()
            self.analyze_committee_hierarchy()
            self.analyze_119th_congress_accuracy()
            
            # Generate summary
            report = self.generate_summary_report()
            
            print("\n✅ ANALYSIS COMPLETE")
            print("Review the generated report for detailed findings.")
            
            return report
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return False
        finally:
            if self.conn:
                self.conn.close()

def main():
    """Execute Phase 1 Data Quality Assessment"""
    analyzer = CongressionalDataQualityAnalyzer()
    return analyzer.run_full_analysis()

if __name__ == "__main__":
    main()