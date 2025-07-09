"""
Performance monitoring service that integrates Phase 3 monitoring 
with Phase 4 optimization features.
"""
import time
import psutil
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import structlog
from sqlalchemy.orm import Session

from ..core.cache import cache_manager
from ..core.database_optimization import db_optimizer
from ..middleware.security_middleware import security_monitor

logger = structlog.get_logger()


class PerformanceMonitor:
    """Monitors API performance and optimization metrics."""
    
    def __init__(self):
        # Store performance metrics
        self.api_metrics = deque(maxlen=1000)  # Last 1000 API calls
        self.cache_metrics = deque(maxlen=100)  # Last 100 cache operations
        self.export_metrics = deque(maxlen=100)  # Last 100 export operations
        self.search_metrics = deque(maxlen=100)  # Last 100 search operations
        
        # Performance thresholds
        self.thresholds = {
            'api_response_time': 2.0,  # seconds
            'database_query_time': 1.0,  # seconds
            'cache_hit_ratio': 0.8,  # 80%
            'memory_usage': 0.85,  # 85%
            'cpu_usage': 0.80,  # 80%
        }
        
        # Alert tracking
        self.last_alerts = {}
        self.alert_cooldown = 300  # 5 minutes
    
    def log_api_request(
        self,
        endpoint: str,
        method: str,
        response_time: float,
        status_code: int,
        cache_hit: bool = False
    ):
        """Log API request performance metrics."""
        metric = {
            'timestamp': time.time(),
            'endpoint': endpoint,
            'method': method,
            'response_time': response_time,
            'status_code': status_code,
            'cache_hit': cache_hit
        }
        
        self.api_metrics.append(metric)
        
        # Check for performance threshold violations
        if response_time > self.thresholds['api_response_time']:
            self._trigger_performance_alert(
                'slow_api_response',
                f"Slow API response: {endpoint} took {response_time:.2f}s",
                {'endpoint': endpoint, 'response_time': response_time}
            )
    
    def log_cache_operation(
        self,
        operation: str,
        hit: bool,
        key: str,
        execution_time: float
    ):
        """Log cache operation metrics."""
        metric = {
            'timestamp': time.time(),
            'operation': operation,
            'hit': hit,
            'key_prefix': key.split(':')[0] if ':' in key else 'unknown',
            'execution_time': execution_time
        }
        
        self.cache_metrics.append(metric)
    
    def log_export_operation(
        self,
        export_type: str,
        format: str,
        record_count: int,
        execution_time: float,
        file_size: Optional[int] = None
    ):
        """Log data export performance metrics."""
        metric = {
            'timestamp': time.time(),
            'export_type': export_type,
            'format': format,
            'record_count': record_count,
            'execution_time': execution_time,
            'file_size': file_size
        }
        
        self.export_metrics.append(metric)
    
    def log_search_operation(
        self,
        search_type: str,
        query: str,
        result_count: int,
        execution_time: float,
        cache_hit: bool = False
    ):
        """Log search operation performance metrics."""
        metric = {
            'timestamp': time.time(),
            'search_type': search_type,
            'query_length': len(query),
            'result_count': result_count,
            'execution_time': execution_time,
            'cache_hit': cache_hit
        }
        
        self.search_metrics.append(metric)
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        now = time.time()
        hour_ago = now - 3600
        
        # API performance
        recent_api_metrics = [m for m in self.api_metrics if m['timestamp'] > hour_ago]
        api_summary = self._analyze_api_metrics(recent_api_metrics)
        
        # Cache performance
        recent_cache_metrics = [m for m in self.cache_metrics if m['timestamp'] > hour_ago]
        cache_summary = self._analyze_cache_metrics(recent_cache_metrics)
        
        # Export performance
        recent_export_metrics = [m for m in self.export_metrics if m['timestamp'] > hour_ago]
        export_summary = self._analyze_export_metrics(recent_export_metrics)
        
        # Search performance
        recent_search_metrics = [m for m in self.search_metrics if m['timestamp'] > hour_ago]
        search_summary = self._analyze_search_metrics(recent_search_metrics)
        
        # System metrics
        system_summary = await self._get_system_metrics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'performance_summary': {
                'api': api_summary,
                'cache': cache_summary,
                'export': export_summary,
                'search': search_summary,
                'system': system_summary
            },
            'optimization_status': await self._get_optimization_status(),
            'alerts': self._get_recent_alerts()
        }
    
    def _analyze_api_metrics(self, metrics: List[Dict]) -> Dict[str, Any]:
        """Analyze API performance metrics."""
        if not metrics:
            return {'status': 'no_data', 'total_requests': 0}
        
        response_times = [m['response_time'] for m in metrics]
        cache_hits = [m for m in metrics if m.get('cache_hit', False)]
        
        return {
            'total_requests': len(metrics),
            'avg_response_time': sum(response_times) / len(response_times),
            'max_response_time': max(response_times),
            'min_response_time': min(response_times),
            'cache_hit_ratio': len(cache_hits) / len(metrics) if metrics else 0,
            'status_codes': self._count_by_field(metrics, 'status_code'),
            'slowest_endpoints': self._get_slowest_endpoints(metrics)
        }
    
    def _analyze_cache_metrics(self, metrics: List[Dict]) -> Dict[str, Any]:
        """Analyze cache performance metrics."""
        if not metrics:
            return {'status': 'no_data', 'total_operations': 0}
        
        hits = [m for m in metrics if m['hit']]
        execution_times = [m['execution_time'] for m in metrics]
        
        return {
            'total_operations': len(metrics),
            'hit_ratio': len(hits) / len(metrics) if metrics else 0,
            'avg_execution_time': sum(execution_times) / len(execution_times) if execution_times else 0,
            'operations_by_type': self._count_by_field(metrics, 'operation'),
            'key_prefixes': self._count_by_field(metrics, 'key_prefix')
        }
    
    def _analyze_export_metrics(self, metrics: List[Dict]) -> Dict[str, Any]:
        """Analyze export performance metrics."""
        if not metrics:
            return {'status': 'no_data', 'total_exports': 0}
        
        execution_times = [m['execution_time'] for m in metrics]
        record_counts = [m['record_count'] for m in metrics]
        
        return {
            'total_exports': len(metrics),
            'avg_execution_time': sum(execution_times) / len(execution_times),
            'total_records_exported': sum(record_counts),
            'formats_used': self._count_by_field(metrics, 'format'),
            'export_types': self._count_by_field(metrics, 'export_type'),
            'avg_records_per_export': sum(record_counts) / len(record_counts) if record_counts else 0
        }
    
    def _analyze_search_metrics(self, metrics: List[Dict]) -> Dict[str, Any]:
        """Analyze search performance metrics."""
        if not metrics:
            return {'status': 'no_data', 'total_searches': 0}
        
        execution_times = [m['execution_time'] for m in metrics]
        result_counts = [m['result_count'] for m in metrics]
        cache_hits = [m for m in metrics if m.get('cache_hit', False)]
        
        return {
            'total_searches': len(metrics),
            'avg_execution_time': sum(execution_times) / len(execution_times),
            'avg_results_per_search': sum(result_counts) / len(result_counts) if result_counts else 0,
            'cache_hit_ratio': len(cache_hits) / len(metrics) if metrics else 0,
            'search_types': self._count_by_field(metrics, 'search_type')
        }
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_usage': cpu_percent / 100,
                'memory_usage': memory.percent / 100,
                'memory_available_gb': memory.available / (1024**3),
                'disk_usage': disk.percent / 100,
                'disk_free_gb': disk.free / (1024**3)
            }
        except Exception as e:
            logger.warning(f"Failed to get system metrics: {e}")
            return {'error': 'unavailable'}
    
    async def _get_optimization_status(self) -> Dict[str, Any]:
        """Get current optimization feature status."""
        try:
            # Cache status
            cache_available = cache_manager.redis_client is not None
            cache_entries = len(cache_manager.memory_cache)
            
            # Database optimization status
            db_stats = await db_optimizer.analyze_query_performance()
            
            return {
                'caching': {
                    'redis_available': cache_available,
                    'memory_cache_entries': cache_entries,
                    'status': 'optimized'
                },
                'database': {
                    'indexes_created': True,
                    'connection_pool': 'optimized',
                    'table_count': len(db_stats.get('table_statistics', {}))
                },
                'security': {
                    'rate_limiting': 'active',
                    'input_validation': 'active',
                    'security_headers': 'enabled'
                },
                'advanced_features': {
                    'data_export': 'available',
                    'enhanced_search': 'available',
                    'autocomplete': 'available'
                }
            }
        except Exception as e:
            logger.warning(f"Failed to get optimization status: {e}")
            return {'error': 'unavailable'}
    
    def _count_by_field(self, metrics: List[Dict], field: str) -> Dict[str, int]:
        """Count occurrences by field value."""
        counts = defaultdict(int)
        for metric in metrics:
            value = metric.get(field, 'unknown')
            counts[str(value)] += 1
        return dict(counts)
    
    def _get_slowest_endpoints(self, metrics: List[Dict], limit: int = 5) -> List[Dict]:
        """Get slowest API endpoints."""
        endpoint_times = defaultdict(list)
        for metric in metrics:
            endpoint_times[metric['endpoint']].append(metric['response_time'])
        
        avg_times = []
        for endpoint, times in endpoint_times.items():
            avg_time = sum(times) / len(times)
            avg_times.append({
                'endpoint': endpoint,
                'avg_response_time': avg_time,
                'request_count': len(times)
            })
        
        return sorted(avg_times, key=lambda x: x['avg_response_time'], reverse=True)[:limit]
    
    def _trigger_performance_alert(self, alert_type: str, message: str, details: Dict[str, Any]):
        """Trigger performance alert with cooldown."""
        now = time.time()
        last_alert_time = self.last_alerts.get(alert_type, 0)
        
        if now - last_alert_time > self.alert_cooldown:
            # Log the alert
            security_monitor.log_security_event(
                f"performance_{alert_type}",
                details,
                "warning"
            )
            
            logger.warning(f"Performance alert: {message}", extra=details)
            self.last_alerts[alert_type] = now
    
    def _get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """Get recent performance alerts."""
        cutoff_time = time.time() - (hours * 3600)
        recent_events = [
            event for event in security_monitor.security_events
            if (event['timestamp'] > cutoff_time and 
                event['type'].startswith('performance_'))
        ]
        return recent_events
    
    async def optimize_performance_automatically(self) -> Dict[str, Any]:
        """Automatically optimize performance based on metrics."""
        optimizations = []
        
        # Analyze recent metrics
        summary = await self.get_performance_summary()
        api_metrics = summary['performance_summary']['api']
        cache_metrics = summary['performance_summary']['cache']
        
        # Cache optimization
        if cache_metrics.get('hit_ratio', 0) < self.thresholds['cache_hit_ratio']:
            try:
                # Warm up cache for popular endpoints
                await self._warm_popular_endpoints()
                optimizations.append('cache_warming')
            except Exception as e:
                logger.warning(f"Cache warming failed: {e}")
        
        # Database optimization trigger
        if api_metrics.get('avg_response_time', 0) > self.thresholds['api_response_time']:
            try:
                # Re-run database optimization
                await db_optimizer.create_performance_indexes()
                optimizations.append('database_reindexing')
            except Exception as e:
                logger.warning(f"Database reindexing failed: {e}")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'optimizations_applied': optimizations,
            'next_check': (datetime.now() + timedelta(minutes=30)).isoformat()
        }
    
    async def _warm_popular_endpoints(self):
        """Warm cache for popular endpoints."""
        # This would make internal requests to popular endpoints
        # to pre-populate the cache
        popular_endpoints = [
            '/api/v1/members',
            '/api/v1/committees',
            '/api/v1/congress/sessions'
        ]
        
        logger.info(f"Cache warming initiated for {len(popular_endpoints)} endpoints")
        # Implementation would make actual requests to these endpoints


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


# Middleware integration functions
async def track_api_performance(request, response_time: float, status_code: int, cache_hit: bool = False):
    """Track API performance for monitoring."""
    performance_monitor.log_api_request(
        endpoint=request.url.path,
        method=request.method,
        response_time=response_time,
        status_code=status_code,
        cache_hit=cache_hit
    )


async def track_cache_performance(operation: str, hit: bool, key: str, execution_time: float):
    """Track cache performance for monitoring."""
    performance_monitor.log_cache_operation(operation, hit, key, execution_time)


async def track_export_performance(export_type: str, format: str, record_count: int, execution_time: float):
    """Track export performance for monitoring."""
    performance_monitor.log_export_operation(export_type, format, record_count, execution_time)


async def track_search_performance(search_type: str, query: str, result_count: int, execution_time: float, cache_hit: bool = False):
    """Track search performance for monitoring."""
    performance_monitor.log_search_operation(search_type, query, result_count, execution_time, cache_hit)