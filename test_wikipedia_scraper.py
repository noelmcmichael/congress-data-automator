#!/usr/bin/env python3

import asyncio
import httpx
from bs4 import BeautifulSoup
import json


async def test_wikipedia_scraper():
    """Test the Wikipedia scraper to see what we can extract."""
    
    url = "https://en.wikipedia.org/wiki/119th_United_States_Congress"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        html = response.text
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for committee tables
    committees = []
    
    # Find all tables on the page
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables on the page")
    
    for i, table in enumerate(tables):
        # Check if this table has committee information
        headers = table.find_all('th')
        if len(headers) >= 3:
            header_text = [th.text.strip() for th in headers]
            print(f"Table {i}: Headers: {header_text}")
            
            # Look for committee-related headers
            if any(keyword in ' '.join(header_text).lower() for keyword in ['committee', 'chair', 'ranking']):
                print(f"  -> This looks like a committee table!")
                
                # Extract committee data
                rows = table.find_all('tr')[1:]  # Skip header row
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        committee_name = cells[0].text.strip()
                        chair = cells[1].text.strip()
                        ranking_member = cells[2].text.strip()
                        
                        # Clean up the names (remove extra formatting)
                        committee_name = committee_name.replace('\n', ' ').strip()
                        chair = chair.replace('\n', ' ').strip()
                        ranking_member = ranking_member.replace('\n', ' ').strip()
                        
                        # Determine chamber based on context
                        chamber = "Unknown"
                        # Look for section headers above this table
                        prev_element = table.find_previous()
                        while prev_element:
                            if prev_element.name in ['h2', 'h3', 'h4']:
                                header_text = prev_element.text.strip()
                                if 'Senate' in header_text:
                                    chamber = "Senate"
                                elif 'House' in header_text:
                                    chamber = "House"
                                elif 'Joint' in header_text:
                                    chamber = "Joint"
                                break
                            prev_element = prev_element.find_previous()
                        
                        committees.append({
                            "name": committee_name,
                            "chamber": chamber,
                            "chair": chair,
                            "ranking_member": ranking_member
                        })
    
    print(f"\nFound {len(committees)} committees:")
    for committee in committees:
        print(f"  {committee['chamber']}: {committee['name']}")
        print(f"    Chair: {committee['chair']}")
        print(f"    Ranking Member: {committee['ranking_member']}")
        print()
    
    # Save to JSON file
    with open('test_wikipedia_data.json', 'w') as f:
        json.dump({"committees": committees}, f, indent=2)
    
    print(f"Data saved to test_wikipedia_data.json")


if __name__ == "__main__":
    asyncio.run(test_wikipedia_scraper())