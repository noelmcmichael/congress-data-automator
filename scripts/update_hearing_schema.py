#!/usr/bin/env python3
"""
Script to update the hearings table schema in production Cloud SQL.
"""
import os
import sys
import asyncio
import keyring
from sqlalchemy import create_engine, text

# Get GCP project secrets
gcp_project_id = "chefgavin"
instance_name = "congressional-db"
database_name = "congress_data"
database_user = "postgres"

# Get database password from keyring
try:
    db_password = keyring.get_password("memex", "GCP_SQL_PASSWORD")
    if not db_password:
        print("Error: Database password not found in keyring")
        sys.exit(1)
except Exception as e:
    print(f"Error accessing keyring: {e}")
    sys.exit(1)

# Construct database URL for Cloud SQL
database_url = f"postgresql://{database_user}:{db_password}@/{database_name}?host=/tmp/cloudsql/{gcp_project_id}:us-central1:{instance_name}"

def update_schema():
    """Update the hearings table schema to increase column lengths."""
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                print("Checking current schema...")
                
                # Check current column definitions
                result = conn.execute(text("""
                    SELECT column_name, character_maximum_length, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'hearings' AND column_name IN ('location', 'room')
                    ORDER BY column_name
                """))
                
                current_defs = result.fetchall()
                print("Current column definitions:")
                for col in current_defs:
                    print(f"  - {col[0]}: {col[2]}({col[1]})")
                
                # Update location column
                print("\nUpdating location column from VARCHAR(255) to VARCHAR(1000)...")
                conn.execute(text("""
                    ALTER TABLE hearings 
                    ALTER COLUMN location TYPE VARCHAR(1000)
                """))
                
                # Update room column
                print("Updating room column from VARCHAR(100) to VARCHAR(500)...")
                conn.execute(text("""
                    ALTER TABLE hearings 
                    ALTER COLUMN room TYPE VARCHAR(500)
                """))
                
                trans.commit()
                print("✅ Schema update completed successfully!")
                
                # Verify the changes
                result = conn.execute(text("""
                    SELECT column_name, character_maximum_length, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'hearings' AND column_name IN ('location', 'room')
                    ORDER BY column_name
                """))
                
                updated_defs = result.fetchall()
                print("\nUpdated column definitions:")
                for col in updated_defs:
                    print(f"  - {col[0]}: {col[2]}({col[1]})")
                
            except Exception as e:
                trans.rollback()
                print(f"❌ Error during schema update: {e}")
                raise
                
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        raise

if __name__ == '__main__':
    print("Updating hearing schema in Cloud SQL...")
    print(f"Target database: {gcp_project_id}:us-central1:{instance_name}/{database_name}")
    print("=" * 60)
    
    update_schema()