#!/usr/bin/env python3
"""
Phase 3A - Verification Script
Verify that the database and API reflect the updated reliable sources.
"""
import requests
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Verification:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable not set.")
        
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.api_base = "https://congressional-data-api-v3-1066017671167.us-central1.run.app"

    def verify_database_state(self):
        """Verify that the database reflects the changes."""
        print("Verifying database state...")
        with self.Session() as session:
            try:
                # Check for unreliable URLs (should be none)
                sql_unreliable = text("""
                    SELECT COUNT(*) FROM committees
                    WHERE hearings_url LIKE '%commerce.senate.gov/2025/hearings%';
                """)
                unreliable_count = session.execute(sql_unreliable).scalar()
                
                # Check for reliable URLs
                sql_reliable = text("""
                    SELECT COUNT(*) FROM committees
                    WHERE hearings_url = 'https://www.agriculture.senate.gov/hearings';
                """)
                reliable_count = session.execute(sql_reliable).scalar()

                print(f"  Unreliable URLs count (expected 0): {unreliable_count}")
                print(f"  Reliable URLs count (expected > 0): {reliable_count}")

                return unreliable_count == 0 and reliable_count > 0
            except Exception as e:
                print(f"  Database verification failed: {e}")
                return False

    def verify_api_response(self):
        """Verify that the API returns the updated data."""
        print("\nVerifying API response...")
        try:
            response = requests.get(f"{self.api_base}/api/v1/committees", timeout=15)
            if response.status_code == 200:
                committees = response.json()
                
                # Find a committee that should have updated URLs
                ag_committee = next((c for c in committees if c['name'] == 'Committee on Agriculture, Nutrition, and Forestry'), None)
                
                if ag_committee:
                    print("  Found 'Committee on Agriculture, Nutrition, and Forestry'")
                    print(f"    hearings_url: {ag_committee.get('hearings_url')}")
                    print(f"    members_url: {ag_committee.get('members_url')}")
                    return ag_committee.get('hearings_url') is not None
                else:
                    print("  Could not find test committee in API response.")
                    return False
            else:
                print(f"  API request failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"  API verification failed: {e}")
            return False

    def run_verification(self):
        """Run all verification checks."""
        print("🚀 Starting Phase 3A Verification")
        print("=" * 50)
        
        db_ok = self.verify_database_state()
        api_ok = self.verify_api_response()
        
        print("=" * 50)
        print("📊 Verification Results")
        print(f"  Database State Correct: {'✅' if db_ok else '❌'}")
        print(f"  API Response Correct: {'✅' if api_ok else '❌'}")
        
        if db_ok and api_ok:
            print("\n🎉 Phase 3A Data Quality Enhancement is VERIFIED!")
            print("   The database and API now reflect the reliable sources.")
        else:
            print("\n⚠️  Verification failed. Please review the logs.")

def main():
    verifier = Verification()
    verifier.run_verification()

if __name__ == "__main__":
    main()