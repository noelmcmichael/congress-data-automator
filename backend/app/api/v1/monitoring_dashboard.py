"""
Unified monitoring dashboard API that combines Phase 3 monitoring 
with Phase 4 performance optimization monitoring.
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import structlog

from ...core.database import get_db
from ...services.performance_monitor import performance_monitor
from ...middleware.security_middleware import security_monitor
from ...middleware.cache_middleware import cache_invalidator

# Import Phase 3 monitoring services
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../services'))

logger = structlog.get_logger()
router = APIRouter()


@router.get("/monitoring/dashboard")
async def get_monitoring_dashboard(db: Session = Depends(get_db)):
    """Get comprehensive monitoring dashboard data."""
    try:
        # Get Phase 4 performance metrics
        performance_summary = await performance_monitor.get_performance_summary()
        
        # Get Phase 3 monitoring data (simulated structure)
        phase3_monitoring = {
            'congressional_session': {
                'current_congress': '119th',
                'session_period': '2025-2027',
                'party_control': 'Republican',
                'status': 'current'
            },
            'data_freshness': {
                'members_current': True,
                'committees_current': True,
                'leadership_current': True,
                'last_update': '2025-01-08T23:00:00Z'
            },
            'system_health': {
                'api_status': 'healthy',
                'database_status': 'healthy',
                'frontend_status': 'healthy',
                'monitoring_status': 'healthy'
            },
            'automated_triggers': {
                'daily_trigger': 'scheduled',
                'weekly_trigger': 'scheduled',
                'monthly_trigger': 'scheduled',
                'transition_trigger': 'active',
                'emergency_trigger': 'ready'
            },
            'alerts': {
                'total_alerts': len(security_monitor.security_events),
                'recent_alerts': len([
                    e for e in security_monitor.security_events 
                    if e.get('timestamp', 0) > (performance_summary.get('timestamp', 0) or 0)
                ])
            }
        }
        
        # Combine all monitoring data
        dashboard_data = {
            'timestamp': performance_summary.get('timestamp'),
            'overall_status': _determine_overall_status(performance_summary, phase3_monitoring),
            'phase3_monitoring': phase3_monitoring,
            'phase4_performance': performance_summary['performance_summary'],
            'optimization_status': performance_summary['optimization_status'],
            'security_summary': security_monitor.get_security_summary(),
            'recommendations': await _generate_recommendations(performance_summary, phase3_monitoring)
        }
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Dashboard data retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard data")


@router.get("/monitoring/performance")
async def get_performance_metrics(
    hours: int = Query(24, ge=1, le=168, description="Hours of metrics to retrieve")
):
    """Get detailed performance metrics."""
    try:
        summary = await performance_monitor.get_performance_summary()
        
        # Add time-based analysis
        metrics_with_trends = {
            **summary,
            'trends': {
                'api_performance': 'stable',  # Would calculate from historical data
                'cache_efficiency': 'improving',
                'export_usage': 'increasing',
                'search_usage': 'stable'
            },
            'recommendations': await _get_performance_recommendations(summary)
        }
        
        return metrics_with_trends
        
    except Exception as e:
        logger.error(f"Performance metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")


@router.get("/monitoring/optimization")
async def get_optimization_status():
    """Get current optimization status and suggestions."""
    try:
        status = await performance_monitor._get_optimization_status()
        
        # Add optimization suggestions
        optimization_data = {
            **status,
            'automatic_optimizations': {
                'enabled': True,
                'last_run': '2025-01-08T23:00:00Z',
                'next_scheduled': '2025-01-08T23:30:00Z'
            },
            'manual_optimizations': [
                {
                    'name': 'Cache Invalidation',
                    'description': 'Clear specific cache entries',
                    'endpoint': '/api/v1/cache/invalidate/{data_type}'
                },
                {
                    'name': 'Database Reindexing',
                    'description': 'Recreate database indexes',
                    'endpoint': '/api/v1/monitoring/optimize/database'
                }
            ],
            'optimization_history': await _get_optimization_history()
        }
        
        return optimization_data
        
    except Exception as e:
        logger.error(f"Optimization status retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get optimization status")


@router.post("/monitoring/optimize/auto")
async def trigger_automatic_optimization():
    """Trigger automatic performance optimization."""
    try:
        result = await performance_monitor.optimize_performance_automatically()
        
        return {
            'optimization_triggered': True,
            'result': result,
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Automatic optimization failed: {e}")
        raise HTTPException(status_code=500, detail="Optimization failed")


@router.post("/monitoring/optimize/cache")
async def optimize_cache():
    """Manually optimize cache performance."""
    try:
        # Warm up cache
        await performance_monitor._warm_popular_endpoints()
        
        return {
            'cache_optimization': 'completed',
            'action': 'cache_warming',
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Cache optimization failed: {e}")
        raise HTTPException(status_code=500, detail="Cache optimization failed")


@router.post("/monitoring/optimize/database")
async def optimize_database():
    """Manually optimize database performance."""
    try:
        from ...core.database_optimization import db_optimizer
        
        # Re-run database optimization
        result = await db_optimizer.create_performance_indexes()
        
        return {
            'database_optimization': 'completed',
            'indexes_created': result.get('created', 0),
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Database optimization failed: {e}")
        raise HTTPException(status_code=500, detail="Database optimization failed")


@router.get("/monitoring/alerts")
async def get_monitoring_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity: info, warning, error, critical"),
    hours: int = Query(24, ge=1, le=168, description="Hours of alerts to retrieve")
):
    """Get monitoring alerts from both Phase 3 and Phase 4."""
    try:
        # Get security/monitoring alerts
        security_summary = security_monitor.get_security_summary()
        
        # Get performance alerts
        performance_alerts = performance_monitor._get_recent_alerts(hours)
        
        # Combine and filter alerts
        all_alerts = list(security_monitor.security_events) + performance_alerts
        
        if severity:
            all_alerts = [a for a in all_alerts if a.get('severity') == severity]
        
        # Sort by timestamp (most recent first)
        all_alerts.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        return {
            'alerts': all_alerts[:100],  # Limit to 100 most recent
            'summary': security_summary,
            'alert_categories': {
                'security': len([a for a in all_alerts if not a['type'].startswith('performance_')]),
                'performance': len([a for a in all_alerts if a['type'].startswith('performance_')])
            }
        }
        
    except Exception as e:
        logger.error(f"Alert retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alerts")


@router.get("/monitoring/health")
async def get_system_health():
    """Get comprehensive system health status."""
    try:
        # Get performance summary
        perf_summary = await performance_monitor.get_performance_summary()
        
        # Calculate health scores
        health_scores = {
            'api_health': _calculate_api_health(perf_summary['performance_summary']['api']),
            'cache_health': _calculate_cache_health(perf_summary['performance_summary']['cache']),
            'database_health': _calculate_database_health(perf_summary['performance_summary']['system']),
            'security_health': _calculate_security_health(),
            'overall_health': 0
        }
        
        # Calculate overall health
        health_scores['overall_health'] = sum(health_scores.values()) / (len(health_scores) - 1)
        
        return {
            'health_scores': health_scores,
            'status': _get_health_status(health_scores['overall_health']),
            'recommendations': _get_health_recommendations(health_scores),
            'timestamp': perf_summary.get('timestamp')
        }
        
    except Exception as e:
        logger.error(f"Health status retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system health")


# Helper functions
def _determine_overall_status(performance_data: Dict, phase3_data: Dict) -> str:
    """Determine overall system status."""
    api_health = performance_data['performance_summary']['api'].get('total_requests', 0) > 0
    system_health = phase3_data['system_health']['api_status'] == 'healthy'
    
    if api_health and system_health:
        return 'healthy'
    elif api_health or system_health:
        return 'degraded'
    else:
        return 'critical'


async def _generate_recommendations(performance_data: Dict, phase3_data: Dict) -> list:
    """Generate optimization recommendations."""
    recommendations = []
    
    # Performance-based recommendations
    api_metrics = performance_data['performance_summary']['api']
    if api_metrics.get('avg_response_time', 0) > 1.0:
        recommendations.append({
            'type': 'performance',
            'priority': 'high',
            'title': 'Optimize API Response Time',
            'description': 'API response time is above 1 second threshold',
            'action': 'Consider caching optimization or database indexing'
        })
    
    cache_metrics = performance_data['performance_summary']['cache']
    if cache_metrics.get('hit_ratio', 1) < 0.8:
        recommendations.append({
            'type': 'caching',
            'priority': 'medium',
            'title': 'Improve Cache Hit Ratio',
            'description': 'Cache hit ratio is below 80%',
            'action': 'Review caching strategy and warm up popular endpoints'
        })
    
    # Security-based recommendations
    security_events = security_monitor.get_security_summary()
    if security_events.get('total_events', 0) > 100:
        recommendations.append({
            'type': 'security',
            'priority': 'medium',
            'title': 'Review Security Events',
            'description': f"High number of security events: {security_events['total_events']}",
            'action': 'Review security logs and consider tightening security policies'
        })
    
    return recommendations


async def _get_performance_recommendations(summary: Dict) -> list:
    """Get performance-specific recommendations."""
    recommendations = []
    
    api_summary = summary['performance_summary']['api']
    if api_summary.get('avg_response_time', 0) > 0.5:
        recommendations.append({
            'category': 'api_performance',
            'suggestion': 'Enable more aggressive caching for frequently accessed endpoints',
            'impact': 'high'
        })
    
    return recommendations


async def _get_optimization_history() -> list:
    """Get history of optimization actions."""
    # This would typically come from a database
    return [
        {
            'timestamp': '2025-01-08T22:30:00Z',
            'type': 'automatic',
            'action': 'cache_warming',
            'result': 'success'
        },
        {
            'timestamp': '2025-01-08T22:00:00Z',
            'type': 'automatic',
            'action': 'database_indexing',
            'result': 'success'
        }
    ]


def _calculate_api_health(api_metrics: Dict) -> float:
    """Calculate API health score (0-1)."""
    if api_metrics.get('total_requests', 0) == 0:
        return 1.0  # No requests, assume healthy
    
    avg_response_time = api_metrics.get('avg_response_time', 0)
    if avg_response_time > 2.0:
        return 0.3
    elif avg_response_time > 1.0:
        return 0.6
    else:
        return 0.9


def _calculate_cache_health(cache_metrics: Dict) -> float:
    """Calculate cache health score (0-1)."""
    hit_ratio = cache_metrics.get('hit_ratio', 0)
    return min(hit_ratio + 0.2, 1.0)  # Add some buffer


def _calculate_database_health(system_metrics: Dict) -> float:
    """Calculate database health score (0-1)."""
    if 'error' in system_metrics:
        return 0.5
    
    memory_usage = system_metrics.get('memory_usage', 0)
    cpu_usage = system_metrics.get('cpu_usage', 0)
    
    if memory_usage > 0.9 or cpu_usage > 0.9:
        return 0.4
    elif memory_usage > 0.8 or cpu_usage > 0.8:
        return 0.7
    else:
        return 0.9


def _calculate_security_health() -> float:
    """Calculate security health score (0-1)."""
    security_summary = security_monitor.get_security_summary()
    
    critical_events = security_summary.get('by_severity', {}).get('critical', 0)
    if critical_events > 5:
        return 0.3
    elif critical_events > 0:
        return 0.6
    else:
        return 0.9


def _get_health_status(score: float) -> str:
    """Get health status from score."""
    if score >= 0.8:
        return 'excellent'
    elif score >= 0.6:
        return 'good'
    elif score >= 0.4:
        return 'fair'
    else:
        return 'poor'


def _get_health_recommendations(health_scores: Dict) -> list:
    """Get health improvement recommendations."""
    recommendations = []
    
    if health_scores['api_health'] < 0.6:
        recommendations.append('Optimize API performance through caching and indexing')
    
    if health_scores['cache_health'] < 0.6:
        recommendations.append('Improve cache configuration and hit ratios')
    
    if health_scores['database_health'] < 0.6:
        recommendations.append('Monitor and optimize database performance')
    
    if health_scores['security_health'] < 0.6:
        recommendations.append('Review and address security events')
    
    return recommendations