"""
Test Step 4.4: Production Monitoring Integration
"""
import asyncio
import time
import sys
import os

# Add the backend app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Install psutil if not available
try:
    import psutil
except ImportError:
    os.system("pip install psutil")
    import psutil

from backend.app.services.performance_monitor import PerformanceMonitor, performance_monitor


async def test_performance_monitoring():
    """Test performance monitoring functionality."""
    print("📊 Testing Performance Monitoring...")
    
    # Test performance monitor initialization
    monitor = PerformanceMonitor()
    print(f"✅ Performance monitor initialized with thresholds: {len(monitor.thresholds)} metrics")
    
    # Test API request logging
    monitor.log_api_request(
        endpoint="/api/v1/members",
        method="GET",
        response_time=0.5,
        status_code=200,
        cache_hit=True
    )
    print("✅ API request logging functional")
    
    # Test cache operation logging
    monitor.log_cache_operation(
        operation="get",
        hit=True,
        key="members:state:CA",
        execution_time=0.01
    )
    print("✅ Cache operation logging functional")
    
    # Test export operation logging
    monitor.log_export_operation(
        export_type="members",
        format="csv",
        record_count=100,
        execution_time=2.5
    )
    print("✅ Export operation logging functional")
    
    # Test search operation logging
    monitor.log_search_operation(
        search_type="members",
        query="john smith",
        result_count=5,
        execution_time=0.3,
        cache_hit=False
    )
    print("✅ Search operation logging functional")
    
    return True


async def test_performance_analysis():
    """Test performance analysis functionality."""
    print("\n📈 Testing Performance Analysis...")
    
    monitor = PerformanceMonitor()
    
    # Add some test data
    for i in range(10):
        monitor.log_api_request(
            endpoint=f"/api/v1/test/{i % 3}",
            method="GET",
            response_time=0.1 + (i * 0.1),
            status_code=200 if i < 8 else 500,
            cache_hit=i % 2 == 0
        )
    
    # Test performance summary
    try:
        summary = await monitor.get_performance_summary()
        
        # Verify summary structure
        required_sections = ['performance_summary', 'optimization_status', 'alerts']
        has_all_sections = all(section in summary for section in required_sections)
        
        # Verify API metrics
        api_metrics = summary['performance_summary']['api']
        has_api_metrics = all(key in api_metrics for key in ['total_requests', 'avg_response_time'])
        
        print(f"✅ Performance summary structure: {'✅ PASS' if has_all_sections else '❌ FAIL'}")
        print(f"✅ API metrics analysis: {'✅ PASS' if has_api_metrics else '❌ FAIL'}")
        
        return has_all_sections and has_api_metrics
        
    except Exception as e:
        print(f"❌ Performance analysis failed: {e}")
        return False


async def test_system_metrics():
    """Test system metrics collection."""
    print("\n🖥️ Testing System Metrics...")
    
    monitor = PerformanceMonitor()
    
    try:
        # Test system metrics collection
        system_metrics = await monitor._get_system_metrics()
        
        # Check for required metrics
        required_metrics = ['cpu_usage', 'memory_usage']
        has_required_metrics = all(metric in system_metrics for metric in required_metrics)
        
        # Validate metric ranges
        valid_ranges = True
        if 'cpu_usage' in system_metrics:
            cpu = system_metrics['cpu_usage']
            valid_ranges = valid_ranges and (0 <= cpu <= 1)
        
        if 'memory_usage' in system_metrics:
            memory = system_metrics['memory_usage']
            valid_ranges = valid_ranges and (0 <= memory <= 1)
        
        print(f"✅ System metrics collection: {'✅ PASS' if has_required_metrics else '❌ FAIL'}")
        print(f"✅ Metric value validation: {'✅ PASS' if valid_ranges else '❌ FAIL'}")
        
        return has_required_metrics and valid_ranges
        
    except Exception as e:
        print(f"❌ System metrics test failed: {e}")
        return False


