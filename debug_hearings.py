#!/usr/bin/env python3
"""
Debug script to check hearing data for string length violations.
"""
import asyncio
import os
import sys
sys.path.append('backend')

# Set required environment variables
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['SECRET_KEY'] = 'test'

# Get the actual Congress API key from keyring
import keyring
congress_api_key = keyring.get_password("memex", "CONGRESS_API_KEY")
if congress_api_key:
    os.environ['CONGRESS_API_KEY'] = congress_api_key
else:
    print("Warning: Congress API key not found in keyring")
    os.environ['CONGRESS_API_KEY'] = 'test'

from backend.app.services.data_processor import DataProcessor

async def debug_hearing_data():
    print("Testing hearing data for string length violations...")
    
    processor = DataProcessor()
    
    # Get hearings from API
    hearings_api = await processor.congress_api.get_hearings()
    print(f'Congress API hearings: {len(hearings_api)}')
    
    # Get hearings from scrapers
    house_hearings = await processor.house_scraper.scrape_hearings()
    senate_hearings = await processor.senate_scraper.scrape_hearings()
    print(f'House hearings: {len(house_hearings)}')
    print(f'Senate hearings: {len(senate_hearings)}')
    
    all_hearings = hearings_api + house_hearings + senate_hearings
    print(f'Total hearings: {len(all_hearings)}')
    
    # Check for long values
    violations = []
    for i, hearing in enumerate(all_hearings):
        title = hearing.get('title', '')
        location = hearing.get('location', '')
        description = hearing.get('description', '')
        
        if len(title) > 500:
            violations.append(f'Hearing {i}: Title too long ({len(title)} chars): {title[:100]}...')
        if len(location) > 255:
            violations.append(f'Hearing {i}: Location too long ({len(location)} chars): {location[:100]}...')
        if isinstance(description, str) and len(description) > 1000:
            violations.append(f'Hearing {i}: Description too long ({len(description)} chars): {description[:100]}...')
    
    if violations:
        print(f"\nFound {len(violations)} violations:")
        for violation in violations:
            print(f"  - {violation}")
    else:
        print("\nNo string length violations found!")
    
    # Print some sample data to debug
    print("\nSample hearing data:")
    for i, hearing in enumerate(all_hearings[:5]):
        title = hearing.get('title', '')
        location = hearing.get('location', '')
        print(f"  {i}: Title({len(title)}): {title}")
        print(f"     Location({len(location)}): {location}")
        print()

if __name__ == '__main__':
    asyncio.run(debug_hearing_data())