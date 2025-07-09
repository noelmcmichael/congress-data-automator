#!/usr/bin/env python3
"""
Priority 1: API Fix Validation Script
====================================

Comprehensive validation of Congressional Data API after database password fix.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

class APIValidator:
    def __init__(self):
        self.api_base = "https://politicalequity.io/api/v1"
        self.validation_start = datetime.now()
        self.results = {
            "validation_start": self.validation_start.isoformat(),
            "api_base": self.api_base,
            "tests": {}
        }
        
    def test_endpoint(self, endpoint: str, expected_status: int = 200, **params):
        """Test an API endpoint with optional parameters"""
        try:
            url = f"{self.api_base}{endpoint}"
            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Try to parse JSON if successful
            data = None
            if response.status_code == 200:
                try:
                    data = response.json()
                except:
                    data = "Non-JSON response"
            
            return {
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "success": response.status_code == expected_status,
                "data_count": len(data) if isinstance(data, list) else None,
                "data_type": type(data).__name__ if data else None,
                "error": None
            }
        except Exception as e:
            return {
                "status_code": None,
                "response_time_ms": None,
                "success": False,
                "data_count": None,
                "data_type": None,
                "error": str(e)
            }
    
    def run_validation(self):
        """Run comprehensive API validation"""
        
        print("🔍 Priority 1: API Fix Validation")
        print("=" * 50)
        
        # 1. Status endpoint
        print("\n1. Testing status endpoint...")
        self.results["tests"]["status"] = self.test_endpoint("/status")
        status_result = self.results["tests"]["status"]
        if status_result["success"]:
            print(f"   ✅ Status: {status_result['status_code']} ({status_result['response_time_ms']}ms)")
        else:
            print(f"   ❌ Status failed: {status_result.get('error', status_result['status_code'])}")
        
        # 2. Committees endpoint (default pagination)
        print("\n2. Testing committees endpoint (default pagination)...")
        self.results["tests"]["committees_default"] = self.test_endpoint("/committees")
        committees_result = self.results["tests"]["committees_default"]
        if committees_result["success"]:
            print(f"   ✅ Committees (default): {committees_result['data_count']} committees ({committees_result['response_time_ms']}ms)")
        else:
            print(f"   ❌ Committees failed: {committees_result.get('error', committees_result['status_code'])}")
        
        # 3. Committees endpoint (full dataset)
        print("\n3. Testing committees endpoint (full dataset)...")
        self.results["tests"]["committees_full"] = self.test_endpoint("/committees", limit=200)
        committees_full_result = self.results["tests"]["committees_full"]
        if committees_full_result["success"]:
            print(f"   ✅ Committees (full): {committees_full_result['data_count']} committees ({committees_full_result['response_time_ms']}ms)")
        else:
            print(f"   ❌ Committees (full) failed: {committees_full_result.get('error', committees_full_result['status_code'])}")
        
        # 4. Chamber filtering
        print("\n4. Testing chamber filtering...")
        self.results["tests"]["committees_house"] = self.test_endpoint("/committees", chamber="House", limit=200)
        house_result = self.results["tests"]["committees_house"]
        if house_result["success"]:
            print(f"   ✅ House committees: {house_result['data_count']} committees ({house_result['response_time_ms']}ms)")
        else:
            print(f"   ❌ House committees failed: {house_result.get('error', house_result['status_code'])}")
        
        self.results["tests"]["committees_senate"] = self.test_endpoint("/committees", chamber="Senate", limit=200)
        senate_result = self.results["tests"]["committees_senate"]
        if senate_result["success"]:
            print(f"   ✅ Senate committees: {senate_result['data_count']} committees ({senate_result['response_time_ms']}ms)")
        else:
            print(f"   ❌ Senate committees failed: {senate_result.get('error', senate_result['status_code'])}")
        
        # 5. Members endpoint
        print("\n5. Testing members endpoint...")
        self.results["tests"]["members"] = self.test_endpoint("/members")
        members_result = self.results["tests"]["members"]
        if members_result["success"]:
            print(f"   ✅ Members: {members_result['data_count']} members ({members_result['response_time_ms']}ms)")
        else:
            print(f"   ❌ Members failed: {members_result.get('error', members_result['status_code'])}")
        
        # 6. Performance validation
        print("\n6. Performance validation...")
        response_times = []
        for test_name, test_result in self.results["tests"].items():
            if test_result.get("response_time_ms"):
                response_times.append(test_result["response_time_ms"])
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            self.results["performance"] = {
                "average_response_time_ms": round(avg_response_time, 2),
                "max_response_time_ms": max_response_time,
                "under_200ms": all(rt < 200 for rt in response_times)
            }
            print(f"   ⏱️ Average response time: {avg_response_time:.1f}ms")
            print(f"   ⏱️ Maximum response time: {max_response_time:.1f}ms")
            if self.results["performance"]["under_200ms"]:
                print("   ✅ All response times under 200ms")
            else:
                print("   ⚠️ Some response times exceed 200ms")
        
        # 7. Data consistency validation
        print("\n7. Data consistency validation...")
        total_committees = committees_full_result.get("data_count", 0)
        house_committees = house_result.get("data_count", 0)
        senate_committees = senate_result.get("data_count", 0)
        
        if total_committees == house_committees + senate_committees:
            print(f"   ✅ Committee counts consistent: {total_committees} = {house_committees} (House) + {senate_committees} (Senate)")
            self.results["data_consistency"] = {"consistent": True, "total": total_committees, "house": house_committees, "senate": senate_committees}
        else:
            print(f"   ⚠️ Committee count mismatch: {total_committees} ≠ {house_committees} + {senate_committees}")
            self.results["data_consistency"] = {"consistent": False, "total": total_committees, "house": house_committees, "senate": senate_committees}
        
        # 8. Success summary
        print("\n8. Success summary...")
        successful_tests = sum(1 for test in self.results["tests"].values() if test.get("success", False))
        total_tests = len(self.results["tests"])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        self.results["summary"] = {
            "successful_tests": successful_tests,
            "total_tests": total_tests,
            "success_rate": round(success_rate, 1),
            "validation_end": datetime.now().isoformat()
        }
        
        print(f"   📊 Success rate: {successful_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 95:
            print("   🎉 API validation PASSED")
            self.results["validation_status"] = "PASSED"
        else:
            print("   ❌ API validation FAILED")
            self.results["validation_status"] = "FAILED"
        
        return self.results
    
    def save_results(self, filename: str = None):
        """Save validation results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"priority1_api_validation_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Results saved to: {filename}")
        return filename

def main():
    validator = APIValidator()
    results = validator.run_validation()
    validator.save_results()
    
    # Final status
    if results["validation_status"] == "PASSED":
        print("\n🎯 Priority 1: API Fix - COMPLETED SUCCESSFULLY")
        print("   All endpoints functional and performant")
        print("   Ready to proceed to Priority 2: Committee Expansion")
    else:
        print("\n⚠️ Priority 1: API Fix - NEEDS ATTENTION")
        print("   Some endpoints may require additional fixes")

if __name__ == "__main__":
    main()