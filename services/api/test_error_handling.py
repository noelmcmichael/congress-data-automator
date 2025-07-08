#!/usr/bin/env python3
"""
Error handling and edge cases testing script for Congressional Data API.
Tests comprehensive error scenarios and validates proper error handling.

Phase 3B Step 8: Error Handling & Edge Cases Testing
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests
from dataclasses import dataclass
import traceback


@dataclass
class ErrorTest:
    """Error test configuration."""
    name: str
    endpoint: str
    method: str = "GET"
    params: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    expected_status: int = 404
    expected_error_type: Optional[str] = None
    test_category: str = "error"


class ErrorHandlingTester:
    """Error handling and edge cases testing class."""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.test_results = []
        self.start_time = datetime.now(timezone.utc)
        
        # Define error test suite
        self.error_tests = self._define_error_tests()
        
    def _define_error_tests(self) -> List[ErrorTest]:
        """Define comprehensive error test suite."""
        return [
            # Invalid ID Tests
            ErrorTest("Non-existent Member ID", "/api/v1/members/999999", "GET", None, None, 404, "NotFound", "invalid_id"),
            ErrorTest("Non-existent Committee ID", "/api/v1/committees/999999", "GET", None, None, 404, "NotFound", "invalid_id"),
            ErrorTest("Non-existent Hearing ID", "/api/v1/hearings/999999", "GET", None, None, 404, "NotFound", "invalid_id"),
            ErrorTest("Zero Member ID", "/api/v1/members/0", "GET", None, None, 404, "NotFound", "invalid_id"),
            ErrorTest("Negative Member ID", "/api/v1/members/-1", "GET", None, None, 404, "NotFound", "invalid_id"),
            ErrorTest("String Member ID", "/api/v1/members/abc", "GET", None, None, 404, "NotFound", "invalid_id"),
            ErrorTest("Float Member ID", "/api/v1/members/1.5", "GET", None, None, 404, "NotFound", "invalid_id"),
            
            # Invalid Pagination Tests
            ErrorTest("Negative Page", "/api/v1/members", "GET", {"page": -1}, None, 422, "ValidationError", "pagination"),
            ErrorTest("Zero Page", "/api/v1/members", "GET", {"page": 0}, None, 422, "ValidationError", "pagination"),
            ErrorTest("Negative Size", "/api/v1/members", "GET", {"size": -1}, None, 422, "ValidationError", "pagination"),
            ErrorTest("Zero Size", "/api/v1/members", "GET", {"size": 0}, None, 422, "ValidationError", "pagination"),
            ErrorTest("Oversized Page", "/api/v1/members", "GET", {"size": 1000}, None, 422, "ValidationError", "pagination"),
            ErrorTest("String Page", "/api/v1/members", "GET", {"page": "abc"}, None, 422, "ValidationError", "pagination"),
            ErrorTest("Float Page", "/api/v1/members", "GET", {"page": 1.5}, None, 422, "ValidationError", "pagination"),
            
            # Invalid Filter Tests
            ErrorTest("Invalid Chamber", "/api/v1/members", "GET", {"chamber": "InvalidChamber"}, None, 422, "ValidationError", "filters"),
            ErrorTest("Invalid Party", "/api/v1/members", "GET", {"party": "InvalidParty"}, None, 422, "ValidationError", "filters"),
            ErrorTest("Invalid State", "/api/v1/members", "GET", {"state": "InvalidState"}, None, 422, "ValidationError", "filters"),
            ErrorTest("Invalid Committee Type", "/api/v1/committees", "GET", {"committee_type": "InvalidType"}, None, 422, "ValidationError", "filters"),
            ErrorTest("Empty String Filter", "/api/v1/members", "GET", {"party": ""}, None, 422, "ValidationError", "filters"),
            ErrorTest("Null Filter", "/api/v1/members", "GET", {"chamber": "null"}, None, 422, "ValidationError", "filters"),
            
            # Invalid Search Tests
            ErrorTest("Empty Search", "/api/v1/members", "GET", {"search": ""}, None, 200, None, "search"),
            ErrorTest("Very Long Search", "/api/v1/members", "GET", {"search": "a" * 1000}, None, 200, None, "search"),
            ErrorTest("Special Character Search", "/api/v1/members", "GET", {"search": "!@#$%^&*()"}, None, 200, None, "search"),
            ErrorTest("SQL Injection Search", "/api/v1/members", "GET", {"search": "'; DROP TABLE members; --"}, None, 200, None, "search"),
            
            # Invalid Method Tests
            ErrorTest("POST to GET endpoint", "/api/v1/members", "POST", None, None, 405, "MethodNotAllowed", "methods"),
            ErrorTest("PUT to GET endpoint", "/api/v1/members", "PUT", None, None, 405, "MethodNotAllowed", "methods"),
            ErrorTest("DELETE to GET endpoint", "/api/v1/members", "DELETE", None, None, 405, "MethodNotAllowed", "methods"),
            
            # Invalid Content Type Tests
            ErrorTest("Invalid JSON", "/api/v1/members", "POST", None, {"invalid": "json"}, 405, "MethodNotAllowed", "content"),
            
            # Non-existent Endpoints
            ErrorTest("Non-existent Endpoint", "/api/v1/nonexistent", "GET", None, None, 404, "NotFound", "endpoints"),
            ErrorTest("Invalid API Version", "/api/v2/members", "GET", None, None, 404, "NotFound", "endpoints"),
            ErrorTest("Misspelled Endpoint", "/api/v1/member", "GET", None, None, 404, "NotFound", "endpoints"),
            
            # Complex Invalid Combinations
            ErrorTest("Invalid Member + Committee", "/api/v1/members/999999/committees", "GET", None, None, 404, "NotFound", "combinations"),
            ErrorTest("Invalid Committee + Members", "/api/v1/committees/999999/members", "GET", None, None, 404, "NotFound", "combinations"),
            ErrorTest("Invalid Hearing + Witnesses", "/api/v1/hearings/999999/witnesses", "GET", None, None, 404, "NotFound", "combinations"),
            
            # Edge Case Values
            ErrorTest("Very Large Page Number", "/api/v1/members", "GET", {"page": 999999}, None, 200, None, "edge_cases"),
            ErrorTest("Unicode in Search", "/api/v1/members", "GET", {"search": "José"}, None, 200, None, "edge_cases"),
            ErrorTest("Multiple Filters", "/api/v1/members", "GET", {"chamber": "House", "party": "Republican", "state": "CA"}, None, 200, None, "edge_cases"),
        ]
    
    def run_error_test(self, test: ErrorTest) -> Dict[str, Any]:
        """Run a single error test."""
        url = f"{self.base_url}{test.endpoint}"
        start_time = time.time()
        
        try:
            if test.method == "GET":
                response = requests.get(url, params=test.params, timeout=10)
            elif test.method == "POST":
                response = requests.post(url, json=test.data, params=test.params, timeout=10)
            elif test.method == "PUT":
                response = requests.put(url, json=test.data, params=test.params, timeout=10)
            elif test.method == "DELETE":
                response = requests.delete(url, params=test.params, timeout=10)
            else:
                response = requests.request(test.method, url, params=test.params, json=test.data, timeout=10)
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Try to parse response
            try:
                response_data = response.json()
                response_size = len(json.dumps(response_data))
            except:
                response_data = {"raw_response": response.text}
                response_size = len(response.text)
            
            # Check if status code matches expectation
            status_match = response.status_code == test.expected_status
            
            # For error cases, check if proper error structure is returned
            error_structure_valid = True
            if test.expected_status >= 400 and response.status_code >= 400:
                if isinstance(response_data, dict):
                    # Check for standard error response structure
                    has_error_field = "error" in response_data or "message" in response_data
                    has_success_field = "success" in response_data
                    
                    if has_error_field:
                        error_structure_valid = True
                    else:
                        error_structure_valid = False
                else:
                    error_structure_valid = False
            
            # Determine overall test result
            if status_match and error_structure_valid:
                result_status = "PASS"
                error_message = None
            elif not status_match:
                result_status = "FAIL"
                error_message = f"Expected status {test.expected_status}, got {response.status_code}"
            else:
                result_status = "FAIL"
                error_message = "Invalid error response structure"
            
            return {
                "test_name": test.name,
                "endpoint": test.endpoint,
                "method": test.method,
                "category": test.test_category,
                "status": result_status,
                "response_time_ms": response_time_ms,
                "details": {
                    "status_code": response.status_code,
                    "expected_status": test.expected_status,
                    "response_size": response_size,
                    "error_structure_valid": error_structure_valid,
                    "response_data": response_data
                },
                "error_message": error_message
            }
            
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return {
                "test_name": test.name,
                "endpoint": test.endpoint,
                "method": test.method,
                "category": test.test_category,
                "status": "ERROR",
                "response_time_ms": response_time_ms,
                "details": {},
                "error_message": str(e)
            }
    
    def run_comprehensive_error_test(self) -> Dict[str, Any]:
        """Run comprehensive error handling testing."""
        print("🚀 Starting Comprehensive Error Handling Testing")
        print(f"📅 Test started at: {self.start_time.isoformat()}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🧪 Total error tests: {len(self.error_tests)}")
        
        # Group tests by category
        categories = {}
        for test in self.error_tests:
            category = test.test_category
            if category not in categories:
                categories[category] = []
            categories[category].append(test)
        
        # Run tests by category
        for category, tests in categories.items():
            print(f"\n🔍 Testing {category.upper()} errors ({len(tests)} tests)")
            
            category_results = []
            for test in tests:
                result = self.run_error_test(test)
                self.test_results.append(result)
                category_results.append(result)
                
                # Print result
                status_emoji = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
                print(f"{status_emoji} {result['test_name']}: {result['status']} ({result['response_time_ms']:.2f}ms)")
                
                if result["status"] != "PASS":
                    print(f"   Error: {result['error_message']}")
                
                if result["details"]:
                    print(f"   Status: {result['details']['status_code']} (expected: {result['details']['expected_status']})")
            
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
        print(f"\n📊 ERROR HANDLING TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"⚠️  Errors: {error_tests} ({error_tests/total_tests*100:.1f}%)")
        print(f"⏱️  Average Response Time: {avg_response_time:.2f}ms")
        print(f"⏱️  Max Response Time: {max_response_time:.2f}ms")
        print(f"⏱️  Min Response Time: {min_response_time:.2f}ms")
        print(f"🕐 Total Duration: {(end_time - self.start_time).total_seconds():.2f}s")
        
        # Category breakdown
        print(f"\n📋 ERROR CATEGORY BREAKDOWN")
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
    """Main function to run error handling testing."""
    tester = ErrorHandlingTester()
    results = tester.run_comprehensive_error_test()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"error_handling_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()