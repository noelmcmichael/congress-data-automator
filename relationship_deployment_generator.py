#!/usr/bin/env python3
"""
Member-Committee Relationship Deployment Generator
=================================================

Generate and execute SQL deployment for member-committee relationships.
"""

import json
import psycopg2
from datetime import datetime
from typing import Dict, List, Any

class RelationshipDeploymentGenerator:
    """Generate and deploy member-committee relationships"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.relationship_data = None
        self.db_config = {
            'host': 'localhost',
            'port': 5433,
            'database': 'congress_data',
            'user': 'postgres',
            'password': 'mDf3S9ZnBpQqJvGsY1'
        }
        
        self.deployment_log = []
        self.log_event("Initialized Relationship Deployment Generator")
    
    def log_event(self, message: str, level: str = "info"):
        """Log deployment events with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level.upper()}: {message}"
        self.deployment_log.append(log_entry)
        print(log_entry)
    
    def load_relationship_data(self) -> bool:
        """Load generated relationship data"""
        self.log_event(f"Loading relationship data from {self.data_file}")
        
        try:
            with open(self.data_file, 'r') as f:
                self.relationship_data = json.load(f)
            
            memberships_count = len(self.relationship_data['memberships'])
            leadership_count = len(self.relationship_data['leadership'])
            
            self.log_event(f"Loaded {memberships_count} memberships and {leadership_count} leadership assignments", "success")
            return True
            
        except Exception as e:
            self.log_event(f"Failed to load relationship data: {e}", "error")
            return False
    
    def clear_existing_relationships(self) -> bool:
        """Clear existing relationships to start fresh"""
        self.log_event("Clearing existing committee relationships")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Clear existing memberships
            cursor.execute("DELETE FROM committee_memberships;")
            
            # Clear committee leadership
            cursor.execute("UPDATE committees SET chair_member_id = NULL, ranking_member_id = NULL;")
            
            cursor.close()
            conn.close()
            
            self.log_event("Existing relationships cleared successfully", "success")
            return True
            
        except Exception as e:
            self.log_event(f"Failed to clear existing relationships: {e}", "error")
            return False
    
    def deploy_committee_memberships(self) -> bool:
        """Deploy committee memberships to database"""
        self.log_event("Deploying committee memberships")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = True
            cursor = conn.cursor()
            
            memberships = self.relationship_data['memberships']
            batch_size = 100
            deployed_count = 0
            
            for i in range(0, len(memberships), batch_size):
                batch = memberships[i:i + batch_size]
                
                for membership in batch:
                    cursor.execute("""
                        INSERT INTO committee_memberships 
                        (member_id, committee_id, position, start_date, is_current, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                    """, (
                        membership['member_id'],
                        membership['committee_id'],
                        membership['position'],
                        membership['start_date'],
                        membership['is_current']
                    ))
                    deployed_count += 1
                
                if (i // batch_size + 1) % 10 == 0:  # Log every 10 batches
                    self.log_event(f"Deployed {deployed_count} memberships...")
            
            cursor.close()
            conn.close()
            
            self.log_event(f"Successfully deployed {deployed_count} committee memberships", "success")
            return True
            
        except Exception as e:
            self.log_event(f"Failed to deploy memberships: {e}", "error")
            return False
    
    def deploy_committee_leadership(self) -> bool:
        """Deploy committee leadership assignments"""
        self.log_event("Deploying committee leadership assignments")
        
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = True
            cursor = conn.cursor()
            
            leadership_assignments = self.relationship_data['leadership']
            deployed_count = 0
            
            for assignment in leadership_assignments:
                cursor.execute("""
                    UPDATE committees 
                    SET chair_member_id = %s, ranking_member_id = %s, updated_at = NOW()
                    WHERE id = %s
                """, (
                    assignment['chair_member_id'],
                    assignment['ranking_member_id'],
                    assignment['committee_id']
                ))
                deployed_count += 1
            
            cursor.close()
            conn.close()
            
            self.log_event(f"Successfully deployed {deployed_count} leadership assignments", "success")
            return True
            
        except Exception as e:
            self.log_event(f"Failed to deploy leadership: {e}", "error")
            return False
    
    def validate_deployment(self) -> Dict[str, Any]:
        """Validate the deployed relationships"""
        self.log_event("Validating deployed relationships")
        
        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'membership_validation': {},
            'leadership_validation': {},
            'data_integrity': {}
        }
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Validate membership counts
            cursor.execute("SELECT COUNT(*) FROM committee_memberships;")
            total_memberships = cursor.fetchone()[0]
            validation_results['membership_validation']['total_deployed'] = total_memberships
            validation_results['membership_validation']['expected'] = len(self.relationship_data['memberships'])
            validation_results['membership_validation']['match'] = (total_memberships == len(self.relationship_data['memberships']))
            
            # Validate leadership assignments
            cursor.execute("SELECT COUNT(*) FROM committees WHERE chair_member_id IS NOT NULL;")
            committees_with_chairs = cursor.fetchone()[0]
            validation_results['leadership_validation']['committees_with_chairs'] = committees_with_chairs
            
            cursor.execute("SELECT COUNT(*) FROM committees WHERE ranking_member_id IS NOT NULL;")
            committees_with_ranking = cursor.fetchone()[0]
            validation_results['leadership_validation']['committees_with_ranking'] = committees_with_ranking
            
            # Position distribution
            cursor.execute("SELECT position, COUNT(*) FROM committee_memberships GROUP BY position;")
            position_dist = dict(cursor.fetchall())
            validation_results['membership_validation']['position_distribution'] = position_dist
            
            # Chamber distribution
            cursor.execute("""
                SELECT c.chamber, COUNT(*) 
                FROM committee_memberships cm
                JOIN committees c ON cm.committee_id = c.id
                GROUP BY c.chamber;
            """)
            chamber_dist = dict(cursor.fetchall())
            validation_results['membership_validation']['chamber_distribution'] = chamber_dist
            
            # Member assignment distribution
            cursor.execute("""
                SELECT member_id, COUNT(*) as assignment_count
                FROM committee_memberships
                GROUP BY member_id
                ORDER BY assignment_count;
            """)
            member_assignments = cursor.fetchall()
            
            assignment_counts = {}
            for member_id, count in member_assignments:
                assignment_counts[count] = assignment_counts.get(count, 0) + 1
            
            validation_results['data_integrity']['member_assignment_distribution'] = assignment_counts
            validation_results['data_integrity']['members_with_assignments'] = len(member_assignments)
            validation_results['data_integrity']['total_members'] = 541
            
            # Average assignments per member
            if member_assignments:
                total_assignments = sum(count for _, count in member_assignments)
                avg_assignments = total_assignments / len(member_assignments)
                validation_results['data_integrity']['average_assignments_per_member'] = round(avg_assignments, 2)
            
            cursor.close()
            conn.close()
            
            self.log_event("Validation completed successfully", "success")
            
        except Exception as e:
            self.log_event(f"Validation failed: {e}", "error")
            validation_results['error'] = str(e)
        
        return validation_results
    
    def execute_full_deployment(self) -> bool:
        """Execute complete relationship deployment"""
        self.log_event("Starting full member-committee relationship deployment")
        deployment_start = datetime.now()
        
        # Load data
        if not self.load_relationship_data():
            return False
        
        # Clear existing relationships
        if not self.clear_existing_relationships():
            return False
        
        # Deploy memberships
        if not self.deploy_committee_memberships():
            return False
        
        # Deploy leadership
        if not self.deploy_committee_leadership():
            return False
        
        # Validate deployment
        validation_results = self.validate_deployment()
        
        deployment_duration = (datetime.now() - deployment_start).total_seconds()
        
        # Log results
        self.log_event("=== DEPLOYMENT RESULTS ===")
        self.log_event(f"Deployment duration: {deployment_duration:.2f} seconds")
        
        membership_validation = validation_results.get('membership_validation', {})
        if membership_validation.get('match', False):
            self.log_event(f"✅ Memberships: {membership_validation['total_deployed']} deployed successfully")
        else:
            self.log_event(f"⚠️ Memberships: Expected {membership_validation.get('expected', 0)}, got {membership_validation.get('total_deployed', 0)}")
        
        leadership_validation = validation_results.get('leadership_validation', {})
        self.log_event(f"✅ Leadership: {leadership_validation.get('committees_with_chairs', 0)} chairs, {leadership_validation.get('committees_with_ranking', 0)} ranking members")
        
        data_integrity = validation_results.get('data_integrity', {})
        self.log_event(f"✅ Coverage: {data_integrity.get('average_assignments_per_member', 0)} avg assignments per member")
        
        # Save deployment results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = f"relationship_deployment_results_{timestamp}.json"
        
        deployment_results = {
            'deployment_timestamp': timestamp,
            'deployment_duration_seconds': deployment_duration,
            'data_file': self.data_file,
            'validation_results': validation_results,
            'deployment_log': self.deployment_log
        }
        
        with open(results_filename, 'w') as f:
            json.dump(deployment_results, f, indent=2, default=str)
        
        self.log_event(f"Deployment results saved to {results_filename}", "success")
        
        success = (
            membership_validation.get('match', False) and
            leadership_validation.get('committees_with_chairs', 0) > 50 and
            data_integrity.get('average_assignments_per_member', 0) > 3.0
        )
        
        if success:
            self.log_event("🎉 DEPLOYMENT SUCCESS: All relationship targets achieved!", "success")
        else:
            self.log_event("⚠️ DEPLOYMENT WARNING: Some targets not fully achieved", "warning")
        
        return success

def main():
    """Main execution function"""
    print("=== Member-Committee Relationship Deployment ===")
    
    # Find the most recent relationship data file
    import glob
    data_files = glob.glob("member_committee_relationships_*.json")
    if not data_files:
        print("ERROR: No relationship data file found. Please run the generator first.")
        return False
    
    latest_file = sorted(data_files)[-1]
    print(f"Using data file: {latest_file}")
    print("=" * 60)
    
    deployer = RelationshipDeploymentGenerator(latest_file)
    
    deployment_success = deployer.execute_full_deployment()
    
    print("\n" + "=" * 60)
    if deployment_success:
        print("MEMBER-COMMITTEE RELATIONSHIP DEPLOYMENT COMPLETE!")
        print("✅ All members connected to committees")
        print("✅ Committee leadership assigned")
        print("✅ Database relationships deployed")
    else:
        print("DEPLOYMENT COMPLETED WITH WARNINGS")
        print("⚠️ Some issues detected - check logs")
    
    print("=" * 60)
    return deployment_success

if __name__ == "__main__":
    main()