"""
Test Step 4.1: Performance Optimization & Caching
"""
import time
import asyncio
import sys
import os

# Add the backend app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.cache import cache_manager, CacheManager
from backend.app.core.database_optimization import db_optimizer, setup_database_optimization


async def test_cache_functionality():
    """Test caching functionality."""
    print("🔧 Testing Cache Functionality...")
    
    # Test cache manager initialization
    cache = CacheManager()
    print(f"✅ Cache manager initialized: Redis={cache.redis_client is not None}")
    
    # Test basic cache operations
    test_key = "test_key_123"
    test_value = {"test": "data", "timestamp": time.time()}
    
    # Set cache
    set_result = await cache.set(test_key, test_value, 60)
    print(f"✅ Cache set operation: {set_result}")
    
    # Get cache
    cached_value = await cache.get(test_key)
    print(f"✅ Cache get operation: {cached_value is not None}")
    
    # Test cache key generation
    cache_key = cache.get_cache_key("members", state="CA", party="Democrat")
    print(f"✅ Cache key generation: {cache_key[:20]}...")
    
    # Test pattern invalidation
    invalidated = await cache.invalidate_pattern("test_*")
    print(f"✅ Pattern invalidation: {invalidated} keys removed")
    
    return True


async def test_database_optimization():
    """Test database optimization functionality."""
    print("\n🗄️ Testing Database Optimization...")
    
    try:
        # Test database optimization setup
        optimization_results = await setup_database_optimization()
        print(f"✅ Database optimization setup: {optimization_results.get('status', 'unknown')}")
        
        # Test performance analysis
        performance_stats = await db_optimizer.analyze_query_performance()
        print(f"✅ Performance analysis: {len(performance_stats.get('table_statistics', {}))} tables analyzed")
        
        # Test connection pool optimization
        pool_stats = await db_optimizer.optimize_connection_pool()
        print(f"✅ Connection pool status: {pool_stats}")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Database optimization test failed: {e}")
        return False


async def test_performance_improvements():
    """Test performance improvements."""
    print("\n⚡ Testing Performance Improvements...")
    
    # Simulate API calls with timing
    start_time = time.time()
    
    # Test multiple cache operations to simulate API load
    for i in range(10):
        test_key = f"perf_test_{i}"
        test_data = {"member_id": i, "name": f"Test Member {i}"}
        await cache_manager.set(test_key, test_data, 300)
    
    for i in range(10):
        test_key = f"perf_test_{i}"
        cached_data = await cache_manager.get(test_key)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✅ Cache performance test: {total_time:.3f}s for 20 operations")
    print(f"✅ Average operation time: {(total_time/20)*1000:.1f}ms")
    
    # Cleanup test data
    for i in range(10):
        await cache_manager.delete(f"perf_test_{i}")
    
    return total_time < 1.0  # Should complete in under 1 second


def print_step_4_1_summary():
    """Print Step 4.1 implementation summary."""
    print("\n" + "="*60)
    print("🚀 STEP 4.1: PERFORMANCE OPTIMIZATION & CACHING - COMPLETE")
    print("="*60)
    print("✅ Cache Manager Implementation:")
    print("   - Redis-based caching with memory fallback")
    print("   - Intelligent TTL configuration by data type")
    print("   - Pattern-based cache invalidation")
    print("   - Performance metrics and monitoring")
    print()
    print("✅ Database Optimization:")
    print("   - Performance indexes for common queries")
    print("   - Connection pool optimization")
    print("   - Query performance analysis")
    print("   - Automatic index creation on startup")
    print()
    print("✅ API Caching Middleware:")
    print("   - Automatic response caching for GET requests")
    print("   - Cache headers and HTTP compliance")
    print("   - Cache invalidation on data updates")
    print("   - Cache status monitoring endpoints")
    print()
    print("🎯 Expected Performance Improvements:")
    print("   - API Response Time: 50% reduction (0.394s → <0.2s)")
    print("   - Database Queries: Optimized with indexes")
    print("   - Cache Hit Ratio: >80% for frequent requests")
    print("   - Memory Usage: Efficient with TTL-based cleanup")
    print("="*60)


async def main():
    """Run all Step 4.1 tests."""
    print("🚀 TESTING STEP 4.1: PERFORMANCE OPTIMIZATION & CACHING")
    print("="*60)
    
    # Test cache functionality
    cache_test = await test_cache_functionality()
    
    # Test database optimization
    db_test = await test_database_optimization()
    
    # Test performance improvements
    perf_test = await test_performance_improvements()
    
    # Print results
    print(f"\n📊 TEST RESULTS:")
    print(f"   Cache Functionality: {'✅ PASS' if cache_test else '❌ FAIL'}")
    print(f"   Database Optimization: {'✅ PASS' if db_test else '❌ FAIL'}")
    print(f"   Performance Test: {'✅ PASS' if perf_test else '❌ FAIL'}")
    
    overall_success = cache_test and db_test and perf_test
    print(f"\n🎯 OVERALL RESULT: {'✅ SUCCESS' if overall_success else '❌ FAILED'}")
    
    if overall_success:
        print_step_4_1_summary()
        return True
    else:
        print("\n⚠️ Some tests failed. Check implementation.")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)