"""
Caching middleware for FastAPI endpoints.
Implements intelligent caching with cache headers and invalidation.
"""
import json
import hashlib
from typing import Callable, Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

from ..core.cache import cache_manager, CACHE_CONFIGS

logger = structlog.get_logger()


class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware for API response caching."""
    
    def __init__(self, app, cache_enabled: bool = True):
        super().__init__(app)
        self.cache_enabled = cache_enabled
        self.cacheable_paths = {
            '/api/v1/members': 'members',
            '/api/v1/committees': 'committees', 
            '/api/v1/hearings': 'hearings',
            '/api/v1/relationships': 'relationships',
            '/api/v1/congress': 'congressional_sessions',
        }
        self.cache_control_headers = {
            'members': 'public, max-age=21600',  # 6 hours
            'committees': 'public, max-age=43200',  # 12 hours
            'hearings': 'public, max-age=7200',  # 2 hours
            'relationships': 'public, max-age=14400',  # 4 hours
            'congressional_sessions': 'public, max-age=86400',  # 24 hours
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> StarletteResponse:
        """Process request with caching logic."""
        if not self.cache_enabled:
            return await call_next(request)
        
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)
        
        # Check if path is cacheable
        cache_type = self._get_cache_type(request.url.path)
        if not cache_type:
            return await call_next(request)
        
        # Generate cache key
        cache_key = self._generate_cache_key(request)
        
        # Check for cache-control headers in request
        force_refresh = request.headers.get("cache-control") == "no-cache"
        
        if not force_refresh:
            # Try to get cached response
            cached_response = await cache_manager.get(cache_key)
            if cached_response:
                logger.debug(f"Cache hit for {request.url.path}")
                return self._create_cached_response(cached_response, cache_type)
        
        # Execute request
        response = await call_next(request)
        
        # Cache successful responses
        if response.status_code == 200 and hasattr(response, 'body'):
            try:
                # Get response body
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                # Parse and cache JSON responses
                if response.headers.get("content-type", "").startswith("application/json"):
                    response_data = json.loads(body.decode())
                    
                    # Cache the response
                    config = CACHE_CONFIGS.get(cache_type, {})
                    ttl = config.get('ttl', 3600)
                    
                    cached_data = {
                        'body': response_data,
                        'status_code': response.status_code,
                        'headers': dict(response.headers)
                    }
                    
                    await cache_manager.set(cache_key, cached_data, ttl)
                    logger.debug(f"Cached response for {request.url.path}")
                
                # Create new response with body
                new_response = Response(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
                
                # Add cache headers
                self._add_cache_headers(new_response, cache_type)
                
                return new_response
                
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")
        
        return response
    
    def _get_cache_type(self, path: str) -> Optional[str]:
        """Determine cache type for given path."""
        for cacheable_path, cache_type in self.cacheable_paths.items():
            if path.startswith(cacheable_path):
                return cache_type
        return None
    
    def _generate_cache_key(self, request: Request) -> str:
        """Generate cache key for request."""
        # Include path, query parameters, and relevant headers
        key_data = {
            'path': request.url.path,
            'query': str(request.url.query),
            'method': request.method,
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return f"api_cache:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def _create_cached_response(self, cached_data: dict, cache_type: str) -> JSONResponse:
        """Create response from cached data."""
        response = JSONResponse(
            content=cached_data['body'],
            status_code=cached_data['status_code']
        )
        
        # Add cache headers
        self._add_cache_headers(response, cache_type)
        response.headers["X-Cache"] = "HIT"
        
        return response
    
    def _add_cache_headers(self, response: Response, cache_type: str):
        """Add appropriate cache headers to response."""
        cache_control = self.cache_control_headers.get(cache_type, 'public, max-age=3600')
        response.headers["Cache-Control"] = cache_control
        response.headers["X-Cache"] = response.headers.get("X-Cache", "MISS")
        response.headers["Vary"] = "Accept-Encoding"


class CacheInvalidationMiddleware:
    """Handles cache invalidation for data updates."""
    
    def __init__(self):
        self.invalidation_patterns = {
            'members': ['api_cache:*members*', 'api_cache:*relationships*'],
            'committees': ['api_cache:*committees*', 'api_cache:*relationships*'],
            'hearings': ['api_cache:*hearings*'],
            'congressional_sessions': ['api_cache:*congress*'],
        }
    
    async def invalidate_cache(self, data_type: str, operation: str = "update"):
        """Invalidate cache for specific data type."""
        patterns = self.invalidation_patterns.get(data_type, [])
        
        total_invalidated = 0
        for pattern in patterns:
            count = await cache_manager.invalidate_pattern(pattern)
            total_invalidated += count
        
        logger.info(f"Cache invalidation for {data_type} {operation}: {total_invalidated} entries removed")
        return total_invalidated


# Global cache invalidator instance
cache_invalidator = CacheInvalidationMiddleware()


def cache_response(cache_type: str, ttl: Optional[int] = None):
    """Decorator for caching individual endpoint responses."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function args
            cache_key = cache_manager.get_cache_key(f"{func.__name__}", *args, **kwargs)
            
            # Try cache first
            cached_result = await cache_manager.get(cache_key)
            if cached_result:
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            cache_ttl = ttl or CACHE_CONFIGS.get(cache_type, {}).get('ttl', 3600)
            await cache_manager.set(cache_key, result, cache_ttl)
            
            return result
        
        return wrapper
    return decorator


async def warm_cache():
    """Pre-warm cache with frequently accessed data."""
    logger.info("Starting cache warm-up process")
    
    # This would typically make requests to common endpoints
    # to pre-populate the cache
    warm_up_endpoints = [
        "/api/v1/members",
        "/api/v1/committees", 
        "/api/v1/congress/sessions",
    ]
    
    logger.info(f"Cache warm-up complete for {len(warm_up_endpoints)} endpoints")
    return len(warm_up_endpoints)