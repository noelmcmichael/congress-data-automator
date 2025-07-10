#!/usr/bin/env python3
"""
Comprehensive Congressional Data Verification System
Compares database against authoritative sources with detailed analysis
"""

import psycopg2
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging
from authoritative_data_fetcher import AuthoritativeDataFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveVerifier:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        
        self.fetcher = AuthoritativeDataFetcher()
        self.authoritative_data = None
        self.database_data = None
        self.verification_results = {
            'timestamp': datetime.now().isoformat(),
            'congress': '119th',
            'summary': {},
            'committee_analysis': {},
            'leadership_analysis': {},
            'member_analysis': {},
            'discrepancies': [],
            'accuracy_scores': {}
        }
    
    def fetch_authoritative_data(self):
        """Fetch authoritative congressional data"""
        logger.info("Fetching authoritative data...")
        self.authoritative_data = self.fetcher.fetch_complete_authoritative_data()
        
    def fetch_database_data(self):
        """Fetch all relevant data from database"""
        logger.info("Fetching database data...")
        
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    # Get committees
                    cursor.execute("""
                        SELECT id, name, chamber, committee_type, 
                               parent_committee_id, is_active
                        FROM committees
                        WHERE is_active = true
                        ORDER BY chamber, name
                    """)
                    
                    committees = []
                    for row in cursor.fetchall():
                        committees.append({
                            'id': row[0],
                            'name': row[1],
                            'chamber': row[2],
                            'type': row[3],
                            'parent_id': row[4],
                            'is_active': row[5]
                        })
                    
                    # Get members with assignments
                    cursor.execute("""
                        SELECT m.id, m.first_name, m.last_name, m.party, 
                               m.chamber, m.state, c.name as committee_name,
                               cm.position, cm.is_current
                        FROM members m
                        JOIN committee_memberships cm ON m.id = cm.member_id
                        JOIN committees c ON cm.committee_id = c.id
                        WHERE cm.is_current = true AND c.is_active = true
                        ORDER BY m.last_name, m.first_name
                    """)
                    
                    members = []
                    for row in cursor.fetchall():
                        members.append({
                            'id': row[0],
                            'first_name': row[1],
                            'last_name': row[2],
                            'full_name': f"{row[1]} {row[2]}",
                            'party': row[3],
                            'chamber': row[4],
                            'state': row[5],
                            'committee': row[6],
                            'position': row[7],
                            'is_current': row[8]
                        })
                    
                    # Get leadership positions
                    cursor.execute("""
                        SELECT c.name as committee_name, c.chamber, 
                               m.first_name, m.last_name, m.party, cm.position
                        FROM committees c
                        JOIN committee_memberships cm ON c.id = cm.committee_id
                        JOIN members m ON cm.member_id = m.id
                        WHERE cm.position IN ('Chair', 'Ranking Member')
                        AND c.is_active = true AND cm.is_current = true
                        ORDER BY c.chamber, c.name, cm.position
                    """)
                    
                    leadership = []
                    for row in cursor.fetchall():
                        leadership.append({
                            'committee': row[0],
                            'chamber': row[1],
                            'member_name': f"{row[2]} {row[3]}",
                            'party': row[4],
                            'position': row[5]
                        })
                    
                    self.database_data = {
                        'committees': committees,
                        'members': members,
                        'leadership': leadership,
                        'totals': {
                            'committees': len(committees),
                            'members': len(set(m['id'] for m in members)),
                            'assignments': len(members),
                            'leadership_positions': len(leadership)
                        }
                    }
                    
                    logger.info(f"Database data fetched: {self.database_data['totals']}")
                    
        except Exception as e:
            logger.error(f"Error fetching database data: {e}")
            self.database_data = {'committees': [], 'members': [], 'leadership': []}
    
    def analyze_committee_accuracy(self):
        """Analyze committee structure accuracy"""
        logger.info("Analyzing committee accuracy...")
        
        if not self.authoritative_data or not self.database_data:
            return
        
        # Get authoritative committee names by chamber
        auth_house = {c['name'] for c in self.authoritative_data['house_committees']}
        auth_senate = {c['name'] for c in self.authoritative_data['senate_committees']}
        auth_joint = {c['name'] for c in self.authoritative_data['joint_committees']}
        
        # Get database committee names by chamber
        db_house = {c['name'] for c in self.database_data['committees'] if c['chamber'] == 'House'}
        db_senate = {c['name'] for c in self.database_data['committees'] if c['chamber'] == 'Senate'}
        db_joint = {c['name'] for c in self.database_data['committees'] if c['chamber'] == 'Joint'}
        
        # Find discrepancies
        discrepancies = []
        
        # House committee discrepancies
        house_missing = auth_house - db_house
        house_extra = db_house - auth_house
        house_correct = auth_house & db_house
        
        for name in house_missing:
            discrepancies.append({
                'type': 'missing_committee',
                'chamber': 'House',
                'committee': name,
                'severity': 'high',
                'description': 'Official committee missing from database'
            })
        
        for name in house_extra:
            discrepancies.append({
                'type': 'extra_committee',
                'chamber': 'House',
                'committee': name,
                'severity': 'medium',
                'description': 'Database committee not found in official sources'
            })
        
        # Senate committee discrepancies
        senate_missing = auth_senate - db_senate
        senate_extra = db_senate - auth_senate
        senate_correct = auth_senate & db_senate
        
        for name in senate_missing:
            discrepancies.append({
                'type': 'missing_committee',
                'chamber': 'Senate',
                'committee': name,
                'severity': 'high',
                'description': 'Official committee missing from database'
            })
        
        for name in senate_extra:
            discrepancies.append({
                'type': 'extra_committee',
                'chamber': 'Senate',
                'committee': name,
                'severity': 'medium',
                'description': 'Database committee not found in official sources'
            })
        
        # Joint committee discrepancies
        joint_missing = auth_joint - db_joint
        joint_extra = db_joint - auth_joint
        joint_correct = auth_joint & db_joint
        
        for name in joint_missing:
            discrepancies.append({
                'type': 'missing_committee',
                'chamber': 'Joint',
                'committee': name,
                'severity': 'high',
                'description': 'Official committee missing from database'
            })
        
        for name in joint_extra:
            discrepancies.append({
                'type': 'extra_committee',
                'chamber': 'Joint',
                'committee': name,
                'severity': 'medium',
                'description': 'Database committee not found in official sources'
            })
        
        # Calculate accuracy scores
        house_accuracy = len(house_correct) / len(auth_house) if auth_house else 0
        senate_accuracy = len(senate_correct) / len(auth_senate) if auth_senate else 0
        joint_accuracy = len(joint_correct) / len(auth_joint) if auth_joint else 0
        
        total_auth = len(auth_house) + len(auth_senate) + len(auth_joint)
        total_correct = len(house_correct) + len(senate_correct) + len(joint_correct)
        overall_accuracy = total_correct / total_auth if total_auth else 0
        
        self.verification_results['committee_analysis'] = {
            'house': {
                'authoritative_count': len(auth_house),
                'database_count': len(db_house),
                'correct_count': len(house_correct),
                'missing_count': len(house_missing),
                'extra_count': len(house_extra),
                'accuracy': house_accuracy
            },
            'senate': {
                'authoritative_count': len(auth_senate),
                'database_count': len(db_senate),
                'correct_count': len(senate_correct),
                'missing_count': len(senate_missing),
                'extra_count': len(senate_extra),
                'accuracy': senate_accuracy
            },
            'joint': {
                'authoritative_count': len(auth_joint),
                'database_count': len(db_joint),
                'correct_count': len(joint_correct),
                'missing_count': len(joint_missing),
                'extra_count': len(joint_extra),
                'accuracy': joint_accuracy
            },
            'overall': {
                'total_authoritative': total_auth,
                'total_correct': total_correct,
                'overall_accuracy': overall_accuracy
            }
        }
        
        self.verification_results['discrepancies'].extend(discrepancies)
        logger.info(f"Committee analysis complete: {overall_accuracy:.2%} accuracy")
    
    def analyze_leadership_accuracy(self):
        """Analyze leadership position accuracy"""
        logger.info("Analyzing leadership accuracy...")
        
        if not self.authoritative_data or not self.database_data:
            return
        
        leadership_structure = self.authoritative_data['leadership_structure']
        leadership_errors = []
        
        for leader in self.database_data['leadership']:
            committee = leader['committee']
            chamber = leader['chamber']
            party = leader['party']
            position = leader['position']
            member = leader['member_name']
            
            # Check if leadership positions match expected party control
            if chamber == 'House':
                expected_chair_party = leadership_structure['house']['majority_party']
                expected_ranking_party = leadership_structure['house']['minority_party']
            else:  # Senate
                expected_chair_party = leadership_structure['senate']['majority_party']
                expected_ranking_party = leadership_structure['senate']['minority_party']
            
            if position == 'Chair':
                if party != expected_chair_party:
                    leadership_errors.append({
                        'committee': committee,
                        'chamber': chamber,
                        'member': member,
                        'position': position,
                        'current_party': party,
                        'expected_party': expected_chair_party,
                        'severity': 'high',
                        'error': f"Chair should be {expected_chair_party}, found {party}"
                    })
            
            elif position == 'Ranking Member':
                if party != expected_ranking_party:
                    leadership_errors.append({
                        'committee': committee,
                        'chamber': chamber,
                        'member': member,
                        'position': position,
                        'current_party': party,
                        'expected_party': expected_ranking_party,
                        'severity': 'high',
                        'error': f"Ranking Member should be {expected_ranking_party}, found {party}"
                    })
        
        # Calculate leadership accuracy
        total_leadership = len(self.database_data['leadership'])
        correct_leadership = total_leadership - len(leadership_errors)
        leadership_accuracy = correct_leadership / total_leadership if total_leadership else 0
        
        self.verification_results['leadership_analysis'] = {
            'total_positions': total_leadership,
            'correct_positions': correct_leadership,
            'error_count': len(leadership_errors),
            'accuracy': leadership_accuracy,
            'errors': leadership_errors
        }
        
        self.verification_results['discrepancies'].extend([
            {
                'type': 'leadership_error',
                'chamber': error['chamber'],
                'committee': error['committee'],
                'severity': error['severity'],
                'description': error['error']
            }
            for error in leadership_errors
        ])
        
        logger.info(f"Leadership analysis complete: {leadership_accuracy:.2%} accuracy")
    
    def calculate_overall_accuracy(self):
        """Calculate overall data accuracy scores"""
        logger.info("Calculating overall accuracy...")
        
        committee_accuracy = self.verification_results['committee_analysis']['overall']['overall_accuracy']
        leadership_accuracy = self.verification_results['leadership_analysis']['accuracy']
        
        # Weight committee accuracy more heavily
        overall_accuracy = (committee_accuracy * 0.7) + (leadership_accuracy * 0.3)
        
        total_discrepancies = len(self.verification_results['discrepancies'])
        high_severity_count = sum(1 for d in self.verification_results['discrepancies'] if d.get('severity') == 'high')
        
        self.verification_results['accuracy_scores'] = {
            'committee_accuracy': committee_accuracy,
            'leadership_accuracy': leadership_accuracy,
            'overall_accuracy': overall_accuracy,
            'total_discrepancies': total_discrepancies,
            'high_severity_discrepancies': high_severity_count,
            'data_quality_grade': self.get_quality_grade(overall_accuracy)
        }
        
        logger.info(f"Overall accuracy: {overall_accuracy:.2%}")
    
    def get_quality_grade(self, accuracy: float) -> str:
        """Convert accuracy to letter grade"""
        if accuracy >= 0.95:
            return "A"
        elif accuracy >= 0.90:
            return "B"
        elif accuracy >= 0.80:
            return "C"
        elif accuracy >= 0.70:
            return "D"
        else:
            return "F"
    
    def generate_comprehensive_report(self) -> str:
        """Generate detailed verification report"""
        logger.info("Generating comprehensive report...")
        
        # Run all analyses
        self.fetch_authoritative_data()
        self.fetch_database_data()
        self.analyze_committee_accuracy()
        self.analyze_leadership_accuracy()
        self.calculate_overall_accuracy()
        
        # Generate report
        ca = self.verification_results['committee_analysis']
        la = self.verification_results['leadership_analysis']
        acc = self.verification_results['accuracy_scores']
        
        report = f"""
COMPREHENSIVE CONGRESSIONAL DATA VERIFICATION REPORT
===================================================
Generated: {self.verification_results['timestamp']}
Congress: {self.verification_results['congress']}

OVERALL ACCURACY ASSESSMENT
===========================
Data Quality Grade: {acc['data_quality_grade']}
Overall Accuracy: {acc['overall_accuracy']:.2%}
Committee Accuracy: {acc['committee_accuracy']:.2%}
Leadership Accuracy: {acc['leadership_accuracy']:.2%}

Total Discrepancies: {acc['total_discrepancies']}
High Severity Issues: {acc['high_severity_discrepancies']}

COMMITTEE STRUCTURE ANALYSIS
============================
House Committees:
  - Official: {ca['house']['authoritative_count']} | Database: {ca['house']['database_count']}
  - Correct: {ca['house']['correct_count']} | Missing: {ca['house']['missing_count']} | Extra: {ca['house']['extra_count']}
  - Accuracy: {ca['house']['accuracy']:.2%}

Senate Committees:
  - Official: {ca['senate']['authoritative_count']} | Database: {ca['senate']['database_count']}
  - Correct: {ca['senate']['correct_count']} | Missing: {ca['senate']['missing_count']} | Extra: {ca['senate']['extra_count']}
  - Accuracy: {ca['senate']['accuracy']:.2%}

Joint Committees:
  - Official: {ca['joint']['authoritative_count']} | Database: {ca['joint']['database_count']}
  - Correct: {ca['joint']['correct_count']} | Missing: {ca['joint']['missing_count']} | Extra: {ca['joint']['extra_count']}
  - Accuracy: {ca['joint']['accuracy']:.2%}

LEADERSHIP ANALYSIS
==================
Total Leadership Positions: {la['total_positions']}
Correct Positions: {la['correct_positions']}
Leadership Errors: {la['error_count']}
Leadership Accuracy: {la['accuracy']:.2%}

DETAILED DISCREPANCIES
=====================
"""
        
        # Group discrepancies by type
        by_type = {}
        for disc in self.verification_results['discrepancies']:
            disc_type = disc['type']
            if disc_type not in by_type:
                by_type[disc_type] = []
            by_type[disc_type].append(disc)
        
        for disc_type, discrepancies in by_type.items():
            report += f"\n{disc_type.upper().replace('_', ' ')} ({len(discrepancies)} issues):\n"
            for disc in discrepancies:
                severity = disc.get('severity', 'medium').upper()
                report += f"  [{severity}] {disc['chamber']} - {disc.get('committee', 'N/A')}: {disc['description']}\n"
        
        if not self.verification_results['discrepancies']:
            report += "\nNo discrepancies found.\n"
        
        report += f"""
RECOMMENDATIONS
===============
"""
        
        if acc['overall_accuracy'] < 0.95:
            report += "- Immediate data quality remediation required\n"
        if acc['high_severity_discrepancies'] > 0:
            report += f"- Address {acc['high_severity_discrepancies']} high-severity issues first\n"
        if ca['house']['missing_count'] > 0:
            report += f"- Add {ca['house']['missing_count']} missing House committees\n"
        if ca['senate']['missing_count'] > 0:
            report += f"- Add {ca['senate']['missing_count']} missing Senate committees\n"
        if la['error_count'] > 0:
            report += f"- Fix {la['error_count']} leadership position errors\n"
        
        return report
    
    def save_results(self, filename: str = None):
        """Save verification results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comprehensive_verification_{timestamp}.json"
        
        filepath = f"/Users/noelmcmichael/Workspace/congress_data_automator/docs/progress/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.verification_results, f, indent=2)
        
        logger.info(f"Verification results saved to {filepath}")
        return filepath

def main():
    """Run comprehensive verification"""
    verifier = ComprehensiveVerifier()
    
    print("Starting Comprehensive Congressional Data Verification...")
    print("=" * 60)
    
    # Generate report
    report = verifier.generate_comprehensive_report()
    print(report)
    
    # Save results
    results_file = verifier.save_results()
    print(f"\nDetailed results saved to: {results_file}")
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"/Users/noelmcmichael/Workspace/congress_data_automator/docs/progress/comprehensive_verification_report_{timestamp}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"Report saved to: {report_file}")

if __name__ == "__main__":
    main()