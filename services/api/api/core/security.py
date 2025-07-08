"""Security middleware and utilities."""

import time
from typing import Dict, Optional
from collections import defaultdict, deque

from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .config import settings
from .logging import logger


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers."""

    def __init__(self, app):
        super().__init__(app)
        self.enabled = settings.security_headers_enabled

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Add security headers to response."""
        response = await call_next(request)
        
        if not self.enabled:
            return response

        # Security headers
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

        # Add HSTS for HTTPS
        if request.url.scheme == "https":
            security_headers["Strict-Transport-Security"] = f"max-age={settings.hsts_max_age}; includeSubDomains"

        # Apply headers
        for header, value in security_headers.items():
            response.headers[header] = value

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""

    def __init__(self, app):
        super().__init__(app)
        self.requests_per_minute = settings.rate_limit_requests
        self.burst_allowance = settings.rate_limit_burst
        self.window_size = settings.rate_limit_period
        
        # In-memory storage for rate limiting
        # In production, this should use Redis
        self.clients: Dict[str, deque] = defaultdict(deque)

    def get_client_ip(self, request: Request) -> str:
        """Get client IP address."""
        # Check for X-Forwarded-For header (proxy/load balancer)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check for X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct connection
        return request.client.host if request.client else "unknown"

    def is_rate_limited(self, client_ip: str) -> bool:
        """Check if client is rate limited."""
        current_time = time.time()
        client_requests = self.clients[client_ip]
        
        # Remove old requests outside the window
        while client_requests and client_requests[0] <= current_time - self.window_size:
            client_requests.popleft()
        
        # Check if under rate limit
        if len(client_requests) < self.requests_per_minute:
            client_requests.append(current_time)
            return False
        
        # Check burst allowance
        if len(client_requests) < self.burst_allowance:
            client_requests.append(current_time)
            logger.warning(f"Rate limit exceeded for {client_ip}, using burst allowance")
            return False
        
        return True

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Rate limit requests."""
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)

        client_ip = self.get_client_ip(request)
        
        if self.is_rate_limited(client_ip):
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.requests_per_minute} requests per {self.window_size} seconds allowed",
                    "retry_after": self.window_size
                }
            )

        response = await call_next(request)
        
        # Add rate limiting headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.requests_per_minute - len(self.clients[client_ip]))
        )
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + self.window_size)
        
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log requests."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Log requests and responses."""
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown"),
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
                "response_size": response.headers.get("content-length", "unknown"),
            }
        )
        
        # Add response time header
        response.headers["X-Response-Time"] = f"{duration:.4f}s"
        
        return response


def get_client_info(request: Request) -> Dict[str, Optional[str]]:
    """Extract client information from request."""
    return {
        "ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "referer": request.headers.get("referer"),
        "forwarded_for": request.headers.get("x-forwarded-for"),
        "real_ip": request.headers.get("x-real-ip"),
    }


def validate_api_key(api_key: Optional[str]) -> bool:
    """Validate API key (placeholder for future implementation)."""
    # For now, no API key validation
    # In production, implement proper API key validation
    return True


def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Sanitize user input."""
    if not value:
        return ""
    
    # Truncate if too long
    value = value[:max_length]
    
    # Remove dangerous characters
    dangerous_chars = ["<", ">", "&", "\"", "'", ";", "(", ")", "{", "}", "[", "]"]
    for char in dangerous_chars:
        value = value.replace(char, "")
    
    return value.strip()