#!/usr/bin/env python3
"""Comprehensive test script for all API endpoints with real data."""

import json
import requests
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8003"

def test_endpoint(method: str, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
    """Test a single endpoint and return results."""
    start_time = time.time()
    
    try:
        if method.upper() == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            return {"error": f"Method {method} not supported"}
        
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
        
        # Try to parse JSON response
        try:
            data = response.json()
            json_valid = True
        except:
            data = response.text
            json_valid = False
        
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "json_valid": json_valid,
            "data": data,
            "success": response.status_code == expected_status
        }
    
    except Exception as e:
        return {
            "endpoint": endpoint,
            "method": method,
            "error": str(e),
            "success": False
        }

def main():
    """Run comprehensive endpoint tests."""
    print("🔍 Phase 3B: Step 5 - Data Quality Assessment")
    print("=" * 60)
    print("Testing all API endpoints with real congressional data...")
    print()
    
    # Test endpoints
    endpoints = [
        # Health endpoints
        ("GET", "/health"),
        ("GET", "/healthz"),
        
        # Root endpoint
        ("GET", "/"),
        
        # Member endpoints
        ("GET", "/api/v1/members"),
        ("GET", "/api/v1/members?page=1&size=5"),
        ("GET", "/api/v1/members?chamber=House"),
        ("GET", "/api/v1/members?party=Republican"),
        ("GET", "/api/v1/members?state=WA"),
        ("GET", "/api/v1/members?search=Michael"),
        ("GET", "/api/v1/members/19"),
        ("GET", "/api/v1/members/19/committees"),
        ("GET", "/api/v1/members/19/full"),
        ("GET", "/api/v1/members/statistics"),
        
        # Committee endpoints
        ("GET", "/api/v1/committees"),
        ("GET", "/api/v1/committees?page=1&size=5"),
        ("GET", "/api/v1/committees?chamber=House"),
        ("GET", "/api/v1/committees?search=Agriculture"),
        ("GET", "/api/v1/committees/statistics"),
        
        # Hearing endpoints
        ("GET", "/api/v1/hearings"),
        ("GET", "/api/v1/hearings/statistics"),
        
        # Search endpoints
        ("GET", "/api/v1/search?q=agriculture"),
        ("GET", "/api/v1/search/members?q=Michael"),
        ("GET", "/api/v1/search/committees?q=Agriculture"),
        ("GET", "/api/v1/search/hearings?q=budget"),
    ]
    
    results = []
    successful_tests = 0
    total_tests = len(endpoints)
    
    for method, endpoint in endpoints:
        print(f"Testing {method} {endpoint}...")
        result = test_endpoint(method, endpoint)
        results.append(result)
        
        if result.get("success", False):
            successful_tests += 1
            status_icon = "✅"
        else:
            status_icon = "❌"
        
        print(f"  {status_icon} {result.get('status_code', 'ERROR')} - {result.get('response_time_ms', 0)}ms")
    
    print()
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    print()
    
    # Analyze data quality
    print("📋 Data Quality Analysis")
    print("=" * 60)
    
    # Analyze member data
    member_result = next((r for r in results if r["endpoint"] == "/api/v1/members"), None)
    if member_result and member_result.get("success"):
        data = member_result["data"]
        if isinstance(data, dict) and "data" in data:
            members = data["data"]
            pagination = data.get("pagination", {})
            
            print(f"👥 Member Data Analysis:")
            print(f"  - Total members: {pagination.get('total', 0)}")
            print(f"  - Current page size: {len(members)}")
            print(f"  - Pagination working: {'✅' if pagination.get('pages', 0) > 1 else '❌'}")
            
            if members:
                first_member = members[0]
                print(f"  - Sample member: {first_member.get('name', 'Unknown')}")
                print(f"  - Required fields present: {'✅' if all(k in first_member for k in ['name', 'party', 'state', 'chamber']) else '❌'}")
    
    # Analyze committee data
    committee_result = next((r for r in results if r["endpoint"] == "/api/v1/committees"), None)
    if committee_result and committee_result.get("success"):
        data = committee_result["data"]
        if isinstance(data, dict) and "data" in data:
            committees = data["data"]
            pagination = data.get("pagination", {})
            
            print(f"🏛️ Committee Data Analysis:")
            print(f"  - Total committees: {pagination.get('total', 0)}")
            print(f"  - Current page size: {len(committees)}")
            print(f"  - Pagination working: {'✅' if pagination.get('pages', 0) > 1 else '❌'}")
            
            if committees:
                first_committee = committees[0]
                print(f"  - Sample committee: {first_committee.get('name', 'Unknown')}")
                print(f"  - Required fields present: {'✅' if all(k in first_committee for k in ['name', 'chamber', 'committee_type']) else '❌'}")
    
    print()
    print("🔍 Performance Analysis")
    print("=" * 60)
    
    # Calculate average response time
    response_times = [r.get("response_time_ms", 0) for r in results if r.get("success")]
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        print(f"Response Time Analysis:")
        print(f"  - Average: {avg_response_time:.2f}ms")
        print(f"  - Maximum: {max_response_time:.2f}ms")
        print(f"  - Minimum: {min_response_time:.2f}ms")
        print(f"  - Performance: {'✅ Excellent' if avg_response_time < 100 else '⚠️ Good' if avg_response_time < 500 else '❌ Needs improvement'}")
    
    # Failed endpoints analysis
    failed_tests = [r for r in results if not r.get("success")]
    if failed_tests:
        print()
        print("❌ Failed Endpoints Analysis")
        print("=" * 60)
        for test in failed_tests:
            print(f"  - {test['endpoint']}: {test.get('error', test.get('status_code', 'Unknown error'))}")
    
    print()
    print("✅ Step 5: Data Quality Assessment Complete")
    print("Ready to proceed to Step 6: Relationship Integrity Testing")
    
    # Save results to file
    with open("phase3b_step5_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Results saved to: phase3b_step5_results.json")

if __name__ == "__main__":
    main()