"""
Caching layer for Congressional Data Automation Service.
Implements Redis-based caching with fallback to in-memory caching.
"""
import json
import hashlib
from typing import Any, Optional, Union, Dict
from datetime import datetime, timedelta
import redis
import structlog
from .config import settings

logger = structlog.get_logger()


class CacheManager:
    """Manages caching operations with Redis and in-memory fallback."""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.memory_cache_ttl: Dict[str, datetime] = {}
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection with fallback handling."""
        try:
            if hasattr(settings, 'redis_url') and settings.redis_url:
                self.redis_client = redis.from_url(
                    settings.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # Test connection
                self.redis_client.ping()
                logger.info("Redis cache initialized successfully")
            else:
                logger.warning("Redis URL not configured, using in-memory cache only")
        except Exception as e:
            logger.warning(f"Redis connection failed, using in-memory cache: {e}")
            self.redis_client = None
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from prefix and parameters."""
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return f"congress_api:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def _cleanup_memory_cache(self):
        """Remove expired entries from memory cache."""
        now = datetime.now()
        expired_keys = [
            key for key, expiry in self.memory_cache_ttl.items()
            if expiry < now
        ]
        for key in expired_keys:
            self.memory_cache.pop(key, None)
            self.memory_cache_ttl.pop(key, None)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            # Try Redis first
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            
            # Fallback to memory cache
            self._cleanup_memory_cache()
            if key in self.memory_cache:
                if key in self.memory_cache_ttl and self.memory_cache_ttl[key] > datetime.now():
                    return self.memory_cache[key]['value']
                else:
                    # Expired
                    self.memory_cache.pop(key, None)
                    self.memory_cache_ttl.pop(key, None)
            
            return None
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """Set value in cache with TTL."""
        try:
            serialized_value = json.dumps(value, default=str)
            
            # Try Redis first
            if self.redis_client:
                success = self.redis_client.setex(key, ttl_seconds, serialized_value)
                if success:
                    return True
            
            # Fallback to memory cache
            self.memory_cache[key] = {'value': value}
            self.memory_cache_ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)
            return True
            
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            deleted = False
            
            # Delete from Redis
            if self.redis_client:
                deleted = bool(self.redis_client.delete(key))
            
            # Delete from memory cache
            if key in self.memory_cache:
                self.memory_cache.pop(key, None)
                self.memory_cache_ttl.pop(key, None)
                deleted = True
            
            return deleted
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        try:
            deleted_count = 0
            
            # Redis pattern deletion
            if self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    deleted_count = self.redis_client.delete(*keys)
            
            # Memory cache pattern deletion
            matching_keys = [key for key in self.memory_cache.keys() if pattern.replace('*', '') in key]
            for key in matching_keys:
                self.memory_cache.pop(key, None)
                self.memory_cache_ttl.pop(key, None)
                deleted_count += 1
            
            logger.info(f"Invalidated {deleted_count} cache entries matching pattern: {pattern}")
            return deleted_count
        except Exception as e:
            logger.warning(f"Cache pattern invalidation error for pattern {pattern}: {e}")
            return 0
    
    def get_cache_key(self, operation: str, *args, **kwargs) -> str:
        """Generate standardized cache key."""
        return self._generate_key(operation, *args, **kwargs)


# Cache configuration for different data types
CACHE_CONFIGS = {
    'members': {'ttl': 3600 * 6, 'key_prefix': 'members'},  # 6 hours
    'committees': {'ttl': 3600 * 12, 'key_prefix': 'committees'},  # 12 hours
    'hearings': {'ttl': 3600 * 2, 'key_prefix': 'hearings'},  # 2 hours
    'search': {'ttl': 3600 * 1, 'key_prefix': 'search'},  # 1 hour
    'relationships': {'ttl': 3600 * 4, 'key_prefix': 'relationships'},  # 4 hours
    'congressional_sessions': {'ttl': 3600 * 24, 'key_prefix': 'sessions'},  # 24 hours
}

# Global cache manager instance
cache_manager = CacheManager()


def cache_key_for(operation: str, *args, **kwargs) -> str:
    """Helper function to generate cache keys."""
    return cache_manager.get_cache_key(operation, *args, **kwargs)


async def cached_operation(
    operation: str,
    cache_ttl: Optional[int] = None,
    force_refresh: bool = False
):
    """Decorator for caching operation results."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if force_refresh:
                # Skip cache, execute function directly
                result = await func(*args, **kwargs)
                return result
            
            # Generate cache key
            cache_key = cache_key_for(operation, *args, **kwargs)
            
            # Try to get from cache
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for operation: {operation}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            
            # Cache the result
            ttl = cache_ttl or CACHE_CONFIGS.get(operation, {}).get('ttl', 3600)
            await cache_manager.set(cache_key, result, ttl)
            
            logger.debug(f"Cache miss for operation: {operation}, cached result")
            return result
        
        return wrapper
    return decorator