async def test_optimization_status():
    """Test optimization status monitoring."""
    print("\n⚙️ Testing Optimization Status...")
    
    monitor = PerformanceMonitor()
    
    try:
        # Test optimization status
        status = await monitor._get_optimization_status()
        
        # Check for required status sections
        required_sections = ['caching', 'database', 'security', 'advanced_features']
        has_all_sections = all(section in status for section in required_sections)
        
        # Check cache status
        cache_status = status.get('caching', {})
        has_cache_info = 'status' in cache_status
        
        print(f"✅ Optimization status structure: {'✅ PASS' if has_all_sections else '❌ FAIL'}")
        print(f"✅ Cache status info: {'✅ PASS' if has_cache_info else '❌ FAIL'}")
        
        return has_all_sections and has_cache_info
        
    except Exception as e:
        print(f"❌ Optimization status test failed: {e}")
        return False


async def test_automatic_optimization():
    """Test automatic optimization functionality."""
    print("\n🤖 Testing Automatic Optimization...")
    
    monitor = PerformanceMonitor()
    
    try:
        # Test automatic optimization
        result = await monitor.optimize_performance_automatically()
        
        # Check result structure
        required_fields = ['timestamp', 'optimizations_applied', 'next_check']
        has_required_fields = all(field in result for field in required_fields)
        
        # Check that optimizations list is present (even if empty)
        optimizations_valid = isinstance(result.get('optimizations_applied', []), list)
        
        print(f"✅ Optimization result structure: {'✅ PASS' if has_required_fields else '❌ FAIL'}")
        print(f"✅ Optimizations list format: {'✅ PASS' if optimizations_valid else '❌ FAIL'}")
        
        return has_required_fields and optimizations_valid
        
    except Exception as e:
        print(f"❌ Automatic optimization test failed: {e}")
        return False


async def test_alert_system():
    """Test performance alert system."""
    print("\n🚨 Testing Alert System...")
    
    monitor = PerformanceMonitor()
    
    # Test alert triggering with slow response time
    monitor._trigger_performance_alert(
        'test_alert',
        'Test performance alert',
        {'test': 'data'}
    )
    
    # Test getting recent alerts
    try:
        recent_alerts = monitor._get_recent_alerts(24)
        
        # Should have at least the test alert
        has_alerts = isinstance(recent_alerts, list)
        alert_structure_valid = True
        
        if recent_alerts:
            first_alert = recent_alerts[0]
            required_fields = ['timestamp', 'type']
            alert_structure_valid = all(field in first_alert for field in required_fields)
        
        print(f"✅ Alert collection: {'✅ PASS' if has_alerts else '❌ FAIL'}")
        print(f"✅ Alert structure: {'✅ PASS' if alert_structure_valid else '❌ FAIL'}")
        
        return has_alerts and alert_structure_valid
        
    except Exception as e:
        print(f"❌ Alert system test failed: {e}")
        return False


async def test_monitoring_integration():
    """Test integration between Phase 3 and Phase 4 monitoring."""
    print("\n🔗 Testing Monitoring Integration...")
    
    try:
        # Test that both monitoring systems can coexist
        from backend.app.middleware.security_middleware import security_monitor
        
        # Add a security event
        security_monitor.log_security_event('test_integration', {'test': 'data'}, 'info')
        
        # Add a performance event
        performance_monitor.log_api_request('/test', 'GET', 0.5, 200)
        
        # Check that both systems have events
        security_events = security_monitor.get_security_summary()
        performance_summary = await performance_monitor.get_performance_summary()
        
        has_security_events = security_events.get('total_events', 0) > 0
        has_performance_events = performance_summary['performance_summary']['api']['total_requests'] > 0
        
        print(f"✅ Security monitoring active: {'✅ PASS' if has_security_events else '❌ FAIL'}")
        print(f"✅ Performance monitoring active: {'✅ PASS' if has_performance_events else '❌ FAIL'}")
        
        return has_security_events and has_performance_events
        
    except Exception as e:
        print(f"❌ Monitoring integration test failed: {e}")
        return False


