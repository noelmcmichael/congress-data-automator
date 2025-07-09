#!/usr/bin/env python3
"""
Phase 1, Step 1.2: Congress.gov API Capacity Planning
Test API limits and response times for data collection scaling
"""

import os
import requests
import time
import json
from datetime import datetime
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
import sys
sys.path.append('backend')
from backend.app.core.config import Settings

def load_congress_api_key():
    """Load Congress.gov API key from environment"""
    # Check if we're in backend directory
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    # Try to get from environment
    api_key = os.environ.get('CONGRESS_API_KEY')
    if not api_key:
        # Try to read from backend env file
        backend_env = 'backend/.env.production'
        if os.path.exists(backend_env):
            with open(backend_env, 'r') as f:
                for line in f:
                    if line.startswith('CONGRESS_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"')
                        break
    
    return api_key

def test_congress_api_capacity() -> Dict[str, Any]:
    """Test Congress.gov API capacity and limits"""
    print("🔍 Testing Congress.gov API Capacity...")
    
    api_key = load_congress_api_key()
    if not api_key:
        return {"error": "No Congress.gov API key found"}
    
    base_url = "https://api.congress.gov/v3"
    headers = {"X-API-Key": api_key}
    
    capacity_results = {
        "timestamp": datetime.now().isoformat(),
        "api_key_status": "loaded",
        "endpoints": {},
        "performance": {},
        "rate_limits": {},
        "data_availability": {}
    }
    
    try:
        # Test 1: Member endpoints
        print("   Testing member endpoints...")
        
        # House members
        house_start = time.time()
        house_response = requests.get(
            f"{base_url}/member/house",
            headers=headers,
            timeout=30
        )
        house_time = time.time() - house_start
        
        capacity_results["endpoints"]["house_members"] = {
            "status_code": house_response.status_code,
            "response_time": house_time,
            "headers": dict(house_response.headers)
        }
        
        if house_response.status_code == 200:
            house_data = house_response.json()
            capacity_results["data_availability"]["house_members"] = len(house_data.get("members", []))
            print(f"   📊 House members available: {len(house_data.get('members', []))}")
        
        # Senate members
        senate_start = time.time()
        senate_response = requests.get(
            f"{base_url}/member/senate",
            headers=headers,
            timeout=30
        )
        senate_time = time.time() - senate_start
        
        capacity_results["endpoints"]["senate_members"] = {
            "status_code": senate_response.status_code,
            "response_time": senate_time,
            "headers": dict(senate_response.headers)
        }
        
        if senate_response.status_code == 200:
            senate_data = senate_response.json()
            capacity_results["data_availability"]["senate_members"] = len(senate_data.get("members", []))
            print(f"   📊 Senate members available: {len(senate_data.get('members', []))}")
        
        # Test 2: Committee endpoints
        print("   Testing committee endpoints...")
        
        # House committees
        house_committees_start = time.time()
        house_committees_response = requests.get(
            f"{base_url}/committee/house",
            headers=headers,
            timeout=30
        )
        house_committees_time = time.time() - house_committees_start
        
        capacity_results["endpoints"]["house_committees"] = {
            "status_code": house_committees_response.status_code,
            "response_time": house_committees_time,
            "headers": dict(house_committees_response.headers)
        }
        
        if house_committees_response.status_code == 200:
            house_committees_data = house_committees_response.json()
            capacity_results["data_availability"]["house_committees"] = len(house_committees_data.get("committees", []))
            print(f"   📊 House committees available: {len(house_committees_data.get('committees', []))}")
        
        # Senate committees
        senate_committees_start = time.time()
        senate_committees_response = requests.get(
            f"{base_url}/committee/senate",
            headers=headers,
            timeout=30
        )
        senate_committees_time = time.time() - senate_committees_start
        
        capacity_results["endpoints"]["senate_committees"] = {
            "status_code": senate_committees_response.status_code,
            "response_time": senate_committees_time,
            "headers": dict(senate_committees_response.headers)
        }
        
        if senate_committees_response.status_code == 200:
            senate_committees_data = senate_committees_response.json()
            capacity_results["data_availability"]["senate_committees"] = len(senate_committees_data.get("committees", []))
            print(f"   📊 Senate committees available: {len(senate_committees_data.get('committees', []))}")
        
        # Test 3: Rate limiting analysis
        print("   Testing rate limits...")
        
        # Check for rate limit headers
        sample_headers = house_response.headers
        rate_limit_headers = {}
        for header_name, header_value in sample_headers.items():
            if 'rate' in header_name.lower() or 'limit' in header_name.lower():
                rate_limit_headers[header_name] = header_value
        
        capacity_results["rate_limits"]["headers"] = rate_limit_headers
        
        # Test 4: Performance analysis
        print("   Analyzing performance...")
        
        response_times = [
            house_time,
            senate_time,
            house_committees_time,
            senate_committees_time
        ]
        
        capacity_results["performance"] = {
            "average_response_time": sum(response_times) / len(response_times),
            "max_response_time": max(response_times),
            "min_response_time": min(response_times),
            "total_test_time": sum(response_times)
        }
        
        # Test 5: Bulk request simulation
        print("   Testing bulk request capacity...")
        
        # Simulate multiple concurrent requests
        def make_request(url):
            start_time = time.time()
            try:
                response = requests.get(url, headers=headers, timeout=10)
                return {
                    "status_code": response.status_code,
                    "response_time": time.time() - start_time,
                    "success": response.status_code == 200
                }
            except Exception as e:
                return {
                    "status_code": 0,
                    "response_time": time.time() - start_time,
                    "success": False,
                    "error": str(e)
                }
        
        # Test concurrent requests
        urls = [
            f"{base_url}/member/house",
            f"{base_url}/member/senate",
            f"{base_url}/committee/house",
            f"{base_url}/committee/senate"
        ] * 3  # Test 12 concurrent requests
        
        concurrent_start = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(make_request, url) for url in urls]
            concurrent_results = [future.result() for future in as_completed(futures)]
        concurrent_time = time.time() - concurrent_start
        
        successful_requests = sum(1 for r in concurrent_results if r["success"])
        capacity_results["performance"]["concurrent_test"] = {
            "total_requests": len(urls),
            "successful_requests": successful_requests,
            "success_rate": successful_requests / len(urls),
            "total_time": concurrent_time,
            "average_concurrent_response_time": sum(r["response_time"] for r in concurrent_results) / len(concurrent_results)
        }
        
        print(f"   📊 Concurrent requests: {successful_requests}/{len(urls)} successful")
        
        print("✅ API Capacity Testing Complete")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        capacity_results["error"] = str(e)
    except Exception as e:
        print(f"❌ Capacity test failed: {e}")
        capacity_results["error"] = str(e)
    
    return capacity_results

