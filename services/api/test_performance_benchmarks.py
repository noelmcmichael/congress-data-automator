#!/usr/bin/env python3
"""
Performance and scalability testing script for Congressional Data API.
Tests response times, concurrent requests, and resource usage.

Phase 3B Step 9: Performance & Scalability Testing
"""

import json
import time
import asyncio
import aiohttp
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import requests
from dataclasses import dataclass
import statistics
import traceback
import psutil
import os


@dataclass
class PerformanceTest:
    """Performance test configuration."""
    name: str
    endpoint: str
    params: Optional[Dict[str, Any]] = None
    concurrent_requests: int = 1
    total_requests: int = 1
    test_category: str = "response_time"


class PerformanceTester:
    """Performance and scalability testing class."""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.test_results = []
        self.start_time = datetime.now(timezone.utc)
        
        # Define performance test suite
        self.performance_tests = self._define_performance_tests()
        
    def _define_performance_tests(self) -> List[PerformanceTest]:
        """Define comprehensive performance test suite."""
        return [
            # Basic Response Time Tests
            PerformanceTest("Health Check", "/health", None, 1, 10, "response_time"),
            PerformanceTest("Members List", "/api/v1/members", None, 1, 10, "response_time"),
            PerformanceTest("Committees List", "/api/v1/committees", None, 1, 10, "response_time"),
            PerformanceTest("Member Detail", "/api/v1/members/19", None, 1, 10, "response_time"),
            PerformanceTest("Committee Detail", "/api/v1/committees/1", None, 1, 10, "response_time"),
            
            # Pagination Performance Tests
            PerformanceTest("Small Page", "/api/v1/members", {"size": 5}, 1, 10, "pagination"),
            PerformanceTest("Medium Page", "/api/v1/members", {"size": 20}, 1, 10, "pagination"),
            PerformanceTest("Large Page", "/api/v1/members", {"size": 50}, 1, 10, "pagination"),
            PerformanceTest("Max Page", "/api/v1/members", {"size": 100}, 1, 10, "pagination"),
            
            # Filtering Performance Tests
            PerformanceTest("Chamber Filter", "/api/v1/members", {"chamber": "House"}, 1, 10, "filtering"),
            PerformanceTest("Party Filter", "/api/v1/members", {"party": "Republican"}, 1, 10, "filtering"),
            PerformanceTest("State Filter", "/api/v1/members", {"state": "CA"}, 1, 10, "filtering"),
            PerformanceTest("Complex Filter", "/api/v1/members", {"chamber": "House", "party": "Republican"}, 1, 10, "filtering"),
            
            # Search Performance Tests
            PerformanceTest("Name Search", "/api/v1/members", {"search": "John"}, 1, 10, "search"),
            PerformanceTest("Committee Search", "/api/v1/committees", {"search": "Agriculture"}, 1, 10, "search"),
            
            # Relationship Performance Tests
            PerformanceTest("Member Committees", "/api/v1/members/19/committees", None, 1, 10, "relationships"),
            PerformanceTest("Committee Members", "/api/v1/committees/1/members", None, 1, 10, "relationships"),
            PerformanceTest("Member Full Details", "/api/v1/members/19/full", None, 1, 10, "relationships"),
            
            # Concurrency Tests
            PerformanceTest("Concurrent Health", "/health", None, 5, 20, "concurrency"),
            PerformanceTest("Concurrent Members", "/api/v1/members", None, 5, 20, "concurrency"),
            PerformanceTest("Concurrent Detail", "/api/v1/members/19", None, 5, 20, "concurrency"),
            
            # Heavy Load Tests
            PerformanceTest("Heavy Members List", "/api/v1/members", None, 10, 50, "heavy_load"),
            PerformanceTest("Heavy Committees", "/api/v1/committees", None, 10, 50, "heavy_load"),
            PerformanceTest("Heavy Complex Filter", "/api/v1/members", {"chamber": "House", "party": "Republican"}, 10, 50, "heavy_load"),
        ]
    
    def run_single_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run a single request and measure performance."""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            success = response.status_code == 200
            
            # Try to get response size
            try:
                response_data = response.json()
                response_size = len(json.dumps(response_data))
                data_count = len(response_data.get("data", [])) if isinstance(response_data, dict) else 0
            except:
                response_size = len(response.text)
                data_count = 0
            
            return {
                "success": success,
                "response_time_ms": response_time,
                "status_code": response.status_code,
                "response_size": response_size,
                "data_count": data_count,
                "error": None
            }
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "response_time_ms": response_time,
                "status_code": 0,
                "response_size": 0,
                "data_count": 0,
                "error": str(e)
            }
    
    def run_concurrent_requests(self, endpoint: str, params: Optional[Dict[str, Any]], concurrent_count: int, total_requests: int) -> List[Dict[str, Any]]:
        """Run concurrent requests using threading."""
        results = []
        requests_per_thread = total_requests // concurrent_count
        remaining_requests = total_requests % concurrent_count
        
        def worker(thread_id: int, request_count: int):
            thread_results = []
            for i in range(request_count):
                result = self.run_single_request(endpoint, params)
                result["thread_id"] = thread_id
                result["request_number"] = i + 1
                thread_results.append(result)
            results.extend(thread_results)
        
        threads = []
        
        # Create threads
        for i in range(concurrent_count):
            request_count = requests_per_thread + (1 if i < remaining_requests else 0)
            thread = threading.Thread(target=worker, args=(i, request_count))
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # Add overall timing information
        for result in results:
            result["total_test_time_s"] = total_time
        
        return results
    
    def run_performance_test(self, test: PerformanceTest) -> Dict[str, Any]:
        """Run a single performance test."""
        print(f"  Running {test.name}...")
        
        # Record initial system metrics
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        initial_cpu = process.cpu_percent()
        
        # Run the test
        start_time = time.time()
        
        if test.concurrent_requests == 1:
            # Sequential requests
            results = []
            for i in range(test.total_requests):
                result = self.run_single_request(test.endpoint, test.params)
                result["request_number"] = i + 1
                results.append(result)
        else:
            # Concurrent requests
            results = self.run_concurrent_requests(test.endpoint, test.params, test.concurrent_requests, test.total_requests)
        
        total_time = time.time() - start_time
        
        # Record final system metrics
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        final_cpu = process.cpu_percent()
        
        # Calculate statistics
        response_times = [r["response_time_ms"] for r in results if r["success"]]
        successful_requests = len([r for r in results if r["success"]])
        failed_requests = len([r for r in results if not r["success"]])
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else max(response_times)
            p99_response_time = statistics.quantiles(response_times, n=100)[98] if len(response_times) >= 100 else max(response_times)
        else:
            avg_response_time = median_response_time = min_response_time = max_response_time = p95_response_time = p99_response_time = 0
        
        # Calculate throughput
        throughput = successful_requests / total_time if total_time > 0 else 0
        
        return {
            "test_name": test.name,
            "endpoint": test.endpoint,
            "category": test.test_category,
            "concurrent_requests": test.concurrent_requests,
            "total_requests": test.total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / test.total_requests) * 100,
            "total_time_s": total_time,
            "throughput_req_per_sec": throughput,
            "response_times": {
                "avg_ms": avg_response_time,
                "median_ms": median_response_time,
                "min_ms": min_response_time,
                "max_ms": max_response_time,
                "p95_ms": p95_response_time,
                "p99_ms": p99_response_time
            },
            "system_metrics": {
                "initial_memory_mb": initial_memory,
                "final_memory_mb": final_memory,
                "memory_delta_mb": final_memory - initial_memory,
                "initial_cpu_percent": initial_cpu,
                "final_cpu_percent": final_cpu
            },
            "raw_results": results
        }
    
    def run_comprehensive_performance_test(self) -> Dict[str, Any]:
        """Run comprehensive performance testing."""
        print("🚀 Starting Comprehensive Performance Testing")
        print(f"📅 Test started at: {self.start_time.isoformat()}")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🧪 Total performance tests: {len(self.performance_tests)}")
        
        # Get system info
        system_info = {
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": psutil.virtual_memory().total / 1024 / 1024 / 1024,
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
        }
        
        print(f"💻 System: {system_info['cpu_count']} CPUs, {system_info['memory_total_gb']:.1f}GB RAM")
        
        # Group tests by category
        categories = {}
        for test in self.performance_tests:
            category = test.test_category
            if category not in categories:
                categories[category] = []
            categories[category].append(test)
        
        # Run tests by category
        for category, tests in categories.items():
            print(f"\n🔍 Testing {category.upper()} performance ({len(tests)} tests)")
            
            category_results = []
            for test in tests:
                result = self.run_performance_test(test)
                self.test_results.append(result)
                category_results.append(result)
                
                # Print result summary
                print(f"  ✅ {result['test_name']}: {result['success_rate']:.1f}% success, {result['response_times']['avg_ms']:.2f}ms avg, {result['throughput_req_per_sec']:.2f} req/s")
            
            # Category summary
            avg_response_time = statistics.mean([r["response_times"]["avg_ms"] for r in category_results])
            avg_throughput = statistics.mean([r["throughput_req_per_sec"] for r in category_results])
            print(f"📊 {category.upper()} Summary: {avg_response_time:.2f}ms avg, {avg_throughput:.2f} req/s avg")
        
        # Calculate overall statistics
        end_time = datetime.now(timezone.utc)
        
        overall_stats = {
            "total_tests": len(self.test_results),
            "total_requests": sum(r["total_requests"] for r in self.test_results),
            "successful_requests": sum(r["successful_requests"] for r in self.test_results),
            "failed_requests": sum(r["failed_requests"] for r in self.test_results),
            "overall_success_rate": (sum(r["successful_requests"] for r in self.test_results) / sum(r["total_requests"] for r in self.test_results)) * 100,
            "avg_response_time_ms": statistics.mean([r["response_times"]["avg_ms"] for r in self.test_results]),
            "avg_throughput_req_per_sec": statistics.mean([r["throughput_req_per_sec"] for r in self.test_results]),
            "total_duration_s": (end_time - self.start_time).total_seconds()
        }
        
        # Print final summary
        print(f"\n📊 PERFORMANCE TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests: {overall_stats['total_tests']}")
        print(f"Total Requests: {overall_stats['total_requests']}")
        print(f"✅ Successful: {overall_stats['successful_requests']} ({overall_stats['overall_success_rate']:.1f}%)")
        print(f"❌ Failed: {overall_stats['failed_requests']}")
        print(f"⏱️  Average Response Time: {overall_stats['avg_response_time_ms']:.2f}ms")
        print(f"🚀 Average Throughput: {overall_stats['avg_throughput_req_per_sec']:.2f} req/s")
        print(f"🕐 Total Duration: {overall_stats['total_duration_s']:.2f}s")
        
        # Category performance breakdown
        print(f"\n📋 PERFORMANCE CATEGORY BREAKDOWN")
        for category in categories.keys():
            category_results = [r for r in self.test_results if r["category"] == category]
            avg_response_time = statistics.mean([r["response_times"]["avg_ms"] for r in category_results])
            avg_throughput = statistics.mean([r["throughput_req_per_sec"] for r in category_results])
            print(f"  {category.upper()}: {avg_response_time:.2f}ms avg, {avg_throughput:.2f} req/s avg")
        
        return {
            "test_summary": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "system_info": system_info,
                **overall_stats
            },
            "category_results": {
                category: {
                    "avg_response_time_ms": statistics.mean([r["response_times"]["avg_ms"] for r in self.test_results if r["category"] == category]),
                    "avg_throughput_req_per_sec": statistics.mean([r["throughput_req_per_sec"] for r in self.test_results if r["category"] == category]),
                    "total_tests": len([r for r in self.test_results if r["category"] == category])
                }
                for category in categories.keys()
            },
            "test_results": self.test_results
        }


def main():
    """Main function to run performance testing."""
    tester = PerformanceTester()
    results = tester.run_comprehensive_performance_test()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"performance_benchmarks_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()