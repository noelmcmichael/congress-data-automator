#!/usr/bin/env python3
"""
Test the data reconciliation service
"""
import os
import sys
sys.path.append('backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.services.data_reconciler import DataReconciler

def test_reconciliation():
    """Test the data reconciliation with imported data"""
    
    # Connect to PostgreSQL
    db_url = os.getenv('DATABASE_URL', 'postgresql://noelmcmichael@127.0.0.1:5432/congress_data')
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        print("🔄 Testing data reconciliation...")
        
        # Create reconciler
        reconciler = DataReconciler(session)
        
        # Run reconciliation
        results = reconciler.reconcile_leadership()
        
        # Print results
        print(f"\n📊 Reconciliation Results:")
        print(f"   Member matches: {len(results['member_matches'])}")
        print(f"   Committee matches: {len(results['committee_matches'])}")
        print(f"   Leadership updates: {len(results['leadership_updates'])}")
        print(f"   Errors: {len(results['errors'])}")
        
        # Show member matches
        if results['member_matches']:
            print(f"\n👥 Member Matches:")
            for match in results['member_matches'][:10]:  # Show first 10
                print(f"   ✅ {match['wikipedia_name']} -> {match['database_name']} ({match['role']}) at {match['committee']}")
        
        # Show committee matches
        if results['committee_matches']:
            print(f"\n📋 Committee Matches:")
            for match in results['committee_matches'][:10]:  # Show first 10
                print(f"   ✅ {match['wikipedia_name']} -> {match['database_name']} ({match['chamber']})")
        
        # Show leadership updates
        if results['leadership_updates']:
            print(f"\n🔄 Leadership Updates:")
            for update in results['leadership_updates']:
                print(f"   📝 {update['committee_name']}: {update['position']} -> {update['new_member_name']} (ID: {update['new_member_id']})")
        
        # Show errors
        if results['errors']:
            print(f"\n❌ Errors:")
            for error in results['errors']:
                print(f"   🚨 {error}")
        
        # Generate SQL
        sql_statements = reconciler.generate_update_sql()
        if sql_statements:
            print(f"\n📜 Generated {len(sql_statements)} SQL statements:")
            for i, sql in enumerate(sql_statements[:5], 1):  # Show first 5
                print(f"   {i}. {sql}")
            
            # Save SQL statements
            with open("leadership_updates.sql", "w") as f:
                for sql in sql_statements:
                    f.write(sql + "\n")
            print(f"   💾 SQL statements saved to leadership_updates.sql")
        
        # Save full results
        reconciler.save_results("reconciliation_results.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Reconciliation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()

if __name__ == "__main__":
    success = test_reconciliation()
    sys.exit(0 if success else 1)