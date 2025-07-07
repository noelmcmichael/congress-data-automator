#!/usr/bin/env python3
"""
Phase 3A - Update Database with Reliable Sources
This script updates the database by:
1. Loading the list of operational (reliable) sources.
2. Setting all committee URL fields to NULL.
3. Populating the URL fields with the reliable sources.
"""
import json
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseUpdater:
    def __init__(self, operational_sources_file):
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable not set.")
        
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.operational_sources = self.load_operational_sources(operational_sources_file)

    def load_operational_sources(self, filepath: str) -> list:
        """Load the list of reliable URLs from the JSON file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Operational sources file not found at {filepath}")
            return []

    def clear_all_committee_urls(self):
        """Set all URL fields in the committees table to NULL."""
        print("Clearing all existing committee URLs from the database...")
        with self.Session() as session:
            try:
                sql = text("""
                    UPDATE committees
                    SET 
                        hearings_url = NULL,
                        members_url = NULL,
                        official_website_url = NULL,
                        last_url_update = NULL;
                """)
                result = session.execute(sql)
                session.commit()
                print(f"Successfully cleared URLs for {result.rowcount} committees.")
                return True
            except Exception as e:
                session.rollback()
                print(f"Error clearing committee URLs: {e}")
                return False

    def update_database_with_reliable_sources(self):
        """Update the database with the reliable URLs."""
        if not self.operational_sources:
            print("No operational sources to update.")
            return

        print(f"Updating database with {len(self.operational_sources)} reliable URLs...")
        updated_committees = set()
        
        with self.Session() as session:
            try:
                for source in self.operational_sources:
                    committee_name = source.get("committee")
                    url_type = source.get("url_type")
                    url = source.get("url")
                    last_validated = source.get("last_validated")

                    if not all([committee_name, url_type, url]):
                        continue

                    sql = text(f"""
                        UPDATE committees
                        SET {url_type} = :url, last_url_update = :last_validated
                        WHERE name = :committee_name;
                    """)
                    
                    params = {
                        "url": url,
                        "last_validated": last_validated,
                        "committee_name": committee_name
                    }
                    
                    result = session.execute(sql, params)
                    if result.rowcount > 0:
                        updated_committees.add(committee_name)

                session.commit()
                print(f"Successfully updated {len(updated_committees)} committees with reliable URLs.")
                return True
            except Exception as e:
                session.rollback()
                print(f"Error updating database: {e}")
                return False

    def run_update(self):
        """Execute the full database update process."""
        print("🚀 Starting Phase 3A Database Update Process")
        print("=" * 50)
        
        if self.clear_all_committee_urls():
            self.update_database_with_reliable_sources()
            
        print("=" * 50)
        print("✅ Database update process complete.")


def main():
    # Find the latest operational sources file
    files = [f for f in os.listdir('.') if f.startswith('operational_sources_') and f.endswith('.json')]
    if not files:
        print("No operational sources file found. Please run the analysis script first.")
        return
        
    latest_file = sorted(files, reverse=True)[0]
    print(f"Using latest operational sources file: {latest_file}")
    
    updater = DatabaseUpdater(latest_file)
    updater.run_update()

if __name__ == "__main__":
    main()