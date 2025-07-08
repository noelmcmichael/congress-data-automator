#!/usr/bin/env python3
"""
Simple load test for Congressional Data API production validation.
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

import httpx

# Production API URL
API_URL = "https://congressional-data-api-v3-1066017671167.us-central1.run.app"

def single_request(url: str) -> Dict:
    """Make a single HTTP request."""
    start_time = time.time()
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 200,
                "url": url
            }
    except Exception as e:
        end_time = time.time()
        return {
            "status_code": 0,
            "response_time": end_time - start_time,
            "success": False,
            "error": str(e),
            "url": url
        }

def run_load_test(concurrent_users: int = 20, requests_per_user: int = 5) -> Dict:
    """Run a simple load test."""
    print(f"Running load test: {concurrent_users} concurrent users, {requests_per_user} requests each")
    
    # Test endpoints
    endpoints = [
        f"{API_URL}/health",
        f"{API_URL}/api/v1/members?limit=10",
        f"{API_URL}/api/v1/committees?limit=10",
        f"{API_URL}/api/v1/hearings?limit=10",
        f"{API_URL}/api/v1/members?party=Republican&limit=5",
        f"{API_URL}/api/v1/members?chamber=Senate&limit=5"
    ]
    
    # Generate all requests
    all_requests = []
    for user in range(concurrent_users):
        for request in range(requests_per_user):
            endpoint = endpoints[request % len(endpoints)]
            all_requests.append(endpoint)
    
    # Run concurrent requests
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        results = list(executor.map(single_request, all_requests))
    end_time = time.time()
    
    # Analyze results
    total_requests = len(results)
    successful_requests = len([r for r in results if r["success"]])
    failed_requests = total_requests - successful_requests
    
    response_times = [r["response_time"] for r in results if r["success"]]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    
    total_time = end_time - start_time
    requests_per_second = total_requests / total_time if total_time > 0 else 0
    
    # Status code distribution
    status_codes = {}
    for result in results:
        code = result["status_code"]
        status_codes[code] = status_codes.get(code, 0) + 1
    
    return {
        "test_config": {
            "concurrent_users": concurrent_users,
            "requests_per_user": requests_per_user,
            "total_requests": total_requests,
            "test_duration": total_time
        },
        "performance": {
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            "requests_per_second": requests_per_second,
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time
        },
        "status_codes": status_codes,
        "detailed_results": results
    }

def main():
    """Run load test and display results."""
    print("=" * 80)
    print("CONGRESSIONAL DATA API - LOAD TEST")
    print("=" * 80)
    print(f"Target: {API_URL}")
    
    # Run different load scenarios
    scenarios = [
        {"users": 10, "requests": 3},
        {"users": 20, "requests": 5},
        {"users": 50, "requests": 2}
    ]
    
    for scenario in scenarios:
        print(f"\n--- Scenario: {scenario['users']} users, {scenario['requests']} requests each ---")
        
        results = run_load_test(
            concurrent_users=scenario["users"], 
            requests_per_user=scenario["requests"]
        )
        
        config = results["test_config"]
        perf = results["performance"]
        
        print(f"Total Requests: {config['total_requests']}")
        print(f"Test Duration: {config['test_duration']:.2f}s")
        print(f"Success Rate: {perf['success_rate']:.1f}%")
        print(f"Requests/sec: {perf['requests_per_second']:.1f}")
        print(f"Avg Response Time: {perf['avg_response_time']:.3f}s")
        print(f"Min Response Time: {perf['min_response_time']:.3f}s")
        print(f"Max Response Time: {perf['max_response_time']:.3f}s")
        print(f"Status Codes: {results['status_codes']}")
        
        if perf["failed_requests"] > 0:
            print(f"⚠️  {perf['failed_requests']} failed requests detected")
        else:
            print("✅ All requests successful")
    
    print("\n" + "=" * 80)
    print("LOAD TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()