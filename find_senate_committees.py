#!/usr/bin/env python3
"""
Find actual Senate committee pages with member information
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def find_senate_committee_pages():
    """Find actual Senate committee pages"""
    print("🔍 Finding Senate Committee Pages...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Try different approaches to find committee pages
    potential_urls = [
        "https://www.senate.gov/committees/index.htm",
        "https://www.senate.gov/committees/",
        "https://www.senate.gov/committees/committee_home.htm",
        "https://www.senate.gov/committees/committee-list.htm",
        "https://www.senate.gov/committees/committees.htm"
    ]
    
    for url in potential_urls:
        print(f"\n🔗 Trying: {url}")
        try:
            response = session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                print(f"✅ Success! Title: {soup.title.string if soup.title else 'No title'}")
                
                # Look for committee links
                links = soup.find_all('a', href=True)
                committee_links = []
                
                for link in links:
                    href = link['href']
                    text = link.get_text().strip()
                    
                    # Look for committee-related links
                    if ('committee' in href.lower() or 
                        any(term in text.lower() for term in ['judiciary', 'armed services', 'agriculture', 'finance', 'appropriations'])):
                        committee_links.append({
                            'text': text,
                            'href': href,
                            'full_url': href if href.startswith('http') else f"https://www.senate.gov{href}"
                        })
                
                if committee_links:
                    print(f"📋 Found {len(committee_links)} potential committee links:")
                    for link in committee_links[:10]:  # Show first 10
                        print(f"  - {link['text'][:50]}... → {link['href']}")
                    
                    return committee_links
                else:
                    print("❌ No committee links found")
                    
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return []

def test_direct_committee_approach():
    """Test direct approach to known committee pages"""
    print("\n🎯 Testing Direct Committee Approach...")
    
    # Try some known committee names that might have direct pages
    committee_names = [
        "judiciary",
        "armed-services", 
        "agriculture",
        "finance",
        "appropriations",
        "foreign-relations",
        "health-education-labor-pensions",
        "homeland-security-governmental-affairs"
    ]
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    working_urls = []
    
    for committee in committee_names:
        # Try different URL patterns
        url_patterns = [
            f"https://www.senate.gov/committees/{committee}.htm",
            f"https://www.senate.gov/committees/{committee}/",
            f"https://www.senate.gov/committees/{committee}/index.htm",
            f"https://www.senate.gov/committees/{committee}/members.htm",
            f"https://www.senate.gov/committees/{committee}/roster.htm"
        ]
        
        print(f"\n🔍 Testing {committee} committee...")
        
        for url in url_patterns:
            try:
                response = session.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.title.string if soup.title else "No title"
                    
                    # Check if it's a real committee page (not 404 or generic)
                    if ('404' not in title and 
                        'error' not in title.lower() and
                        len(soup.get_text()) > 1000):  # Substantial content
                        print(f"✅ Found working URL: {url}")
                        print(f"   Title: {title}")
                        
                        working_urls.append({
                            'committee': committee,
                            'url': url,
                            'title': title
                        })
                        break
                    else:
                        print(f"❌ Not a valid committee page: {url}")
                else:
                    print(f"❌ {response.status_code}: {url}")
                    
            except Exception as e:
                print(f"❌ Error testing {url}: {e}")
    
    return working_urls

def check_congress_gov_committees():
    """Check Congress.gov for committee information"""
    print("\n🏛️ Checking Congress.gov for committee information...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Congress.gov committee pages
    congress_urls = [
        "https://www.congress.gov/committees/senate",
        "https://www.congress.gov/committees/senate/119th-congress",
        "https://www.congress.gov/committees"
    ]
    
    for url in congress_urls:
        print(f"\n🔗 Trying Congress.gov: {url}")
        try:
            response = session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                print(f"✅ Success! Title: {soup.title.string if soup.title else 'No title'}")
                
                # Look for committee links
                links = soup.find_all('a', href=True)
                committee_links = []
                
                for link in links:
                    href = link['href']
                    text = link.get_text().strip()
                    
                    if ('committee' in href.lower() and 
                        'senate' in href.lower() and
                        len(text) > 5):
                        committee_links.append({
                            'text': text,
                            'href': href,
                            'full_url': href if href.startswith('http') else f"https://www.congress.gov{href}"
                        })
                
                if committee_links:
                    print(f"📋 Found {len(committee_links)} Congress.gov committee links:")
                    for link in committee_links[:10]:
                        print(f"  - {link['text'][:50]}... → {link['href']}")
                    
                    return committee_links
                    
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return []

def main():
    """Main function to find working committee pages"""
    print("🏛️ Finding Senate Committee Pages")
    print("=" * 50)
    
    all_results = {}
    
    # Method 1: Try to find main committee index
    print("\n📋 METHOD 1: Finding Committee Index Pages")
    committee_links = find_senate_committee_pages()
    if committee_links:
        all_results['senate_gov_links'] = committee_links
    
    # Method 2: Try direct committee URLs
    print("\n📋 METHOD 2: Testing Direct Committee URLs")
    working_urls = test_direct_committee_approach()
    if working_urls:
        all_results['direct_urls'] = working_urls
    
    # Method 3: Check Congress.gov
    print("\n📋 METHOD 3: Checking Congress.gov")
    congress_links = check_congress_gov_committees()
    if congress_links:
        all_results['congress_gov_links'] = congress_links
    
    # Save results
    results_file = f"senate_committee_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Summary
    print(f"\n🎯 SEARCH SUMMARY")
    print(f"Senate.gov links found: {len(all_results.get('senate_gov_links', []))}")
    print(f"Direct URLs working: {len(all_results.get('direct_urls', []))}")
    print(f"Congress.gov links found: {len(all_results.get('congress_gov_links', []))}")
    
    if any(all_results.values()):
        print("\n✅ SUCCESS: Found working committee page sources")
        print("Next step: Test scraping member information from these pages")
    else:
        print("\n❌ No working committee pages found")
        print("May need to try alternative approaches or use Congress.gov API")

if __name__ == "__main__":
    main()