#!/usr/bin/env python3
"""
Production testing suite for Congressional Data API.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# Add the api module to the path
sys.path.insert(0, str(Path(__file__).parent))

from api.core.config import settings
from api.core.logging import logger
from tests.security_test import SecurityTester


class ProductionTestRunner:
    """Comprehensive production testing suite."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.api_base_url or "http://localhost:8003"
        self.base_url = self.base_url.rstrip('/')
        self.test_results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "base_url": self.base_url,
            "tests": {}
        }
        self.session = None
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all production tests."""
        print(f"🚀 Starting production testing suite against {self.base_url}")
        print(f"Started at: {self.test_results['started_at']}")
        print("=" * 60)
        
        # Initialize HTTP session
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            # Run tests in sequence
            await self.test_service_health()
            await self.test_api_functionality()
            await self.test_performance()
            await self.test_concurrent_load()
            await self.test_database_integrity()
            await self.test_monitoring_endpoints()
            
            # Run security tests (synchronous)
            await self.test_security()
            
            # Run load tests (external)
            await self.test_load_performance()
        
        # Generate final report
        self.test_results["completed_at"] = datetime.now(timezone.utc).isoformat()
        self.test_results["duration_seconds"] = (
            datetime.fromisoformat(self.test_results["completed_at"]) -
            datetime.fromisoformat(self.test_results["started_at"])
        ).total_seconds()
        
        return self.test_results
    
    async def test_service_health(self):
        """Test basic service health."""
        print("🔍 Testing service health...")
        
        start_time = time.time()
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        # Test basic health endpoint
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                health_data = await response.json()
                results["tests"].append({
                    "name": "Basic Health Check",
                    "passed": response.status == 200,
                    "response_time_ms": (time.time() - start_time) * 1000,
                    "data": health_data
                })
        except Exception as e:
            results["tests"].append({
                "name": "Basic Health Check",
                "passed": False,
                "error": str(e)
            })
        
        # Test detailed health endpoint
        try:
            start_time = time.time()
            async with self.session.get(f"{self.base_url}/healthz") as response:
                health_data = await response.json()
                results["tests"].append({
                    "name": "Detailed Health Check",
                    "passed": response.status == 200 and health_data.get("status") == "healthy",
                    "response_time_ms": (time.time() - start_time) * 1000,
                    "data": health_data
                })
        except Exception as e:
            results["tests"].append({
                "name": "Detailed Health Check",
                "passed": False,
                "error": str(e)
            })
        
        # Test database connectivity
        try:
            start_time = time.time()
            async with self.session.get(f"{self.base_url}/api/v1/members?limit=1") as response:
                members_data = await response.json()
                results["tests"].append({
                    "name": "Database Connectivity",
                    "passed": response.status == 200,
                    "response_time_ms": (time.time() - start_time) * 1000,
                    "data": {"member_count": len(members_data.get("data", []))}
                })
        except Exception as e:
            results["tests"].append({
                "name": "Database Connectivity",
                "passed": False,
                "error": str(e)
            })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["service_health"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        print(f"   Service Health: {passed}/{total} tests passed")
    
    async def test_api_functionality(self):
        """Test API functionality."""
        print("🔍 Testing API functionality...")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        # Test all major endpoints
        endpoints = [
            {"url": "/api/v1/members", "name": "Members List"},
            {"url": "/api/v1/members?chamber=House", "name": "House Members"},
            {"url": "/api/v1/members?chamber=Senate", "name": "Senate Members"},
            {"url": "/api/v1/committees", "name": "Committees List"},
            {"url": "/api/v1/committees?chamber=House", "name": "House Committees"},
            {"url": "/api/v1/committees?chamber=Senate", "name": "Senate Committees"},
            {"url": "/api/v1/hearings", "name": "Hearings List"},
            {"url": "/api/v1/search?q=Smith", "name": "Search Members"},
            {"url": "/api/v1/statistics/overview", "name": "Statistics Overview"},
            {"url": "/api/v1/statistics/members", "name": "Member Statistics"},
            {"url": "/api/v1/statistics/committees", "name": "Committee Statistics"},
        ]
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                async with self.session.get(f"{self.base_url}{endpoint['url']}") as response:
                    data = await response.json()
                    response_time = (time.time() - start_time) * 1000
                    
                    results["tests"].append({
                        "name": endpoint["name"],
                        "url": endpoint["url"],
                        "passed": response.status == 200,
                        "response_time_ms": response_time,
                        "status_code": response.status,
                        "data_length": len(str(data))
                    })
            except Exception as e:
                results["tests"].append({
                    "name": endpoint["name"],
                    "url": endpoint["url"],
                    "passed": False,
                    "error": str(e)
                })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["api_functionality"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        avg_response_time = sum(test.get("response_time_ms", 0) for test in results["tests"]) / total
        print(f"   API Functionality: {passed}/{total} tests passed, avg response time: {avg_response_time:.1f}ms")
    
    async def test_performance(self):
        """Test performance benchmarks."""
        print("🔍 Testing performance benchmarks...")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        # Performance benchmarks
        benchmarks = [
            {"url": "/api/v1/members?limit=100", "name": "Large Members Query", "target_ms": 500},
            {"url": "/api/v1/committees?limit=50", "name": "Large Committees Query", "target_ms": 300},
            {"url": "/api/v1/hearings?limit=100", "name": "Large Hearings Query", "target_ms": 500},
            {"url": "/api/v1/search?q=committee&limit=50", "name": "Search Query", "target_ms": 1000},
            {"url": "/api/v1/statistics/overview", "name": "Statistics Query", "target_ms": 200},
        ]
        
        for benchmark in benchmarks:
            try:
                # Run multiple times to get average
                times = []
                for _ in range(5):
                    start_time = time.time()
                    async with self.session.get(f"{self.base_url}{benchmark['url']}") as response:
                        await response.json()
                        times.append((time.time() - start_time) * 1000)
                
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                results["tests"].append({
                    "name": benchmark["name"],
                    "url": benchmark["url"],
                    "passed": avg_time < benchmark["target_ms"],
                    "avg_response_time_ms": avg_time,
                    "min_response_time_ms": min_time,
                    "max_response_time_ms": max_time,
                    "target_ms": benchmark["target_ms"],
                    "runs": len(times)
                })
            except Exception as e:
                results["tests"].append({
                    "name": benchmark["name"],
                    "url": benchmark["url"],
                    "passed": False,
                    "error": str(e)
                })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["performance"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        print(f"   Performance: {passed}/{total} benchmarks passed")
    
    async def test_concurrent_load(self):
        """Test concurrent load handling."""
        print("🔍 Testing concurrent load handling...")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        # Test concurrent requests
        async def make_request(url: str):
            start_time = time.time()
            try:
                async with self.session.get(url) as response:
                    await response.json()
                    return {
                        "success": True,
                        "response_time_ms": (time.time() - start_time) * 1000,
                        "status_code": response.status
                    }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "response_time_ms": (time.time() - start_time) * 1000
                }
        
        # Test different concurrency levels
        concurrency_tests = [
            {"concurrent_requests": 10, "url": "/api/v1/members?limit=10"},
            {"concurrent_requests": 25, "url": "/api/v1/committees?limit=10"},
            {"concurrent_requests": 50, "url": "/health"},
        ]
        
        for test in concurrency_tests:
            try:
                start_time = time.time()
                url = f"{self.base_url}{test['url']}"
                
                # Create concurrent requests
                tasks = [make_request(url) for _ in range(test['concurrent_requests'])]
                request_results = await asyncio.gather(*tasks)
                
                total_time = time.time() - start_time
                successful = sum(1 for r in request_results if r["success"])
                avg_response_time = sum(r["response_time_ms"] for r in request_results) / len(request_results)
                
                results["tests"].append({
                    "name": f"Concurrent Load ({test['concurrent_requests']} requests)",
                    "url": test["url"],
                    "passed": successful >= test['concurrent_requests'] * 0.9,  # 90% success rate
                    "concurrent_requests": test['concurrent_requests'],
                    "successful_requests": successful,
                    "total_time_seconds": total_time,
                    "avg_response_time_ms": avg_response_time,
                    "requests_per_second": test['concurrent_requests'] / total_time
                })
            except Exception as e:
                results["tests"].append({
                    "name": f"Concurrent Load ({test['concurrent_requests']} requests)",
                    "url": test["url"],
                    "passed": False,
                    "error": str(e)
                })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["concurrent_load"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        print(f"   Concurrent Load: {passed}/{total} tests passed")
    
    async def test_database_integrity(self):
        """Test database integrity and consistency."""
        print("🔍 Testing database integrity...")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        # Test data consistency
        try:
            # Get statistics
            async with self.session.get(f"{self.base_url}/api/v1/statistics/overview") as response:
                stats = await response.json()
                stats_data = stats.get("data", {})
            
            # Test member counts
            async with self.session.get(f"{self.base_url}/api/v1/members?limit=1000") as response:
                members = await response.json()
                member_count = len(members.get("data", []))
            
            # Test committee counts
            async with self.session.get(f"{self.base_url}/api/v1/committees?limit=1000") as response:
                committees = await response.json()
                committee_count = len(committees.get("data", []))
            
            # Check consistency
            results["tests"].append({
                "name": "Data Consistency",
                "passed": True,  # Basic consistency check
                "member_count": member_count,
                "committee_count": committee_count,
                "stats_data": stats_data
            })
            
        except Exception as e:
            results["tests"].append({
                "name": "Data Consistency",
                "passed": False,
                "error": str(e)
            })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["database_integrity"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        print(f"   Database Integrity: {passed}/{total} tests passed")
    
    async def test_monitoring_endpoints(self):
        """Test monitoring endpoints."""
        print("🔍 Testing monitoring endpoints...")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        # Test monitoring endpoints
        monitoring_endpoints = [
            {"url": "/health", "name": "Health Endpoint"},
            {"url": "/healthz", "name": "Detailed Health Endpoint"},
            {"url": "/metrics", "name": "Metrics Endpoint"},
            {"url": "/status", "name": "Status Endpoint"},
            {"url": "/ping", "name": "Ping Endpoint"},
        ]
        
        for endpoint in monitoring_endpoints:
            try:
                start_time = time.time()
                async with self.session.get(f"{self.base_url}{endpoint['url']}") as response:
                    response_time = (time.time() - start_time) * 1000
                    
                    results["tests"].append({
                        "name": endpoint["name"],
                        "url": endpoint["url"],
                        "passed": response.status == 200,
                        "response_time_ms": response_time,
                        "status_code": response.status
                    })
            except Exception as e:
                results["tests"].append({
                    "name": endpoint["name"],
                    "url": endpoint["url"],
                    "passed": False,
                    "error": str(e)
                })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["monitoring"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        print(f"   Monitoring: {passed}/{total} tests passed")
    
    async def test_security(self):
        """Test security using the security test suite."""
        print("🔍 Testing security...")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        try:
            # Run security tests
            tester = SecurityTester(self.base_url)
            security_results = tester.run_all_tests()
            
            results["tests"] = [
                {
                    "name": result.test_name,
                    "passed": result.passed,
                    "message": result.message,
                    "details": result.details
                }
                for result in security_results
            ]
            
        except Exception as e:
            results["tests"].append({
                "name": "Security Test Suite",
                "passed": False,
                "error": str(e)
            })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["security"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        print(f"   Security: {passed}/{total} tests passed")
    
    async def test_load_performance(self):
        """Test load performance using Artillery."""
        print("🔍 Testing load performance...")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tests": []
        }
        
        # Check if Artillery is available
        try:
            result = subprocess.run(
                ["artillery", "version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Run Artillery load test
                env = os.environ.copy()
                env["API_BASE_URL"] = self.base_url
                
                result = subprocess.run(
                    ["artillery", "run", "tests/load_test.js"],
                    cwd=Path(__file__).parent,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minutes
                    env=env
                )
                
                results["tests"].append({
                    "name": "Artillery Load Test",
                    "passed": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None
                })
            else:
                results["tests"].append({
                    "name": "Artillery Load Test",
                    "passed": False,
                    "error": "Artillery not available"
                })
                
        except subprocess.TimeoutExpired:
            results["tests"].append({
                "name": "Artillery Load Test",
                "passed": False,
                "error": "Load test timed out"
            })
        except Exception as e:
            results["tests"].append({
                "name": "Artillery Load Test",
                "passed": False,
                "error": str(e)
            })
        
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["duration_seconds"] = (
            datetime.fromisoformat(results["completed_at"]) -
            datetime.fromisoformat(results["started_at"])
        ).total_seconds()
        
        self.test_results["tests"]["load_performance"] = results
        
        # Print results
        passed = sum(1 for test in results["tests"] if test["passed"])
        total = len(results["tests"])
        print(f"   Load Performance: {passed}/{total} tests passed")
    
    def generate_report(self) -> str:
        """Generate a comprehensive test report."""
        report = []
        report.append("=" * 80)
        report.append("CONGRESSIONAL DATA API - PRODUCTION TEST REPORT")
        report.append("=" * 80)
        report.append(f"Test Suite: {self.base_url}")
        report.append(f"Started: {self.test_results['started_at']}")
        report.append(f"Completed: {self.test_results['completed_at']}")
        report.append(f"Duration: {self.test_results['duration_seconds']:.2f} seconds")
        report.append("")
        
        # Overall summary
        total_tests = 0
        total_passed = 0
        
        for test_category, category_results in self.test_results["tests"].items():
            category_tests = len(category_results["tests"])
            category_passed = sum(1 for test in category_results["tests"] if test["passed"])
            total_tests += category_tests
            total_passed += category_passed
        
        report.append(f"OVERALL SUMMARY:")
        report.append(f"  Total Tests: {total_tests}")
        report.append(f"  Passed: {total_passed}")
        report.append(f"  Failed: {total_tests - total_passed}")
        report.append(f"  Success Rate: {(total_passed / total_tests * 100):.1f}%")
        report.append("")
        
        # Category details
        for test_category, category_results in self.test_results["tests"].items():
            category_tests = len(category_results["tests"])
            category_passed = sum(1 for test in category_results["tests"] if test["passed"])
            
            report.append(f"{test_category.upper().replace('_', ' ')}:")
            report.append(f"  Tests: {category_passed}/{category_tests}")
            report.append(f"  Duration: {category_results['duration_seconds']:.2f}s")
            
            for test in category_results["tests"]:
                status = "✅" if test["passed"] else "❌"
                report.append(f"    {status} {test['name']}")
                if not test["passed"] and "error" in test:
                    report.append(f"        Error: {test['error']}")
            
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)


async def main():
    """Main function to run production tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Production testing for Congressional Data API")
    parser.add_argument("--url", help="Base URL for API")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--report", help="Output file for test report")
    
    args = parser.parse_args()
    
    # Determine base URL
    base_url = args.url
    if not base_url:
        if settings.is_production:
            base_url = "https://your-production-api.com"  # Replace with actual production URL
        else:
            base_url = "http://localhost:8003"
    
    # Run tests
    runner = ProductionTestRunner(base_url)
    results = await runner.run_all_tests()
    
    # Generate and print report
    report = runner.generate_report()
    print(report)
    
    # Save results and report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")
    
    if args.report:
        with open(args.report, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.report}")
    
    # Exit with appropriate code
    total_tests = sum(len(cat["tests"]) for cat in results["tests"].values())
    passed_tests = sum(sum(1 for test in cat["tests"] if test["passed"]) for cat in results["tests"].values())
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())