#!/usr/bin/env python3
"""
Analyze Senate committee page structure to understand how to scrape member information
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def analyze_senate_committee_page(url: str, committee_name: str):
    """Analyze structure of a Senate committee page"""
    print(f"🔍 Analyzing {committee_name} committee page...")
    print(f"URL: {url}")
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        response = session.get(url)
        if response.status_code != 200:
            print(f"❌ Failed to fetch page: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Analyze page structure
        print(f"\n📋 Page Title: {soup.title.string if soup.title else 'No title'}")
        
        # Look for common patterns
        print("\n🔍 Looking for member-related elements...")
        
        # Check for common member-related terms
        member_terms = ['member', 'chair', 'ranking', 'senator', 'committee']
        
        for term in member_terms:
            # Find elements containing the term
            elements = soup.find_all(string=lambda text: text and term.lower() in text.lower())
            if elements:
                print(f"\n📌 Found {len(elements)} elements containing '{term}':")
                for element in elements[:3]:  # Show first 3
                    parent = element.parent
                    tag_info = f"<{parent.name}>" if parent else "text"
                    print(f"  {tag_info}: {str(element).strip()[:80]}...")
        
        # Check for tables (common for member listings)
        tables = soup.find_all('table')
        if tables:
            print(f"\n📊 Found {len(tables)} tables:")
            for i, table in enumerate(tables):
                print(f"  Table {i+1}: {len(table.find_all('tr'))} rows")
                # Show first few rows
                rows = table.find_all('tr')
                for j, row in enumerate(rows[:2]):
                    cells = row.find_all(['td', 'th'])
                    cell_text = [cell.get_text().strip() for cell in cells]
                    print(f"    Row {j+1}: {cell_text}")
        
        # Check for lists (ul, ol)
        lists = soup.find_all(['ul', 'ol'])
        if lists:
            print(f"\n📝 Found {len(lists)} lists:")
            for i, list_elem in enumerate(lists):
                items = list_elem.find_all('li')
                print(f"  List {i+1}: {len(items)} items")
                for j, item in enumerate(items[:2]):
                    print(f"    Item {j+1}: {item.get_text().strip()[:80]}...")
        
        # Look for div sections that might contain member info
        divs = soup.find_all('div')
        member_divs = []
        
        for div in divs:
            div_text = div.get_text().lower()
            if any(term in div_text for term in ['member', 'chair', 'ranking']):
                member_divs.append(div)
        
        if member_divs:
            print(f"\n🏛️ Found {len(member_divs)} divs with member-related content:")
            for i, div in enumerate(member_divs[:3]):
                print(f"  Div {i+1}: {div.get_text().strip()[:100]}...")
        
        # Save full page content for analysis
        page_content = {
            'url': url,
            'committee': committee_name,
            'title': soup.title.string if soup.title else None,
            'html_content': str(soup),
            'text_content': soup.get_text(),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return page_content
        
    except Exception as e:
        print(f"❌ Error analyzing page: {e}")
        return None

def test_multiple_senate_committees():
    """Test multiple Senate committee pages to find patterns"""
    
    # Test different Senate committee pages
    test_committees = [
        {
            'name': 'Judiciary',
            'url': 'https://www.senate.gov/committees/judiciary.htm'
        },
        {
            'name': 'Armed Services',
            'url': 'https://www.senate.gov/committees/armed-services.htm'
        },
        {
            'name': 'Agriculture',
            'url': 'https://www.senate.gov/committees/agriculture-nutrition-and-forestry.htm'
        }
    ]
    
    results = []
    
    for committee in test_committees:
        print("=" * 60)
        result = analyze_senate_committee_page(committee['url'], committee['name'])
        if result:
            results.append(result)
    
    # Save results
    results_file = f"senate_structure_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Analysis results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    print("🏛️ Senate Committee Structure Analysis")
    print("=" * 50)
    
    results = test_multiple_senate_committees()
    
    print(f"\n🎯 ANALYSIS COMPLETE")
    print(f"Analyzed {len(results)} committee pages")
    print("\n📋 NEXT STEPS:")
    print("1. Review saved analysis files")
    print("2. Identify common patterns for member listings")
    print("3. Update scraping strategy based on findings")
    print("4. Test improved scraping approach")