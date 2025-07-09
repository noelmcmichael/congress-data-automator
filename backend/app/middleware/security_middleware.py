"""
Security middleware for Congressional Data Automation Service.
Implements rate limiting, security headers, and request validation.
"""
import time
import hashlib
from typing import Dict, Optional, Tuple
from collections import defaultdict, deque
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

logger = structlog.get_logger()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with sliding window implementation."""
    
    def __init__(
        self,
        app,
        calls: int = 100,
        period: int = 60,
        per_ip: bool = True,
        exempt_paths: Optional[list] = None
    ):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.per_ip = per_ip
        self.exempt_paths = exempt_paths or ["/health", "/docs", "/openapi.json"]
        
        # In-memory storage for rate limiting
        # In production, this should use Redis for multi-instance support
        self.request_counts: Dict[str, deque] = defaultdict(deque)
        self.last_cleanup = time.time()
        self.cleanup_interval = 300  # 5 minutes
    
    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        """Process request with rate limiting."""
        # Skip rate limiting for exempt paths
        if any(request.url.path.startswith(path) for path in self.exempt_paths):
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limit
        if not await self._check_rate_limit(client_id):
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "detail": f"Maximum {self.calls} requests per {self.period} seconds",
                    "retry_after": self.period
                },
                headers={
                    "Retry-After": str(self.period),
                    "X-RateLimit-Limit": str(self.calls),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + self.period)
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        remaining = await self._get_remaining_requests(client_id)
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + self.period)
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting."""
        if self.per_ip:
            # Try to get real IP from headers (for reverse proxy setups)
            forwarded_for = request.headers.get("X-Forwarded-For")
            if forwarded_for:
                # Take the first IP in the chain
                client_ip = forwarded_for.split(",")[0].strip()
            else:
                client_ip = request.client.host if request.client else "unknown"
            return f"ip:{client_ip}"
        else:
            # Global rate limiting
            return "global"
    
    async def _check_rate_limit(self, client_id: str) -> bool:
        """Check if request is within rate limit."""
        now = time.time()
        
        # Cleanup old entries periodically
        if now - self.last_cleanup > self.cleanup_interval:
            await self._cleanup_old_entries()
            self.last_cleanup = now
        
        # Get request times for this client
        request_times = self.request_counts[client_id]
        
        # Remove old requests outside the time window
        cutoff_time = now - self.period
        while request_times and request_times[0] < cutoff_time:
            request_times.popleft()
        
        # Check if under limit
        if len(request_times) >= self.calls:
            return False
        
        # Add current request
        request_times.append(now)
        return True
    
    async def _get_remaining_requests(self, client_id: str) -> int:
        """Get remaining requests for client."""
        request_times = self.request_counts[client_id]
        return max(0, self.calls - len(request_times))
    
    async def _cleanup_old_entries(self):
        """Remove old entries to prevent memory leaks."""
        now = time.time()
        cutoff_time = now - self.period
        
        clients_to_remove = []
        for client_id, request_times in self.request_counts.items():
            # Remove old requests
            while request_times and request_times[0] < cutoff_time:
                request_times.popleft()
            
            # Remove clients with no recent requests
            if not request_times:
                clients_to_remove.append(client_id)
        
        for client_id in clients_to_remove:
            del self.request_counts[client_id]
        
        logger.debug(f"Rate limit cleanup: removed {len(clients_to_remove)} inactive clients")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Security headers middleware."""
    
    def __init__(self, app):
        super().__init__(app)
        self.security_headers = {
            # Prevent clickjacking
            "X-Frame-Options": "DENY",
            
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            
            # XSS protection
            "X-XSS-Protection": "1; mode=block",
            
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'"
            ),
            
            # Permissions policy
            "Permissions-Policy": (
                "camera=(), "
                "microphone=(), "
                "geolocation=(), "
                "payment=(), "
                "usb=()"
            ),
        }
    
    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        """Add security headers to response."""
        response = await call_next(request)
        
        # Add security headers
        for header, value in self.security_headers.items():
            response.headers[header] = value
        
        # Add HSTS for HTTPS requests
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Request validation and sanitization middleware."""
    
    def __init__(self, app, max_request_size: int = 1024 * 1024):  # 1MB default
        super().__init__(app)
        self.max_request_size = max_request_size
        self.suspicious_patterns = [
            # SQL injection patterns
            r"(?i)(union.*select|insert.*into|delete.*from|drop.*table)",
            # XSS patterns
            r"(?i)(<script|javascript:|on\w+\s*=)",
            # Command injection patterns
            r"(?i)(;.*rm\s|;.*cat\s|;.*ls\s|\|\s*rm\s)"
        ]
    
    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        """Validate and sanitize requests."""
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_request_size:
            logger.warning(f"Request too large: {content_length} bytes")
            return JSONResponse(
                status_code=413,
                content={"error": "Request entity too large"}
            )
        
        # Validate query parameters
        if request.url.query:
            if not self._validate_query_params(request.url.query):
                logger.warning(f"Suspicious query parameters detected: {request.url.query}")
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid request parameters"}
                )
        
        # Process request
        response = await call_next(request)
        
        return response
    
    def _validate_query_params(self, query_string: str) -> bool:
        """Validate query parameters for suspicious content."""
        import re
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, query_string):
                return False
        
        return True


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    """IP whitelist middleware for admin endpoints."""
    
    def __init__(self, app, admin_paths: Optional[list] = None, allowed_ips: Optional[list] = None):
        super().__init__(app)
        self.admin_paths = admin_paths or ["/admin", "/api/v1/admin"]
        self.allowed_ips = set(allowed_ips or ["127.0.0.1", "::1"])  # localhost by default
    
    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        """Check IP whitelist for admin endpoints."""
        # Check if this is an admin path
        is_admin_path = any(request.url.path.startswith(path) for path in self.admin_paths)
        
        if is_admin_path:
            client_ip = self._get_client_ip(request)
            if client_ip not in self.allowed_ips:
                logger.warning(f"Unauthorized admin access attempt from IP: {client_ip}")
                return JSONResponse(
                    status_code=403,
                    content={"error": "Access denied"}
                )
        
        return await call_next(request)
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address."""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"


class SecurityMonitor:
    """Security monitoring and logging."""
    
    def __init__(self):
        self.security_events = deque(maxlen=1000)  # Keep last 1000 events
    
    def log_security_event(self, event_type: str, details: dict, severity: str = "info"):
        """Log security event."""
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "details": details,
            "severity": severity
        }
        
        self.security_events.append(event)
        
        if severity == "critical":
            logger.error(f"Security event: {event_type}", extra=details)
        elif severity == "warning":
            logger.warning(f"Security event: {event_type}", extra=details)
        else:
            logger.info(f"Security event: {event_type}", extra=details)
    
    def get_security_summary(self) -> dict:
        """Get security events summary."""
        if not self.security_events:
            return {"total_events": 0, "by_type": {}, "by_severity": {}}
        
        by_type = defaultdict(int)
        by_severity = defaultdict(int)
        
        for event in self.security_events:
            by_type[event["type"]] += 1
            by_severity[event["severity"]] += 1
        
        return {
            "total_events": len(self.security_events),
            "by_type": dict(by_type),
            "by_severity": dict(by_severity),
            "last_24h": len([e for e in self.security_events if time.time() - e["timestamp"] < 86400])
        }


# Global security monitor instance
security_monitor = SecurityMonitor()