"""
Database migration to fix hearing location field length.
"""
import asyncio
from sqlalchemy import create_engine, text
from ..core.config import settings

async def migrate_hearing_location_length():
    """
    Increase the location field length in hearings table to accommodate longer descriptions.
    """
    engine = create_engine(settings.database_url)
    
    try:
        with engine.connect() as conn:
            # Start a transaction
            trans = conn.begin()
            
            try:
                # Check current column definition
                result = conn.execute(text("""
                    SELECT column_name, character_maximum_length, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'hearings' AND column_name = 'location'
                """))
                
                current_def = result.fetchone()
                if current_def:
                    print(f"Current location column: {current_def}")
                    
                    # Update column length from 255 to 1000
                    conn.execute(text("""
                        ALTER TABLE hearings 
                        ALTER COLUMN location TYPE VARCHAR(1000)
                    """))
                    
                    print("Successfully increased location column length to 1000 characters")
                else:
                    print("Location column not found in hearings table")
                
                # Also check if we need to increase room column
                result = conn.execute(text("""
                    SELECT column_name, character_maximum_length, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'hearings' AND column_name = 'room'
                """))
                
                room_def = result.fetchone()
                if room_def:
                    print(f"Current room column: {room_def}")
                    
                    # Update room column length from 100 to 500
                    conn.execute(text("""
                        ALTER TABLE hearings 
                        ALTER COLUMN room TYPE VARCHAR(500)
                    """))
                    
                    print("Successfully increased room column length to 500 characters")
                
                # Commit the transaction
                trans.commit()
                print("Migration completed successfully")
                
            except Exception as e:
                trans.rollback()
                print(f"Error during migration: {e}")
                raise
                
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(migrate_hearing_location_length())