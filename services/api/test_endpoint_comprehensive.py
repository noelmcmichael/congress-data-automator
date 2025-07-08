#!/usr/bin/env python3
"""
Comprehensive endpoint testing script for Congressional Data API.
Tests all API endpoints systematically with real data and edge cases.

Phase 3B Step 7: Comprehensive API Endpoint Testing
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests
from dataclasses import dataclass
import traceback


@dataclass
class EndpointTest:
    """Endpoint test configuration."""
    name: str
    endpoint: str
    method: str = "GET"
    params: Optional[Dict[str, Any]] = None
    expected_status: int = 200
    test_category: str = "general"


class ComprehensiveEndpointTester:
    """Comprehensive endpoint testing class."""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.test_results = []
        self.start_time = datetime.now(timezone.utc)
        
        # Define comprehensive endpoint test suite
        self.test_suite = self._define_test_suite()
        
    def _define_test_suite(self) -> List[EndpointTest]:
        """Define comprehensive test suite for all endpoints."""
        return [
            # Health & Status Endpoints
            EndpointTest("Health Check", "/health", "GET", None, 200, "health"),
            EndpointTest("Health Check Z", "/healthz", "GET", None, 200, "health"),
            EndpointTest("Root Endpoint", "/", "GET", None, 200, "health"),
            
            # Member Endpoints - Basic
            EndpointTest("Members List", "/api/v1/members", "GET", None, 200, "members"),
            EndpointTest("Members Pagination", "/api/v1/members", "GET", {"page": 1, "size": 5}, 200, "members"),
            EndpointTest("Members Large Page", "/api/v1/members", "GET", {"page": 1, "size": 50}, 200, "members"),
            
            # Member Endpoints - Filtering
            EndpointTest("Members by Chamber House", "/api/v1/members", "GET", {"chamber": "House"}, 200, "members"),
            EndpointTest("Members by Chamber Senate", "/api/v1/members", "GET", {"chamber": "Senate"}, 200, "members"),
            EndpointTest("Members by Party Republican", "/api/v1/members", "GET", {"party": "Republican"}, 200, "members"),
            EndpointTest("Members by Party Democrat", "/api/v1/members", "GET", {"party": "Democrat"}, 200, "members"),
            EndpointTest("Members by State CA", "/api/v1/members", "GET", {"state": "CA"}, 200, "members"),
            EndpointTest("Members by State TX", "/api/v1/members", "GET", {"state": "TX"}, 200, "members"),
            EndpointTest("Members by State WA", "/api/v1/members", "GET", {"state": "WA"}, 200, "members"),
            
            # Member Endpoints - Search
            EndpointTest("Members Search John", "/api/v1/members", "GET", {"search": "John"}, 200, "members"),
            EndpointTest("Members Search Michael", "/api/v1/members", "GET", {"search": "Michael"}, 200, "members"),
            EndpointTest("Members Search Smith", "/api/v1/members", "GET", {"search": "Smith"}, 200, "members"),
            
            # Member Endpoints - Complex Filters
            EndpointTest("Members House Republican", "/api/v1/members", "GET", {"chamber": "House", "party": "Republican"}, 200, "members"),
            EndpointTest("Members Senate Democrat", "/api/v1/members", "GET", {"chamber": "Senate", "party": "Democrat"}, 200, "members"),
            EndpointTest("Members CA House", "/api/v1/members", "GET", {"state": "CA", "chamber": "House"}, 200, "members"),
            
            # Member Detail Endpoints
            EndpointTest("Member Detail ID 19", "/api/v1/members/19", "GET", None, 200, "members"),
            EndpointTest("Member Detail ID 24", "/api/v1/members/24", "GET", None, 200, "members"),
            EndpointTest("Member Detail ID 29", "/api/v1/members/29", "GET", None, 200, "members"),
            EndpointTest("Member Committees ID 19", "/api/v1/members/19/committees", "GET", None, 200, "members"),
            EndpointTest("Member Committees ID 24", "/api/v1/members/24/committees", "GET", None, 200, "members"),
            EndpointTest("Member Full Detail ID 19", "/api/v1/members/19/full", "GET", None, 200, "members"),
            
            # Committee Endpoints - Basic
            EndpointTest("Committees List", "/api/v1/committees", "GET", None, 200, "committees"),
            EndpointTest("Committees Pagination", "/api/v1/committees", "GET", {"page": 1, "size": 5}, 200, "committees"),
            EndpointTest("Committees Large Page", "/api/v1/committees", "GET", {"page": 1, "size": 30}, 200, "committees"),
            
            # Committee Endpoints - Filtering
            EndpointTest("Committees by Chamber House", "/api/v1/committees", "GET", {"chamber": "House"}, 200, "committees"),
            EndpointTest("Committees by Chamber Senate", "/api/v1/committees", "GET", {"chamber": "Senate"}, 200, "committees"),
            EndpointTest("Committees by Type Standing", "/api/v1/committees", "GET", {"committee_type": "Standing"}, 200, "committees"),
            
            # Committee Endpoints - Search
            EndpointTest("Committees Search Agriculture", "/api/v1/committees", "GET", {"search": "Agriculture"}, 200, "committees"),
            EndpointTest("Committees Search Judiciary", "/api/v1/committees", "GET", {"search": "Judiciary"}, 200, "committees"),
            EndpointTest("Committees Search Armed", "/api/v1/committees", "GET", {"search": "Armed"}, 200, "committees"),
            
            # Committee Detail Endpoints
            EndpointTest("Committee Detail ID 1", "/api/v1/committees/1", "GET", None, 200, "committees"),
            EndpointTest("Committee Detail ID 2", "/api/v1/committees/2", "GET", None, 200, "committees"),
            EndpointTest("Committee Members ID 1", "/api/v1/committees/1/members", "GET", None, 200, "committees"),
            EndpointTest("Committee Members ID 2", "/api/v1/committees/2/members", "GET", None, 200, "committees"),
            EndpointTest("Committee Hearings ID 1", "/api/v1/committees/1/hearings", "GET", None, 200, "committees"),
            
            # Hearing Endpoints
            EndpointTest("Hearings List", "/api/v1/hearings", "GET", None, 200, "hearings"),
            EndpointTest("Hearings Pagination", "/api/v1/hearings", "GET", {"page": 1, "size": 5}, 200, "hearings"),
            EndpointTest("Hearing Detail ID 1", "/api/v1/hearings/1", "GET", None, 200, "hearings"),
            EndpointTest("Hearing Witnesses ID 1", "/api/v1/hearings/1/witnesses", "GET", None, 200, "hearings"),
            
            # Statistics Endpoints (may not be implemented)
            EndpointTest("Member Statistics", "/api/v1/statistics/members", "GET", None, 200, "statistics"),
            EndpointTest("Committee Statistics", "/api/v1/statistics/committees", "GET", None, 200, "statistics"),
            EndpointTest("Hearing Statistics", "/api/v1/statistics/hearings", "GET", None, 200, "statistics"),
            
            # Search Endpoints (may not be implemented)
            EndpointTest("Global Search", "/api/v1/search", "GET", {"q": "judiciary"}, 200, "search"),
            EndpointTest("Search Members", "/api/v1/search/members", "GET", {"q": "Smith"}, 200, "search"),
            EndpointTest("Search Committees", "/api/v1/search/committees", "GET", {"q": "Agriculture"}, 200, "search"),
            
            # Error Test Cases
            EndpointTest("Invalid Member ID", "/api/v1/members/999999", "GET", None, 404, "errors"),
            EndpointTest("Invalid Committee ID", "/api/v1/committees/999999", "GET", None, 404, "errors"),
            EndpointTest("Invalid Hearing ID", "/api/v1/hearings/999999", "GET", None, 404, "errors"),
            EndpointTest("Invalid Pagination", "/api/v1/members", "GET", {"page": -1}, 422, "errors"),
            EndpointTest("Invalid Size", "/api/v1/members", "GET", {"size": 0}, 422, "errors"),
            EndpointTest("Invalid Chamber", "/api/v1/members", "GET", {"chamber": "Invalid"}, 422, "errors"),
            EndpointTest("Invalid Party", "/api/v1/members", "GET", {"party": "Invalid"}, 422, "errors"),
        ]
    
    def run_endpoint_test(self, test: EndpointTest) -> Dict[str, Any]:
        """Run a single endpoint test."""
        url = f"{self.base_url}{test.endpoint}"
        start_time = time.time()
        
        try:
            if test.method == "GET":
                response = requests.get(url, params=test.params, timeout=10)
            else:
                response = requests.request(test.method, url, params=test.params, timeout=10)
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Check status code
            status_match = response.status_code == test.expected_status
            
            # Try to parse JSON response
            try:
                response_data = response.json()
                response_size = len(json.dumps(response_data))
            except:
                response_data = None
                response_size = len(response.text)
            
            # Determine test result
            if status_match:
                if test.expected_status == 200:
                    # For success cases, check data structure
                    if response_data and isinstance(response_data, dict):
                        if "data" in response_data:
                            data_count = len(response_data["data"]) if isinstance(response_data["data"], list) else 1
                            result_status = "PASS"
                            details = {
                                "status_code": response.status_code,
                                "response_size": response_size,
                                "data_count": data_count,
                                "has_pagination": "pagination" in response_data
                            }
                        else:
                            result_status = "PASS"
                            details = {
                                "status_code": response.status_code,
                                "response_size": response_size,
                                "response_type": "simple"
                            }
                    else:
                        result_status = "PASS"
                        details = {
                            "status_code": response.status_code,
                            "response_size": response_size,
                            "response_type": "non_dict"
                        }
                else:
                    # For error cases, just check status code
                    result_status = "PASS"
                    details = {
                        "status_code": response.status_code,
                        "response_size": response_size,
                        "expected_error": True
                    }
            else:
                result_status = "FAIL"
                details = {
                    "status_code": response.status_code,
                    "expected_status": test.expected_status,
                    "response_size": response_size
                }
            
            return {
                "test_name": test.name,
                "endpoint": test.endpoint,
                "category": test.test_category,
                "status": result_status,
                "response_time_ms": response_time_ms,
                "details": details,
                "error_message": None if result_status == "PASS" else f"Expected {test.expected_status}, got {response.status_code}"
            }
            
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return {
                "test_name": test.name,
                "endpoint": test.endpoint,
                "category": test.test_category,
                "status": "ERROR",
                "response_time_ms": response_time_ms,
                "details": {},
                "error_message": str(e)
            }
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive endpoint testing."""
        print("🚀 Starting Comprehensive Endpoint Testing")
        print(f"📅 Test started at: {self.start_time.isoformat()}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🧪 Total tests: {len(self.test_suite)}")
        
        # Group tests by category
        categories = {}
        for test in self.test_suite:
            category = test.test_category
            if category not in categories:
                categories[category] = []
            categories[category].append(test)
        
        # Run tests by category
        for category, tests in categories.items():
            print(f"\n🔍 Testing {category.upper()} endpoints ({len(tests)} tests)")
            
            category_results = []
            for test in tests:
                result = self.run_endpoint_test(test)
                self.test_results.append(result)
                category_results.append(result)
                
                # Print result
                status_emoji = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
                print(f"{status_emoji} {result['test_name']}: {result['status']} ({result['response_time_ms']:.2f}ms)")
                
                if result["status"] != "PASS":
                    print(f"   Error: {result['error_message']}")
                
                if result["details"]:
                    if "data_count" in result["details"]:
                        print(f"   Data: {result['details']['data_count']} items")
            
            # Category summary
            passed = len([r for r in category_results if r["status"] == "PASS"])
            total = len(category_results)
            print(f"📊 {category.upper()} Summary: {passed}/{total} passed ({passed/total*100:.1f}%)")
        
        # Calculate overall statistics
        end_time = datetime.now(timezone.utc)
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        error_tests = len([r for r in self.test_results if r["status"] == "ERROR"])
        
        avg_response_time = sum(r["response_time_ms"] for r in self.test_results) / total_tests if total_tests > 0 else 0
        max_response_time = max(r["response_time_ms"] for r in self.test_results) if total_tests > 0 else 0
        min_response_time = min(r["response_time_ms"] for r in self.test_results) if total_tests > 0 else 0
        
        # Print final summary
        print(f"\n📊 COMPREHENSIVE ENDPOINT TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"⚠️  Errors: {error_tests} ({error_tests/total_tests*100:.1f}%)")
        print(f"⏱️  Average Response Time: {avg_response_time:.2f}ms")
        print(f"⏱️  Max Response Time: {max_response_time:.2f}ms")
        print(f"⏱️  Min Response Time: {min_response_time:.2f}ms")
        print(f"🕐 Total Duration: {(end_time - self.start_time).total_seconds():.2f}s")
        
        # Category breakdown
        print(f"\n📋 CATEGORY BREAKDOWN")
        for category in categories.keys():
            category_results = [r for r in self.test_results if r["category"] == category]
            passed = len([r for r in category_results if r["status"] == "PASS"])
            total = len(category_results)
            print(f"  {category.upper()}: {passed}/{total} passed ({passed/total*100:.1f}%)")
        
        return {
            "test_summary": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "total_duration_seconds": (end_time - self.start_time).total_seconds(),
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "success_rate": passed_tests / total_tests * 100 if total_tests > 0 else 0,
                "average_response_time_ms": avg_response_time,
                "max_response_time_ms": max_response_time,
                "min_response_time_ms": min_response_time,
            },
            "category_results": {
                category: {
                    "total": len([r for r in self.test_results if r["category"] == category]),
                    "passed": len([r for r in self.test_results if r["category"] == category and r["status"] == "PASS"]),
                    "failed": len([r for r in self.test_results if r["category"] == category and r["status"] == "FAIL"]),
                    "errors": len([r for r in self.test_results if r["category"] == category and r["status"] == "ERROR"])
                }
                for category in categories.keys()
            },
            "test_results": self.test_results
        }


def main():
    """Main function to run comprehensive endpoint testing."""
    tester = ComprehensiveEndpointTester()
    results = tester.run_comprehensive_test()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"comprehensive_endpoint_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()