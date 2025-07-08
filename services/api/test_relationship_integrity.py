#!/usr/bin/env python3
"""
Comprehensive relationship integrity testing script for Congressional Data API.
Tests all data relationships with real congressional data and verifies integrity.

Phase 3B Step 6: Relationship Integrity Testing
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests
from dataclasses import dataclass
import traceback


@dataclass
class TestResult:
    """Test result data structure."""
    test_name: str
    endpoint: str
    status: str  # 'PASS', 'FAIL', 'ERROR'
    response_time_ms: float
    details: Dict[str, Any]
    error_message: Optional[str] = None


class RelationshipIntegrityTester:
    """Comprehensive relationship integrity testing class."""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.test_results: List[TestResult] = []
        self.start_time = datetime.now(timezone.utc)
        
    def log_test_result(self, result: TestResult):
        """Log test result and print to console."""
        self.test_results.append(result)
        status_emoji = "✅" if result.status == "PASS" else "❌" if result.status == "FAIL" else "⚠️"
        print(f"{status_emoji} {result.test_name}: {result.status} ({result.response_time_ms:.2f}ms)")
        if result.error_message:
            print(f"   Error: {result.error_message}")
        if result.details:
            print(f"   Details: {result.details}")
    
    def make_request(self, endpoint: str, test_name: str) -> TestResult:
        """Make HTTP request and return test result."""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=10)
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                return TestResult(
                    test_name=test_name,
                    endpoint=endpoint,
                    status="PASS",
                    response_time_ms=response_time_ms,
                    details={"response_size": len(str(data)), "status_code": response.status_code},
                    error_message=None
                )
            else:
                return TestResult(
                    test_name=test_name,
                    endpoint=endpoint,
                    status="FAIL",
                    response_time_ms=response_time_ms,
                    details={"status_code": response.status_code},
                    error_message=f"HTTP {response.status_code}: {response.text[:200]}"
                )
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            return TestResult(
                test_name=test_name,
                endpoint=endpoint,
                status="ERROR",
                response_time_ms=response_time_ms,
                details={},
                error_message=str(e)
            )
    
    def test_member_committee_relationships(self) -> None:
        """Test member-committee relationships extensively."""
        print("\n🔍 Testing Member-Committee Relationships")
        
        # 1. Get list of members
        members_result = self.make_request("/api/v1/members", "Get Members List")
        self.log_test_result(members_result)
        
        if members_result.status != "PASS":
            print("❌ Cannot proceed with member-committee testing - members endpoint failed")
            return
        
        # Parse members data
        members_response = requests.get(f"{self.base_url}/api/v1/members")
        members_data = members_response.json()
        
        if "data" not in members_data:
            print("❌ Members response missing 'data' field")
            return
        
        members = members_data["data"]
        print(f"📊 Found {len(members)} members for relationship testing")
        
        # 2. Test first 5 members' committee relationships
        relationship_tests = []
        for i, member in enumerate(members[:5]):
            member_id = member.get("id")
            member_name = member.get("full_name", "Unknown")
            
            if member_id:
                # Test member committees endpoint
                committees_result = self.make_request(
                    f"/api/v1/members/{member_id}/committees", 
                    f"Member {member_name} Committees"
                )
                self.log_test_result(committees_result)
                
                if committees_result.status == "PASS":
                    # Get committee data for validation
                    committees_response = requests.get(f"{self.base_url}/api/v1/members/{member_id}/committees")
                    committees_data = committees_response.json()
                    
                    if "data" in committees_data:
                        committees = committees_data["data"]
                        relationship_tests.append({
                            "member_id": member_id,
                            "member_name": member_name,
                            "committees_count": len(committees),
                            "committees": committees
                        })
        
        print(f"✅ Successfully tested {len(relationship_tests)} member-committee relationships")
        
        # 3. Test full member details
        if relationship_tests:
            first_member = relationship_tests[0]
            full_result = self.make_request(
                f"/api/v1/members/{first_member['member_id']}/full",
                f"Full Member Details - {first_member['member_name']}"
            )
            self.log_test_result(full_result)
    
    def test_committee_hierarchy(self) -> None:
        """Test committee hierarchy and structure."""
        print("\n🏛️ Testing Committee Hierarchy")
        
        # 1. Get list of committees
        committees_result = self.make_request("/api/v1/committees", "Get Committees List")
        self.log_test_result(committees_result)
        
        if committees_result.status != "PASS":
            print("❌ Cannot proceed with committee hierarchy testing - committees endpoint failed")
            return
        
        # Parse committees data
        committees_response = requests.get(f"{self.base_url}/api/v1/committees")
        committees_data = committees_response.json()
        
        if "data" not in committees_data:
            print("❌ Committees response missing 'data' field")
            return
        
        committees = committees_data["data"]
        print(f"📊 Found {len(committees)} committees for hierarchy testing")
        
        # 2. Test committee types and structure
        committee_types = {}
        for committee in committees:
            committee_type = committee.get("committee_type", "Unknown")
            committee_types[committee_type] = committee_types.get(committee_type, 0) + 1
        
        print(f"📋 Committee types found: {committee_types}")
        
        # 3. Test first 3 committees' member relationships
        for i, committee in enumerate(committees[:3]):
            committee_id = committee.get("id")
            committee_name = committee.get("name", "Unknown")
            
            if committee_id:
                # Test committee members endpoint
                members_result = self.make_request(
                    f"/api/v1/committees/{committee_id}/members",
                    f"Committee {committee_name} Members"
                )
                self.log_test_result(members_result)
    
    def test_cross_reference_validation(self) -> None:
        """Test data consistency across all endpoints."""
        print("\n🔄 Testing Cross-Reference Validation")
        
        # 1. Get a member and their committees
        members_response = requests.get(f"{self.base_url}/api/v1/members?size=1")
        members_data = members_response.json()
        
        if "data" not in members_data or not members_data["data"]:
            print("❌ No members found for cross-reference testing")
            return
        
        member = members_data["data"][0]
        member_id = member.get("id")
        member_name = member.get("full_name", "Unknown")
        
        print(f"🔍 Cross-referencing member: {member_name} (ID: {member_id})")
        
        # 2. Get member's committees
        committees_response = requests.get(f"{self.base_url}/api/v1/members/{member_id}/committees")
        if committees_response.status_code == 200:
            committees_data = committees_response.json()
            if "data" in committees_data and committees_data["data"]:
                member_committees = committees_data["data"]
                print(f"📋 Member is on {len(member_committees)} committees")
                
                # 3. Validate committee membership consistency
                for committee in member_committees:
                    committee_id = committee.get("id")
                    committee_name = committee.get("name", "Unknown")
                    
                    if committee_id:
                        # Check if member appears in committee's member list
                        committee_members_response = requests.get(
                            f"{self.base_url}/api/v1/committees/{committee_id}/members"
                        )
                        
                        if committee_members_response.status_code == 200:
                            committee_members_data = committee_members_response.json()
                            if "data" in committee_members_data:
                                committee_members = committee_members_data["data"]
                                member_ids = [m.get("id") for m in committee_members]
                                
                                if member_id in member_ids:
                                    self.log_test_result(TestResult(
                                        test_name=f"Cross-reference {committee_name}",
                                        endpoint=f"/api/v1/committees/{committee_id}/members",
                                        status="PASS",
                                        response_time_ms=0,
                                        details={"member_found": True, "committee_members": len(committee_members)},
                                        error_message=None
                                    ))
                                else:
                                    self.log_test_result(TestResult(
                                        test_name=f"Cross-reference {committee_name}",
                                        endpoint=f"/api/v1/committees/{committee_id}/members",
                                        status="FAIL",
                                        response_time_ms=0,
                                        details={"member_found": False, "committee_members": len(committee_members)},
                                        error_message=f"Member {member_id} not found in committee {committee_id} members"
                                    ))
    
    def test_relationship_performance(self) -> None:
        """Test performance of complex relationship queries."""
        print("\n⚡ Testing Relationship Performance")
        
        # 1. Test pagination with relationships
        pagination_result = self.make_request(
            "/api/v1/members?size=50", 
            "Large Member List Performance"
        )
        self.log_test_result(pagination_result)
        
        # 2. Test filtering with relationships
        filter_result = self.make_request(
            "/api/v1/members?chamber=House&party=Republican",
            "Complex Filter Performance"
        )
        self.log_test_result(filter_result)
        
        # 3. Test search with relationships
        search_result = self.make_request(
            "/api/v1/members?search=John",
            "Search Performance"
        )
        self.log_test_result(search_result)
        
        # 4. Test committee filtering
        committee_filter_result = self.make_request(
            "/api/v1/committees?chamber=House",
            "Committee Filter Performance"
        )
        self.log_test_result(committee_filter_result)
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive relationship integrity testing."""
        print("🚀 Starting Comprehensive Relationship Integrity Testing")
        print(f"📅 Test started at: {self.start_time.isoformat()}")
        print(f"🌐 Base URL: {self.base_url}")
        
        # Run all test phases
        try:
            self.test_member_committee_relationships()
            self.test_committee_hierarchy()
            self.test_cross_reference_validation()
            self.test_relationship_performance()
        except Exception as e:
            print(f"❌ Test suite error: {str(e)}")
            traceback.print_exc()
        
        # Calculate summary statistics
        end_time = datetime.now(timezone.utc)
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.status == "PASS"])
        failed_tests = len([r for r in self.test_results if r.status == "FAIL"])
        error_tests = len([r for r in self.test_results if r.status == "ERROR"])
        
        avg_response_time = sum(r.response_time_ms for r in self.test_results) / total_tests if total_tests > 0 else 0
        max_response_time = max(r.response_time_ms for r in self.test_results) if total_tests > 0 else 0
        min_response_time = min(r.response_time_ms for r in self.test_results) if total_tests > 0 else 0
        
        # Print summary
        print(f"\n📊 RELATIONSHIP INTEGRITY TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"❌ Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"⚠️  Errors: {error_tests} ({error_tests/total_tests*100:.1f}%)")
        print(f"⏱️  Average Response Time: {avg_response_time:.2f}ms")
        print(f"⏱️  Max Response Time: {max_response_time:.2f}ms")
        print(f"⏱️  Min Response Time: {min_response_time:.2f}ms")
        print(f"🕐 Total Duration: {(end_time - self.start_time).total_seconds():.2f}s")
        
        # Return comprehensive results
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
            "test_results": [
                {
                    "test_name": r.test_name,
                    "endpoint": r.endpoint,
                    "status": r.status,
                    "response_time_ms": r.response_time_ms,
                    "details": r.details,
                    "error_message": r.error_message
                }
                for r in self.test_results
            ]
        }


def main():
    """Main function to run relationship integrity testing."""
    tester = RelationshipIntegrityTester()
    results = tester.run_comprehensive_test()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"relationship_integrity_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Return results for programmatic use
    return results


if __name__ == "__main__":
    main()