def calculate_scaling_recommendations(results: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate scaling recommendations based on capacity test results"""
    recommendations = {
        "batch_size": 10,  # Default conservative batch size
        "request_delay": 1.0,  # Default delay between requests
        "concurrent_limit": 2,  # Default concurrent requests
        "estimated_time": {}
    }
    
    if "performance" in results:
        performance = results["performance"]
        avg_response_time = performance.get("average_response_time", 1.0)
        
        # Calculate optimal batch size based on response time
        if avg_response_time < 0.5:
            recommendations["batch_size"] = 20
            recommendations["request_delay"] = 0.5
            recommendations["concurrent_limit"] = 4
        elif avg_response_time < 1.0:
            recommendations["batch_size"] = 15
            recommendations["request_delay"] = 0.7
            recommendations["concurrent_limit"] = 3
        else:
            recommendations["batch_size"] = 10
            recommendations["request_delay"] = 1.0
            recommendations["concurrent_limit"] = 2
        
        # Calculate estimated collection times
        members_needed = 485  # From audit
        committees_needed = 150  # Estimated additional committees
        
        # Member collection time
        member_batches = (members_needed + recommendations["batch_size"] - 1) // recommendations["batch_size"]
        member_collection_time = member_batches * (avg_response_time + recommendations["request_delay"])
        
        # Committee collection time
        committee_batches = (committees_needed + recommendations["batch_size"] - 1) // recommendations["batch_size"]
        committee_collection_time = committee_batches * (avg_response_time + recommendations["request_delay"])
        
        recommendations["estimated_time"] = {
            "member_collection_minutes": member_collection_time / 60,
            "committee_collection_minutes": committee_collection_time / 60,
            "total_collection_minutes": (member_collection_time + committee_collection_time) / 60
        }
    
    return recommendations

def save_capacity_results(results: Dict[str, Any], recommendations: Dict[str, Any]) -> str:
    """Save capacity test results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"phase1_capacity_results_{timestamp}.json"
    
    combined_results = {
        "capacity_test": results,
        "recommendations": recommendations
    }
    
    with open(filename, 'w') as f:
        json.dump(combined_results, f, indent=2)
    
    print(f"📄 Capacity test results saved to: {filename}")
    return filename

def print_capacity_summary(results: Dict[str, Any], recommendations: Dict[str, Any]):
    """Print capacity test summary"""
    print("\n" + "="*60)
    print("📋 CONGRESS.GOV API CAPACITY SUMMARY")
    print("="*60)
    
    if "error" in results:
        print(f"❌ Capacity test failed: {results['error']}")
        return
    
    print(f"🕐 Test Time: {results.get('timestamp', 'Unknown')}")
    print(f"🔑 API Key: {results.get('api_key_status', 'Unknown')}")
    
    # Data availability
    if "data_availability" in results:
        availability = results["data_availability"]
        print(f"\n📊 DATA AVAILABILITY:")
        print(f"   • House Members: {availability.get('house_members', 0)}")
        print(f"   • Senate Members: {availability.get('senate_members', 0)}")
        print(f"   • House Committees: {availability.get('house_committees', 0)}")
        print(f"   • Senate Committees: {availability.get('senate_committees', 0)}")
        
        total_members = availability.get('house_members', 0) + availability.get('senate_members', 0)
        print(f"   • Total Members Available: {total_members}")
    
    # Performance metrics
    if "performance" in results:
        performance = results["performance"]
        print(f"\n⚡ PERFORMANCE METRICS:")
        print(f"   • Average Response Time: {performance.get('average_response_time', 0):.2f}s")
        print(f"   • Max Response Time: {performance.get('max_response_time', 0):.2f}s")
        print(f"   • Min Response Time: {performance.get('min_response_time', 0):.2f}s")
        
        if "concurrent_test" in performance:
            concurrent = performance["concurrent_test"]
            print(f"   • Concurrent Success Rate: {concurrent.get('success_rate', 0):.1%}")
            print(f"   • Concurrent Response Time: {concurrent.get('average_concurrent_response_time', 0):.2f}s")
    
    # Recommendations
    print(f"\n🚀 SCALING RECOMMENDATIONS:")
    print(f"   • Batch Size: {recommendations.get('batch_size', 10)} requests/batch")
    print(f"   • Request Delay: {recommendations.get('request_delay', 1.0)}s between requests")
    print(f"   • Concurrent Limit: {recommendations.get('concurrent_limit', 2)} concurrent requests")
    
    if "estimated_time" in recommendations:
        estimated = recommendations["estimated_time"]
        print(f"   • Member Collection Time: {estimated.get('member_collection_minutes', 0):.1f} minutes")
        print(f"   • Committee Collection Time: {estimated.get('committee_collection_minutes', 0):.1f} minutes")
        print(f"   • Total Collection Time: {estimated.get('total_collection_minutes', 0):.1f} minutes")

if __name__ == "__main__":
    print("🚀 Phase 1, Step 1.2: Congress.gov API Capacity Planning")
    print("="*55)
    
    # Test API capacity
    capacity_results = test_congress_api_capacity()
    
    # Calculate recommendations
    recommendations = calculate_scaling_recommendations(capacity_results)
    
    # Save results
    filename = save_capacity_results(capacity_results, recommendations)
    
    # Print summary
    print_capacity_summary(capacity_results, recommendations)
    
    print(f"\n📋 Next Steps:")
    print("   1. Review capacity test results and recommendations")
    print("   2. Proceed to Step 1.3: Migration Strategy Planning")
    print("   3. Use recommendations for optimal data collection approach")