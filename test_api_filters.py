#!/usr/bin/env python3
"""
Test API filter functionality directly
"""
import requests
import json

# API base URL
BASE_URL = "https://congressional-data-api-v2-1066017671167.us-central1.run.app/api/v1"

def test_api_filters():
    """Test various API filter combinations"""
    print("Testing Congressional Data API Filters")
    print("="*50)
    
    # Test cases with expected results based on database inspection
    test_cases = [
        # Basic query (should return 538 members)
        {"endpoint": "members", "params": {}, "expected_desc": "All members (538)"},
        
        # Party filters
        {"endpoint": "members", "params": {"party": "Republican"}, "expected_desc": "Republican members"},
        {"endpoint": "members", "params": {"party": "Democratic"}, "expected_desc": "Democratic members"},
        {"endpoint": "members", "params": {"party": "Independent"}, "expected_desc": "Independent members"},
        {"endpoint": "members", "params": {"party": "INVALID"}, "expected_desc": "Invalid party (should be 0)"},
        
        # Chamber filters - testing both cases
        {"endpoint": "members", "params": {"chamber": "house"}, "expected_desc": "House members (lowercase)"},
        {"endpoint": "members", "params": {"chamber": "House"}, "expected_desc": "House members (capitalized)"},
        {"endpoint": "members", "params": {"chamber": "senate"}, "expected_desc": "Senate members (lowercase)"},
        {"endpoint": "members", "params": {"chamber": "Senate"}, "expected_desc": "Senate members (capitalized)"},
        
        # State filters
        {"endpoint": "members", "params": {"state": "CA"}, "expected_desc": "California members"},
        {"endpoint": "members", "params": {"state": "NY"}, "expected_desc": "New York members"},
        {"endpoint": "members", "params": {"state": "XX"}, "expected_desc": "Invalid state (should be 0)"},
        
        # Combined filters
        {"endpoint": "members", "params": {"party": "Democratic", "state": "CA"}, "expected_desc": "Democratic California members"},
        {"endpoint": "members", "params": {"party": "Republican", "chamber": "House"}, "expected_desc": "Republican House members"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['expected_desc']}")
        
        # Make API request
        url = f"{BASE_URL}/{test_case['endpoint']}"
        try:
            response = requests.get(url, params=test_case['params'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data)
                print(f"   Status: ✅ SUCCESS")
                print(f"   Results: {count} items")
                print(f"   URL: {response.url}")
                
                # Show sample data for first few results
                if count > 0 and count <= 3:
                    print("   Sample data:")
                    for item in data[:3]:
                        if 'first_name' in item and 'last_name' in item:
                            print(f"     - {item.get('first_name', '')} {item.get('last_name', '')}, "
                                  f"Party: {item.get('party', 'N/A')}, "
                                  f"Chamber: {item.get('chamber', 'N/A')}, "
                                  f"State: {item.get('state', 'N/A')}")
                elif count > 3:
                    print(f"   Sample data (first 3 of {count}):")
                    for item in data[:3]:
                        if 'first_name' in item and 'last_name' in item:
                            print(f"     - {item.get('first_name', '')} {item.get('last_name', '')}, "
                                  f"Party: {item.get('party', 'N/A')}, "
                                  f"Chamber: {item.get('chamber', 'N/A')}, "
                                  f"State: {item.get('state', 'N/A')}")
            else:
                print(f"   Status: ❌ ERROR {response.status_code}")
                print(f"   Error: {response.text}")
                print(f"   URL: {response.url}")
                
        except requests.exceptions.RequestException as e:
            print(f"   Status: ❌ REQUEST ERROR")
            print(f"   Error: {e}")

def main():
    """Main execution function"""
    test_api_filters()

if __name__ == "__main__":
    main()