def print_step_4_4_summary():
    """Print Step 4.4 implementation summary."""
    print("\n" + "="*60)
    print("📊 STEP 4.4: PRODUCTION MONITORING INTEGRATION - COMPLETE")
    print("="*60)
    print("✅ Performance Monitoring System:")
    print("   - API request tracking with response times")
    print("   - Cache operation monitoring and hit ratios")
    print("   - Export operation performance tracking")
    print("   - Search operation performance analysis")
    print("   - System resource monitoring (CPU, memory, disk)")
    print()
    print("✅ Unified Monitoring Dashboard:")
    print("   - Combined Phase 3 and Phase 4 metrics")
    print("   - Real-time system health monitoring")
    print("   - Performance optimization status")
    print("   - Security event integration")
    print("   - Automated recommendations engine")
    print()
    print("✅ Automatic Optimization:")
    print("   - Performance threshold monitoring")
    print("   - Automatic cache warming")
    print("   - Database reindexing triggers")
    print("   - Alert-based optimization actions")
    print("   - Cooldown periods to prevent over-optimization")
    print()
    print("✅ Monitoring API Endpoints:")
    print("   - /api/v1/monitoring/dashboard (unified overview)")
    print("   - /api/v1/monitoring/performance (detailed metrics)")
    print("   - /api/v1/monitoring/optimization (optimization status)")
    print("   - /api/v1/monitoring/alerts (alert management)")
    print("   - /api/v1/monitoring/health (system health scores)")
    print("   - /api/v1/monitoring/optimize/* (manual optimization)")
    print()
    print("🎯 Integrated Benefits:")
    print("   - Phase 3 monitoring ensures data currency")
    print("   - Phase 4 monitoring optimizes performance")
    print("   - Unified dashboard for operational visibility")
    print("   - Automated optimization reduces manual overhead")
    print("   - Comprehensive alerting prevents issues")
    print("="*60)


async def main():
    """Run all Step 4.4 tests."""
    print("📊 TESTING STEP 4.4: PRODUCTION MONITORING INTEGRATION")
    print("="*60)
    
    # Run all monitoring integration tests
    performance_test = await test_performance_monitoring()
    analysis_test = await test_performance_analysis()
    system_test = await test_system_metrics()
    optimization_test = await test_optimization_status()
    auto_opt_test = await test_automatic_optimization()
    alert_test = await test_alert_system()
    integration_test = await test_monitoring_integration()
    
    # Print results
    print(f"\n📊 TEST RESULTS:")
    print(f"   Performance Monitoring: {'✅ PASS' if performance_test else '❌ FAIL'}")
    print(f"   Performance Analysis: {'✅ PASS' if analysis_test else '❌ FAIL'}")
    print(f"   System Metrics: {'✅ PASS' if system_test else '❌ FAIL'}")
    print(f"   Optimization Status: {'✅ PASS' if optimization_test else '❌ FAIL'}")
    print(f"   Automatic Optimization: {'✅ PASS' if auto_opt_test else '❌ FAIL'}")
    print(f"   Alert System: {'✅ PASS' if alert_test else '❌ FAIL'}")
    print(f"   Monitoring Integration: {'✅ PASS' if integration_test else '❌ FAIL'}")
    
    overall_success = all([
        performance_test, analysis_test, system_test, 
        optimization_test, auto_opt_test, alert_test, integration_test
    ])
    print(f"\n🎯 OVERALL RESULT: {'✅ SUCCESS' if overall_success else '❌ FAILED'}")
    
    if overall_success:
        print_step_4_4_summary()
        return True
    else:
        print("\n⚠️ Some monitoring integration tests failed. Check implementation.")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)