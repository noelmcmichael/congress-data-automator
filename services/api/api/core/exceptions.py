"""Custom exceptions for the API service."""

from typing import Any, Dict, Optional


class APIException(Exception):
    """Base API exception."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        self.headers = headers or {}
        super().__init__(self.message)


class ValidationError(APIException):
    """Validation error exception."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=422,
            detail=detail,
        )


class NotFoundError(APIException):
    """Not found error exception."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=404,
            detail=detail,
        )


class BadRequestError(APIException):
    """Bad request error exception."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=400,
            detail=detail,
        )


class ConflictError(APIException):
    """Conflict error exception."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=409,
            detail=detail,
        )


class InternalServerError(APIException):
    """Internal server error exception."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=500,
            detail=detail,
        )


class ServiceUnavailableError(APIException):
    """Service unavailable error exception."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=503,
            detail=detail,
        )


class RateLimitExceededError(APIException):
    """Rate limit exceeded error exception."""
    
    def __init__(self, message: str, detail: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=429,
            detail=detail,
        )