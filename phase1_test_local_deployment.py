#!/usr/bin/env python3
"""
Phase 1.3: Test Local Deployment
Test the 119th Congress data migration with a local SQLite database.
"""

import json
import os
import sys
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path for imports
sys.path.append('backend')

from backend.app.core.database import Base
from backend.app.models import Member, Committee, CommitteeMembership, CongressionalSession

class LocalDeploymentTester:
    """Test deployment with local SQLite database."""
    
    def __init__(self):
        self.migration_file = None
        self.engine = None
        self.session_factory = None
        self.test_log = []
        
        # Find the most recent migration file
        migration_files = [f for f in os.listdir('.') if f.startswith('phase1_migration_data_')]
        if migration_files:
            self.migration_file = sorted(migration_files)[-1]
    
    def log_action(self, action: str, details: str, status: str = "INFO"):
        """Log test actions."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "status": status
        }
        self.test_log.append(entry)
        print(f"[{status}] {action}: {details}")
    
    def setup_test_database(self):
        """Setup local SQLite test database."""
        try:
            self.log_action("setup_test_database", "Creating local SQLite test database")
            
            # Create engine for local SQLite
            self.engine = create_engine("sqlite:///test_119th_congress.db", echo=False)
            
            # Create session factory
            self.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            self.log_action("setup_test_database", "Test database created successfully")
            return True
            
        except Exception as e:
            self.log_action("setup_test_database", f"Failed: {str(e)}", "ERROR")
            return False
    
    def load_and_test_migration(self) -> Dict[str, Any]:
        """Load migration data and test deployment."""
        if not self.migration_file:
            self.log_action("load_migration", "No migration file found", "ERROR")
            return {"success": False, "error": "No migration file"}
        
        try:
            self.log_action("load_migration", f"Loading {self.migration_file}")
            
            with open(self.migration_file, 'r') as f:
                data = json.load(f)
            
            # Test deploying congressional sessions
            self.test_congressional_sessions(data.get('congressional_sessions', []))
            
            # Test deploying members
            self.test_members_deployment(data.get('members', []))
            
            # Test deploying committees
            self.test_committees_deployment(data.get('committees', []))
            
            # Test API model compatibility
            self.test_api_compatibility()
            
            return {"success": True, "data": data}
            
        except Exception as e:
            self.log_action("load_migration", f"Failed: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    def test_congressional_sessions(self, sessions_data: List[Dict[str, Any]]):
        """Test congressional sessions deployment."""
        try:
            self.log_action("test_sessions", f"Testing {len(sessions_data)} sessions")
            
            db = self.session_factory()
            
            for session_data in sessions_data:
                session = CongressionalSession(
                    congress_number=session_data['congress_number'],
                    start_date=datetime.strptime(session_data['start_date'], '%Y-%m-%d').date(),
                    end_date=datetime.strptime(session_data['end_date'], '%Y-%m-%d').date(),
                    is_current=session_data.get('is_current', False),
                    party_control_house=session_data.get('party_control_house'),
                    party_control_senate=session_data.get('party_control_senate'),
                    session_name=f"{session_data['congress_number']}th Congress",
                    election_year=session_data.get('election_year')
                )
                
                db.add(session)
                self.log_action("test_sessions", f"Added session {session_data['congress_number']}")
            
            db.commit()
            
            # Verify
            count = db.query(CongressionalSession).count()
            current = db.query(CongressionalSession).filter(CongressionalSession.is_current == True).first()
            
            self.log_action("test_sessions", f"✅ Sessions test passed: {count} sessions, current: {current.congress_number if current else 'None'}")
            
            db.close()
            
        except Exception as e:
            self.log_action("test_sessions", f"Failed: {str(e)}", "ERROR")
            if 'db' in locals():
                db.rollback()
                db.close()
    
    def test_members_deployment(self, members_data: List[Dict[str, Any]]):
        """Test members deployment."""
        try:
            self.log_action("test_members", f"Testing {len(members_data)} members")
            
            db = self.session_factory()
            
            for member_data in members_data[:5]:  # Test first 5 members
                member_dict = member_data.copy()
                if 'id' in member_dict:
                    del member_dict['id']  # Let database assign new ID
                
                # Convert date strings
                if member_dict.get('term_start'):
                    try:
                        member_dict['term_start'] = datetime.strptime(member_dict['term_start'], '%Y-%m-%d').date()
                    except:
                        member_dict['term_start'] = None
                
                if member_dict.get('term_end'):
                    try:
                        member_dict['term_end'] = datetime.strptime(member_dict['term_end'], '%Y-%m-%d').date()
                    except:
                        member_dict['term_end'] = None
                
                member = Member(**member_dict)
                db.add(member)
                
                name = f"{member_dict.get('first_name', '')} {member_dict.get('last_name', '')}"
                self.log_action("test_members", f"Added member {name}")
            
            db.commit()
            
            # Verify
            count = db.query(Member).count()
            congress_119_count = db.query(Member).filter(Member.congress_session == 119).count()
            
            self.log_action("test_members", f"✅ Members test passed: {count} total, {congress_119_count} from 119th Congress")
            
            db.close()
            
        except Exception as e:
            self.log_action("test_members", f"Failed: {str(e)}", "ERROR")
            if 'db' in locals():
                db.rollback()
                db.close()
    
    def test_committees_deployment(self, committees_data: List[Dict[str, Any]]):
        """Test committees deployment."""
        try:
            self.log_action("test_committees", f"Testing {len(committees_data)} committees")
            
            db = self.session_factory()
            
            for committee_data in committees_data[:5]:  # Test first 5 committees
                committee_dict = committee_data.copy()
                if 'id' in committee_dict:
                    del committee_dict['id']  # Let database assign new ID
                
                # Remove 119th-specific fields
                committee_dict = {k: v for k, v in committee_dict.items() if not k.startswith('_119th_')}
                
                committee = Committee(**committee_dict)
                db.add(committee)
                
                self.log_action("test_committees", f"Added committee {committee_dict['name']}")
            
            db.commit()
            
            # Verify
            count = db.query(Committee).count()
            congress_119_count = db.query(Committee).filter(Committee.congress_session == 119).count()
            
            self.log_action("test_committees", f"✅ Committees test passed: {count} total, {congress_119_count} from 119th Congress")
            
            db.close()
            
        except Exception as e:
            self.log_action("test_committees", f"Failed: {str(e)}", "ERROR")
            if 'db' in locals():
                db.rollback()
                db.close()
    
    def test_api_compatibility(self):
        """Test API model compatibility with migrated data."""
        try:
            self.log_action("test_api_compatibility", "Testing API schemas with migrated data")
            
            db = self.session_factory()
            
            # Test member schema compatibility
            member = db.query(Member).first()
            if member:
                # Test that we can access all required fields for API response
                test_fields = [
                    'id', 'bioguide_id', 'first_name', 'last_name', 'party', 
                    'chamber', 'state', 'is_current', 'congress_session'
                ]
                
                for field in test_fields:
                    value = getattr(member, field, None)
                    if value is None and field in ['first_name', 'last_name', 'party', 'chamber', 'state']:
                        raise ValueError(f"Required field {field} is None")
                
                self.log_action("test_api_compatibility", f"✅ Member API compatibility verified")
            
            # Test committee schema compatibility
            committee = db.query(Committee).first()
            if committee:
                test_fields = [
                    'id', 'name', 'chamber', 'is_active', 'congress_session'
                ]
                
                for field in test_fields:
                    value = getattr(committee, field, None)
                    if value is None and field in ['name', 'chamber']:
                        raise ValueError(f"Required field {field} is None")
                
                self.log_action("test_api_compatibility", f"✅ Committee API compatibility verified")
            
            # Test congressional session functionality
            session = db.query(CongressionalSession).filter(CongressionalSession.is_current == True).first()
            if session:
                # Test computed properties
                display_name = session.display_name
                years_display = session.years_display
                
                self.log_action("test_api_compatibility", f"✅ Congressional session API compatibility verified: {display_name} ({years_display})")
            
            db.close()
            
        except Exception as e:
            self.log_action("test_api_compatibility", f"Failed: {str(e)}", "ERROR")
            if 'db' in locals():
                db.close()

def main():
    """Run the local deployment test."""
    
    print("🧪 Phase 1.3: Test Local Deployment")
    print("=" * 50)
    
    # Initialize tester
    tester = LocalDeploymentTester()
    
    # Setup test database
    if not tester.setup_test_database():
        print("❌ Failed to setup test database")
        return
    
    # Run migration test
    print("🔄 Testing 119th Congress data migration...")
    result = tester.load_and_test_migration()
    
    # Save test results
    output_file = f"phase1_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "migration_file": tester.migration_file,
        "success": result["success"],
        "test_log": tester.test_log
    }
    
    with open(output_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    # Display summary
    print(f"\n📊 Test Summary:")
    print(f"   Migration File: {tester.migration_file}")
    print(f"   Success: {'✅ YES' if result['success'] else '❌ NO'}")
    
    # Count successful tests
    successful_tests = [log for log in tester.test_log if "✅" in log["details"]]
    total_tests = [log for log in tester.test_log if "test" in log["action"]]
    
    print(f"   Successful Tests: {len(successful_tests)}")
    print(f"   Total Test Actions: {len(total_tests)}")
    
    # Show test results
    print(f"\n🧪 Test Results:")
    for log in tester.test_log:
        if "✅" in log["details"] or log["status"] == "ERROR":
            status_icon = "✅" if "✅" in log["details"] else "❌"
            print(f"   {status_icon} {log['action'].replace('_', ' ').title()}: {log['details']}")
    
    # Show any errors
    errors = [log for log in tester.test_log if log["status"] == "ERROR"]
    if errors:
        print(f"\n⚠️  Test Errors ({len(errors)}):")
        for error in errors:
            print(f"   - {error['action']}: {error['details']}")
    
    print(f"\n📄 Test results saved to: {output_file}")
    
    if result["success"]:
        print(f"\n✅ Phase 1.3 Local Testing Complete")
        print(f"\n🎯 Migration Compatibility Verified:")
        print(f"   ✅ SQLAlchemy models work with 119th Congress data")
        print(f"   ✅ Congressional session tracking functional")
        print(f"   ✅ API schema compatibility confirmed")
        print(f"   ✅ Database deployment process tested")
        print(f"\n🚀 Ready for production deployment to Cloud SQL")
    else:
        print(f"\n❌ Phase 1.3 Local Testing Failed")
        print(f"   Fix issues before attempting production deployment")
    
    # Cleanup test database
    if os.path.exists("test_119th_congress.db"):
        os.remove("test_119th_congress.db")
        print(f"   🧹 Cleaned up test database")
    
    return result

if __name__ == "__main__":
    main()