#!/usr/bin/env python3
"""
Data Freshness Validator Service

This service validates the currency and freshness of Congressional data
to ensure the database contains current, accurate information.

Key Functions:
- Member data currency validation
- Committee assignment validation
- Leadership position validation
- Database integrity checks
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataFreshnessLevel(Enum):
    """Data freshness levels"""
    FRESH = "fresh"
    STALE = "stale"
    OUTDATED = "outdated"
    CRITICAL = "critical"

class ValidationResult(Enum):
    """Validation result types"""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    ERROR = "error"

@dataclass
class DataFreshnessCheck:
    """Data freshness check result"""
    check_type: str
    status: ValidationResult
    freshness_level: DataFreshnessLevel
    details: str
    recommendations: List[str]
    timestamp: datetime
    metrics: Dict[str, any]

class DataFreshnessValidator:
    """Validate Congressional data freshness and currency"""
    
    def __init__(self, db_path: str = "congress_119th.db"):
        self.db_path = db_path
        self.current_congress = 119  # 119th Congress (2025-2027)
        self.expected_house_majority = "Republican"
        self.expected_senate_majority = "Republican"
        
    def validate_member_data_currency(self) -> DataFreshnessCheck:
        """Validate member data currency and completeness"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check member counts
                cursor.execute("SELECT COUNT(*) FROM members_119th")
                total_members = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM members_119th WHERE chamber = 'House'")
                house_members = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM members_119th WHERE chamber = 'Senate'")
                senate_members = cursor.fetchone()[0]
                
                # Check for missing data
                cursor.execute("SELECT COUNT(*) FROM members_119th WHERE name IS NULL OR name = ''")
                missing_names = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM members_119th WHERE party IS NULL OR party = ''")
                missing_parties = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM members_119th WHERE state IS NULL OR state = ''")
                missing_states = cursor.fetchone()[0]
                
                # Expected counts for 119th Congress
                expected_house = 441  # 435 voting + 6 non-voting
                expected_senate = 100
                expected_total = 541
                
                metrics = {
                    'total_members': total_members,
                    'house_members': house_members,
                    'senate_members': senate_members,
                    'missing_names': missing_names,
                    'missing_parties': missing_parties,
                    'missing_states': missing_states,
                    'expected_total': expected_total,
                    'expected_house': expected_house,
                    'expected_senate': expected_senate
                }
                
                # Determine validation result
                recommendations = []
                
                if total_members < expected_total * 0.9:  # Less than 90% of expected
                    status = ValidationResult.FAIL
                    freshness_level = DataFreshnessLevel.CRITICAL
                    recommendations.append(f"Critical: Only {total_members}/{expected_total} members found")
                elif total_members < expected_total:
                    status = ValidationResult.WARN
                    freshness_level = DataFreshnessLevel.STALE
                    recommendations.append(f"Warning: {total_members}/{expected_total} members found")
                else:
                    status = ValidationResult.PASS
                    freshness_level = DataFreshnessLevel.FRESH
                
                # Check for missing data
                if missing_names > 0:
                    recommendations.append(f"Missing names for {missing_names} members")
                if missing_parties > 0:
                    recommendations.append(f"Missing party affiliation for {missing_parties} members")
                if missing_states > 0:
                    recommendations.append(f"Missing state information for {missing_states} members")
                
                # Check chamber distribution
                if house_members < expected_house * 0.9:
                    recommendations.append(f"House members below expected: {house_members}/{expected_house}")
                if senate_members < expected_senate * 0.9:
                    recommendations.append(f"Senate members below expected: {senate_members}/{expected_senate}")
                
                details = f"Member data validation: {total_members} total members ({house_members} House, {senate_members} Senate)"
                
                return DataFreshnessCheck(
                    check_type="member_data_currency",
                    status=status,
                    freshness_level=freshness_level,
                    details=details,
                    recommendations=recommendations,
                    timestamp=datetime.now(),
                    metrics=metrics
                )
                
        except sqlite3.Error as e:
            logger.error(f"Database error validating member data: {e}")
            return DataFreshnessCheck(
                check_type="member_data_currency",
                status=ValidationResult.ERROR,
                freshness_level=DataFreshnessLevel.CRITICAL,
                details=f"Database error: {e}",
                recommendations=["Fix database connection issues"],
                timestamp=datetime.now(),
                metrics={}
            )
    
    def validate_committee_assignments(self) -> DataFreshnessCheck:
        """Validate committee assignment currency and completeness"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check committee assignment coverage
                cursor.execute("""
                    SELECT COUNT(DISTINCT m.id) 
                    FROM members_119th m
                    JOIN committee_memberships_119th cm ON m.id = cm.member_id
                """)
                members_with_assignments = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM members_119th")
                total_members = cursor.fetchone()[0]
                
                # Check committee counts
                cursor.execute("SELECT COUNT(*) FROM committees_119th")
                total_committees = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM committee_memberships_119th")
                total_assignments = cursor.fetchone()[0]
                
                # Check for orphaned assignments
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM committee_memberships_119th cm
                    LEFT JOIN members_119th m ON cm.member_id = m.id
                    WHERE m.id IS NULL
                """)
                orphaned_assignments = cursor.fetchone()[0]
                
                # Check leadership positions
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM committee_memberships_119th 
                    WHERE position IN ('Chair', 'Ranking Member')
                """)
                leadership_positions = cursor.fetchone()[0]
                
                metrics = {
                    'members_with_assignments': members_with_assignments,
                    'total_members': total_members,
                    'assignment_coverage': (members_with_assignments / total_members * 100) if total_members > 0 else 0,
                    'total_committees': total_committees,
                    'total_assignments': total_assignments,
                    'orphaned_assignments': orphaned_assignments,
                    'leadership_positions': leadership_positions
                }
                
                # Determine validation result
                recommendations = []
                coverage = metrics['assignment_coverage']
                
                if coverage < 50:  # Less than 50% coverage
                    status = ValidationResult.FAIL
                    freshness_level = DataFreshnessLevel.CRITICAL
                    recommendations.append(f"Critical: Only {coverage:.1f}% of members have committee assignments")
                elif coverage < 80:  # Less than 80% coverage
                    status = ValidationResult.WARN
                    freshness_level = DataFreshnessLevel.STALE
                    recommendations.append(f"Warning: {coverage:.1f}% committee assignment coverage")
                else:
                    status = ValidationResult.PASS
                    freshness_level = DataFreshnessLevel.FRESH
                
                # Check for data quality issues
                if orphaned_assignments > 0:
                    recommendations.append(f"Found {orphaned_assignments} orphaned committee assignments")
                
                if leadership_positions < total_committees * 0.5:  # Expect at least 50% committees to have leadership
                    recommendations.append(f"Low leadership position coverage: {leadership_positions} positions")
                
                details = f"Committee assignment validation: {members_with_assignments}/{total_members} members have assignments ({coverage:.1f}%)"
                
                return DataFreshnessCheck(
                    check_type="committee_assignments",
                    status=status,
                    freshness_level=freshness_level,
                    details=details,
                    recommendations=recommendations,
                    timestamp=datetime.now(),
                    metrics=metrics
                )
                
        except sqlite3.Error as e:
            logger.error(f"Database error validating committee assignments: {e}")
            return DataFreshnessCheck(
                check_type="committee_assignments",
                status=ValidationResult.ERROR,
                freshness_level=DataFreshnessLevel.CRITICAL,
                details=f"Database error: {e}",
                recommendations=["Fix database connection issues"],
                timestamp=datetime.now(),
                metrics={}
            )
    
    def validate_leadership_positions(self) -> DataFreshnessCheck:
        """Validate committee leadership positions for current Congress"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check party distribution of committee chairs
                cursor.execute("""
                    SELECT m.party, COUNT(*) as chair_count
                    FROM committee_memberships_119th cm
                    JOIN members_119th m ON cm.member_id = m.id
                    WHERE cm.position = 'Chair'
                    GROUP BY m.party
                """)
                chair_distribution = dict(cursor.fetchall())
                
                # Check party distribution of ranking members
                cursor.execute("""
                    SELECT m.party, COUNT(*) as ranking_count
                    FROM committee_memberships_119th cm
                    JOIN members_119th m ON cm.member_id = m.id
                    WHERE cm.position = 'Ranking Member'
                    GROUP BY m.party
                """)
                ranking_distribution = dict(cursor.fetchall())
                
                # Check total leadership positions
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM committee_memberships_119th 
                    WHERE position IN ('Chair', 'Ranking Member')
                """)
                total_leadership = cursor.fetchone()[0]
                
                # Check committees without leadership
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM committees_119th c
                    LEFT JOIN committee_memberships_119th cm ON c.id = cm.committee_id AND cm.position = 'Chair'
                    WHERE cm.committee_id IS NULL
                """)
                committees_without_chairs = cursor.fetchone()[0]
                
                metrics = {
                    'chair_distribution': chair_distribution,
                    'ranking_distribution': ranking_distribution,
                    'total_leadership': total_leadership,
                    'committees_without_chairs': committees_without_chairs,
                    'republican_chairs': chair_distribution.get('Republican', 0),
                    'democratic_chairs': chair_distribution.get('Democratic', 0)
                }
                
                # Determine validation result based on expected party control
                recommendations = []
                republican_chairs = metrics['republican_chairs']
                democratic_chairs = metrics['democratic_chairs']
                
                # For 119th Congress, expect Republican majority in chairs
                if self.expected_house_majority == "Republican":
                    if republican_chairs <= democratic_chairs:
                        status = ValidationResult.FAIL
                        freshness_level = DataFreshnessLevel.CRITICAL
                        recommendations.append(f"Critical: Expected Republican chair majority, found {republican_chairs} R vs {democratic_chairs} D")
                    elif republican_chairs < democratic_chairs * 1.5:  # Expect significant majority
                        status = ValidationResult.WARN
                        freshness_level = DataFreshnessLevel.STALE
                        recommendations.append(f"Warning: Low Republican chair majority: {republican_chairs} R vs {democratic_chairs} D")
                    else:
                        status = ValidationResult.PASS
                        freshness_level = DataFreshnessLevel.FRESH
                
                # Check for missing leadership
                if committees_without_chairs > 0:
                    recommendations.append(f"Found {committees_without_chairs} committees without chairs")
                
                if total_leadership < 50:  # Expect at least 50 leadership positions
                    recommendations.append(f"Low total leadership positions: {total_leadership}")
                
                details = f"Leadership validation: {republican_chairs} Republican chairs, {democratic_chairs} Democratic chairs"
                
                return DataFreshnessCheck(
                    check_type="leadership_positions",
                    status=status,
                    freshness_level=freshness_level,
                    details=details,
                    recommendations=recommendations,
                    timestamp=datetime.now(),
                    metrics=metrics
                )
                
        except sqlite3.Error as e:
            logger.error(f"Database error validating leadership positions: {e}")
            return DataFreshnessCheck(
                check_type="leadership_positions",
                status=ValidationResult.ERROR,
                freshness_level=DataFreshnessLevel.CRITICAL,
                details=f"Database error: {e}",
                recommendations=["Fix database connection issues"],
                timestamp=datetime.now(),
                metrics={}
            )
    
    def validate_database_integrity(self) -> DataFreshnessCheck:
        """Validate database integrity and consistency"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check for duplicate members
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM (
                        SELECT name, COUNT(*) as count
                        FROM members_119th
                        GROUP BY name
                        HAVING COUNT(*) > 1
                    )
                """)
                duplicate_members = cursor.fetchone()[0]
                
                # Check for invalid references
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM committee_memberships_119th cm
                    LEFT JOIN members_119th m ON cm.member_id = m.id
                    LEFT JOIN committees_119th c ON cm.committee_id = c.id
                    WHERE m.id IS NULL OR c.id IS NULL
                """)
                invalid_references = cursor.fetchone()[0]
                
                # Check for missing required fields
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM members_119th 
                    WHERE name IS NULL OR party IS NULL OR chamber IS NULL
                """)
                missing_required_fields = cursor.fetchone()[0]
                
                # Check database schema version
                cursor.execute("""
                    SELECT name 
                    FROM sqlite_master 
                    WHERE type='table' AND name='congressional_sessions'
                """)
                has_session_table = cursor.fetchone() is not None
                
                metrics = {
                    'duplicate_members': duplicate_members,
                    'invalid_references': invalid_references,
                    'missing_required_fields': missing_required_fields,
                    'has_session_table': has_session_table,
                    'database_accessible': True
                }
                
                # Determine validation result
                recommendations = []
                
                if duplicate_members > 0:
                    recommendations.append(f"Found {duplicate_members} duplicate member entries")
                
                if invalid_references > 0:
                    recommendations.append(f"Found {invalid_references} invalid committee assignment references")
                
                if missing_required_fields > 0:
                    recommendations.append(f"Found {missing_required_fields} members with missing required fields")
                
                if not has_session_table:
                    recommendations.append("Missing congressional_sessions table - schema update needed")
                
                if len(recommendations) == 0:
                    status = ValidationResult.PASS
                    freshness_level = DataFreshnessLevel.FRESH
                    details = "Database integrity validation passed"
                elif len(recommendations) <= 2:
                    status = ValidationResult.WARN
                    freshness_level = DataFreshnessLevel.STALE
                    details = f"Database integrity issues found: {len(recommendations)} issues"
                else:
                    status = ValidationResult.FAIL
                    freshness_level = DataFreshnessLevel.CRITICAL
                    details = f"Critical database integrity issues: {len(recommendations)} issues"
                
                return DataFreshnessCheck(
                    check_type="database_integrity",
                    status=status,
                    freshness_level=freshness_level,
                    details=details,
                    recommendations=recommendations,
                    timestamp=datetime.now(),
                    metrics=metrics
                )
                
        except sqlite3.Error as e:
            logger.error(f"Database error validating integrity: {e}")
            return DataFreshnessCheck(
                check_type="database_integrity",
                status=ValidationResult.ERROR,
                freshness_level=DataFreshnessLevel.CRITICAL,
                details=f"Database error: {e}",
                recommendations=["Fix database connection issues"],
                timestamp=datetime.now(),
                metrics={}
            )
    
    def run_comprehensive_validation(self) -> Dict[str, DataFreshnessCheck]:
        """Run comprehensive data freshness validation"""
        logger.info("Running comprehensive data freshness validation")
        
        validations = {
            'member_data': self.validate_member_data_currency(),
            'committee_assignments': self.validate_committee_assignments(),
            'leadership_positions': self.validate_leadership_positions(),
            'database_integrity': self.validate_database_integrity()
        }
        
        return validations
    
    def generate_freshness_report(self) -> Dict[str, any]:
        """Generate comprehensive data freshness report"""
        validations = self.run_comprehensive_validation()
        
        # Calculate overall status
        critical_issues = sum(1 for v in validations.values() if v.status == ValidationResult.FAIL)
        warning_issues = sum(1 for v in validations.values() if v.status == ValidationResult.WARN)
        error_issues = sum(1 for v in validations.values() if v.status == ValidationResult.ERROR)
        
        if critical_issues > 0 or error_issues > 0:
            overall_status = "CRITICAL"
        elif warning_issues > 0:
            overall_status = "WARNING"
        else:
            overall_status = "HEALTHY"
        
        # Collect all recommendations
        all_recommendations = []
        for validation in validations.values():
            all_recommendations.extend(validation.recommendations)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall_status,
            'summary': {
                'total_checks': len(validations),
                'passed': sum(1 for v in validations.values() if v.status == ValidationResult.PASS),
                'warnings': warning_issues,
                'critical': critical_issues,
                'errors': error_issues
            },
            'validations': {
                name: {
                    'status': validation.status.value,
                    'freshness_level': validation.freshness_level.value,
                    'details': validation.details,
                    'recommendations': validation.recommendations,
                    'metrics': validation.metrics
                }
                for name, validation in validations.items()
            },
            'recommendations': all_recommendations,
            'next_check_recommended': (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        return report
    
    def log_validation_results(self, validations: Dict[str, DataFreshnessCheck]):
        """Log validation results to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Ensure data_freshness_log table exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS data_freshness_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        check_type TEXT NOT NULL,
                        status TEXT NOT NULL,
                        details TEXT,
                        recommendations TEXT,
                        metrics TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insert validation results
                for name, validation in validations.items():
                    cursor.execute("""
                        INSERT INTO data_freshness_log 
                        (check_type, status, details, recommendations, metrics)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        validation.check_type,
                        validation.status.value,
                        validation.details,
                        '\n'.join(validation.recommendations),
                        str(validation.metrics)
                    ))
                
                conn.commit()
                logger.info(f"Logged {len(validations)} validation results")
                
        except sqlite3.Error as e:
            logger.error(f"Error logging validation results: {e}")

def main():
    """Main function for testing the Data Freshness Validator"""
    validator = DataFreshnessValidator()
    
    # Run comprehensive validation
    report = validator.generate_freshness_report()
    
    print("\n" + "="*60)
    print("DATA FRESHNESS VALIDATION REPORT")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}")
    print(f"Overall Status: {report['overall_status']}")
    print(f"Checks: {report['summary']['passed']}/{report['summary']['total_checks']} passed")
    print(f"Warnings: {report['summary']['warnings']}")
    print(f"Critical: {report['summary']['critical']}")
    print(f"Errors: {report['summary']['errors']}")
    
    print("\nValidation Results:")
    for name, validation in report['validations'].items():
        status_icon = "✅" if validation['status'] == 'pass' else "⚠️" if validation['status'] == 'warn' else "❌"
        print(f"  {status_icon} {name}: {validation['status'].upper()}")
        print(f"    {validation['details']}")
        if validation['recommendations']:
            for rec in validation['recommendations']:
                print(f"    → {rec}")
    
    if report['recommendations']:
        print("\nOverall Recommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
    
    print(f"\nNext check recommended: {report['next_check_recommended']}")
    print("="*60)

if __name__ == "__main__":
    main()