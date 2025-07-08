#!/usr/bin/env python3
"""
Final Production Validation for Congressional Data API
Validates the current production deployment for Step 8 completion.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any

import httpx
import structlog

# Configure logging
logger = structlog.get_logger()

# Production API URL
PRODUCTION_API_URL = "https://congressional-data-api-v3-1066017671167.us-central1.run.app"
FRONTEND_URL = "https://storage.googleapis.com/congressional-data-frontend/index.html"

class ProductionValidator:
    """Validates production deployment."""
    
    def __init__(self):
        self.api_url = PRODUCTION_API_URL
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "api_url": self.api_url,
            "frontend_url": FRONTEND_URL,
            "tests": [],
            "summary": {}
        }
    
    async def run_validation(self) -> Dict[str, Any]:
        """Run comprehensive production validation."""
        logger.info("Starting production validation", api_url=self.api_url)
        
        # Test categories
        test_categories = [
            self.test_api_health,
            self.test_api_endpoints,
            self.test_data_quality,
            self.test_performance,
            self.test_congressional_data,
            self.test_search_functionality,
            self.test_pagination,
            self.test_error_handling
        ]
        
        # Run all tests
        for test_category in test_categories:
            try:
                await test_category()
            except Exception as e:
                logger.error(f"Test category failed: {test_category.__name__}", error=str(e))
                self.results["tests"].append({
                    "category": test_category.__name__,
                    "status": "FAILED",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Generate summary
        self.generate_summary()
        
        return self.results
    
    async def test_api_health(self):
        """Test API health endpoints."""
        logger.info("Testing API health")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Health check
            response = await client.get(f"{self.api_url}/health")
            assert response.status_code == 200
            health_data = response.json()
            assert health_data.get("status") == "healthy"
            
            self.results["tests"].append({
                "category": "api_health",
                "test": "health_endpoint",
                "status": "PASSED",
                "response_time": response.elapsed.total_seconds(),
                "data": health_data
            })
            
            # API root
            response = await client.get(f"{self.api_url}/")
            assert response.status_code == 200
            
            self.results["tests"].append({
                "category": "api_health",
                "test": "root_endpoint",
                "status": "PASSED", 
                "response_time": response.elapsed.total_seconds()
            })
    
    async def test_api_endpoints(self):
        """Test core API endpoints."""
        logger.info("Testing API endpoints")
        
        endpoints = [
            "/api/v1/members",
            "/api/v1/committees", 
            "/api/v1/hearings"
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for endpoint in endpoints:
                response = await client.get(f"{self.api_url}{endpoint}?limit=5")
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)
                assert len(data) <= 5
                
                self.results["tests"].append({
                    "category": "api_endpoints",
                    "test": endpoint,
                    "status": "PASSED",
                    "response_time": response.elapsed.total_seconds(),
                    "count": len(data)
                })
    
    async def test_data_quality(self):
        """Test data quality and completeness."""
        logger.info("Testing data quality")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test members data quality
            response = await client.get(f"{self.api_url}/api/v1/members?limit=10")
            members = response.json()
            
            # Validate member data structure
            required_fields = ["id", "bioguide_id", "first_name", "last_name", "party", "chamber"]
            for member in members:
                for field in required_fields:
                    assert field in member, f"Missing field {field} in member data"
                assert member["party"] in ["Democratic", "Republican", "Independent"]
                assert member["chamber"] in ["House", "Senate"]
            
            self.results["tests"].append({
                "category": "data_quality",
                "test": "member_data_structure",
                "status": "PASSED",
                "validated_records": len(members)
            })
            
            # Test committees data quality
            response = await client.get(f"{self.api_url}/api/v1/committees?limit=10")
            committees = response.json()
            
            required_fields = ["id", "name", "chamber"]
            for committee in committees:
                for field in required_fields:
                    assert field in committee, f"Missing field {field} in committee data"
                assert committee["chamber"] in ["House", "Senate", "Joint"]
            
            self.results["tests"].append({
                "category": "data_quality", 
                "test": "committee_data_structure",
                "status": "PASSED",
                "validated_records": len(committees)
            })
    
    async def test_performance(self):
        """Test API performance."""
        logger.info("Testing performance")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test response times
            start_time = time.time()
            
            tasks = []
            for i in range(10):
                task = client.get(f"{self.api_url}/api/v1/members?limit=20")
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            end_time = time.time()
            
            # Validate all responses
            for response in responses:
                assert response.status_code == 200
            
            avg_response_time = (end_time - start_time) / len(responses)
            
            self.results["tests"].append({
                "category": "performance",
                "test": "concurrent_requests",
                "status": "PASSED",
                "concurrent_requests": len(responses),
                "avg_response_time": avg_response_time,
                "total_time": end_time - start_time
            })
    
    async def test_congressional_data(self):
        """Test congressional data completeness."""
        logger.info("Testing congressional data completeness")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test total member count
            response = await client.get(f"{self.api_url}/api/v1/members")
            members = response.json()
            total_members = len(members)
            
            # Expected: at least 30 members for testing (production has 50)
            assert total_members >= 30, f"Expected at least 30 members, got {total_members}"
            
            # Test party distribution
            party_counts = {}
            chamber_counts = {}
            for member in members:
                party = member["party"]
                chamber = member["chamber"]
                party_counts[party] = party_counts.get(party, 0) + 1
                chamber_counts[chamber] = chamber_counts.get(chamber, 0) + 1
            
            self.results["tests"].append({
                "category": "congressional_data",
                "test": "member_completeness",
                "status": "PASSED",
                "total_members": total_members,
                "party_distribution": party_counts,
                "chamber_distribution": chamber_counts
            })
            
            # Test committees
            response = await client.get(f"{self.api_url}/api/v1/committees")
            committees = response.json()
            total_committees = len(committees)
            
            assert total_committees >= 20, f"Expected at least 20 committees, got {total_committees}"
            
            self.results["tests"].append({
                "category": "congressional_data",
                "test": "committee_completeness", 
                "status": "PASSED",
                "total_committees": total_committees
            })
    
    async def test_search_functionality(self):
        """Test search functionality."""
        logger.info("Testing search functionality")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test member search
            response = await client.get(f"{self.api_url}/api/v1/members?search=John")
            members = response.json()
            
            # Verify search results contain "John"
            for member in members:
                assert "john" in member["first_name"].lower() or "john" in member["last_name"].lower()
            
            self.results["tests"].append({
                "category": "search_functionality",
                "test": "member_search",
                "status": "PASSED",
                "search_term": "John",
                "results_count": len(members)
            })
            
            # Test filtering
            response = await client.get(f"{self.api_url}/api/v1/members?party=Republican&limit=10")
            members = response.json()
            
            for member in members:
                assert member["party"] == "Republican"
            
            self.results["tests"].append({
                "category": "search_functionality",
                "test": "party_filter",
                "status": "PASSED",
                "filter": "party=Republican",
                "results_count": len(members)
            })
    
    async def test_pagination(self):
        """Test pagination functionality."""
        logger.info("Testing pagination")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test different page sizes
            for limit in [5, 10, 20]:
                response = await client.get(f"{self.api_url}/api/v1/members?limit={limit}")
                members = response.json()
                assert len(members) == limit
                
                self.results["tests"].append({
                    "category": "pagination",
                    "test": f"limit_{limit}",
                    "status": "PASSED",
                    "requested_limit": limit,
                    "actual_count": len(members)
                })
    
    async def test_error_handling(self):
        """Test error handling."""
        logger.info("Testing error handling")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test invalid endpoint
            response = await client.get(f"{self.api_url}/api/v1/invalid_endpoint")
            assert response.status_code == 404
            
            self.results["tests"].append({
                "category": "error_handling",
                "test": "invalid_endpoint",
                "status": "PASSED",
                "status_code": response.status_code
            })
            
            # Test invalid parameter
            response = await client.get(f"{self.api_url}/api/v1/members?limit=invalid")
            # Should handle gracefully (might return default or error)
            assert response.status_code in [200, 400, 422]
            
            self.results["tests"].append({
                "category": "error_handling",
                "test": "invalid_parameter",
                "status": "PASSED",
                "status_code": response.status_code
            })
    
    def generate_summary(self):
        """Generate validation summary."""
        total_tests = len(self.results["tests"])
        passed_tests = len([t for t in self.results["tests"] if t.get("status") == "PASSED"])
        failed_tests = total_tests - passed_tests
        
        # Calculate average response time
        response_times = [t.get("response_time", 0) for t in self.results["tests"] if t.get("response_time")]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "avg_response_time": avg_response_time,
            "validation_status": "PASSED" if failed_tests == 0 else "FAILED"
        }


async def main():
    """Run production validation."""
    validator = ProductionValidator()
    results = await validator.run_validation()
    
    # Print results
    print("\n" + "="*80)
    print("CONGRESSIONAL DATA API - PRODUCTION VALIDATION RESULTS")
    print("="*80)
    
    print(f"\nAPI URL: {results['api_url']}")
    print(f"Frontend URL: {results['frontend_url']}")
    print(f"Validation Time: {results['timestamp']}")
    
    summary = results["summary"]
    print(f"\nSUMMARY:")
    print(f"  Total Tests: {summary['total_tests']}")
    print(f"  Passed: {summary['passed_tests']}")
    print(f"  Failed: {summary['failed_tests']}")
    print(f"  Success Rate: {summary['success_rate']:.1f}%")
    print(f"  Avg Response Time: {summary['avg_response_time']:.3f}s")
    print(f"  Overall Status: {summary['validation_status']}")
    
    # Print test details
    print(f"\nTEST DETAILS:")
    for test in results["tests"]:
        status = test.get("status", "UNKNOWN")
        test_name = test.get("test", test.get("category", "unnamed"))
        print(f"  ✅ {test_name}: {status}" if status == "PASSED" else f"  ❌ {test_name}: {status}")
    
    # Save results to file
    filename = f"production_validation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {filename}")
    
    if summary["validation_status"] == "PASSED":
        print("\n🎉 PRODUCTION VALIDATION SUCCESSFUL!")
        print("   Congressional Data API is ready for production use.")
    else:
        print("\n⚠️  PRODUCTION VALIDATION ISSUES DETECTED")
        print("   Please review failed tests before go-live.")
    
    print("\n" + "="*80)
    
    return results


if __name__ == "__main__":
    asyncio.run(main())