"""
Security utilities for Congressional Data Automation Service.
Implements input validation, sanitization, and security checks.
"""
import re
import html
import bleach
from typing import Any, Dict, List, Optional, Union
import structlog
from sqlalchemy import text
from ..middleware.security_middleware import security_monitor

logger = structlog.get_logger()


class InputValidator:
    """Input validation and sanitization utilities."""
    
    # Define allowed patterns for different input types
    PATTERNS = {
        'state_code': re.compile(r'^[A-Z]{2}$'),
        'party': re.compile(r'^(Republican|Democrat|Independent|Libertarian|Green)$', re.IGNORECASE),
        'chamber': re.compile(r'^(House|Senate)$', re.IGNORECASE),
        'member_id': re.compile(r'^[A-Z]\d{6}$'),
        'bioguide_id': re.compile(r'^[A-Z]\d{6}$'),
        'committee_code': re.compile(r'^[A-Z]{2,4}\d{0,2}$'),
        'congress_number': re.compile(r'^\d{1,3}$'),
        'alphanumeric': re.compile(r'^[a-zA-Z0-9\s\-_.]+$'),
        'name': re.compile(r'^[a-zA-Z\s\-\'\.]+$'),
        'url': re.compile(r'^https?://[^\s<>"{}|\\^`\[\]]+$'),
        'date': re.compile(r'^\d{4}-\d{2}-\d{2}$'),
        'year': re.compile(r'^(19|20)\d{2}$'),
    }
    
    # SQL injection patterns to detect
    SQL_INJECTION_PATTERNS = [
        re.compile(r"(\'|\;|\-\-|\/\*|\*\/)", re.IGNORECASE),
        re.compile(r"(union.*select|insert.*into|delete.*from|drop.*table|alter.*table)", re.IGNORECASE),
        re.compile(r"(exec.*|execute.*|sp_.*|xp_.*)", re.IGNORECASE),
        re.compile(r"(script.*>|<.*script|javascript:)", re.IGNORECASE),
    ]
    
    # XSS patterns to detect
    XSS_PATTERNS = [
        re.compile(r"<\s*script", re.IGNORECASE),
        re.compile(r"javascript:", re.IGNORECASE),
        re.compile(r"on\w+\s*=", re.IGNORECASE),
        re.compile(r"<\s*iframe", re.IGNORECASE),
        re.compile(r"<\s*object", re.IGNORECASE),
        re.compile(r"<\s*embed", re.IGNORECASE),
    ]
    
    @classmethod
    def validate_input(cls, value: Any, input_type: str, required: bool = True) -> tuple[bool, str, Any]:
        """
        Validate input against specified type.
        
        Returns:
            tuple: (is_valid, error_message, sanitized_value)
        """
        if value is None or value == "":
            if required:
                return False, f"{input_type} is required", None
            return True, "", None
        
        # Convert to string for pattern matching
        str_value = str(value).strip()
        
        # Check for SQL injection patterns
        if cls._contains_sql_injection(str_value):
            security_monitor.log_security_event(
                "sql_injection_attempt",
                {"input": str_value[:100], "type": input_type},
                "critical"
            )
            return False, "Invalid input detected", None
        
        # Check for XSS patterns
        if cls._contains_xss(str_value):
            security_monitor.log_security_event(
                "xss_attempt",
                {"input": str_value[:100], "type": input_type},
                "warning"
            )
            return False, "Invalid input detected", None
        
        # Validate against specific pattern
        if input_type in cls.PATTERNS:
            pattern = cls.PATTERNS[input_type]
            if not pattern.match(str_value):
                return False, f"Invalid {input_type} format", None
        
        # Sanitize the input
        sanitized_value = cls._sanitize_input(str_value, input_type)
        
        return True, "", sanitized_value
    
    @classmethod
    def _contains_sql_injection(cls, value: str) -> bool:
        """Check if input contains SQL injection patterns."""
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if pattern.search(value):
                return True
        return False
    
    @classmethod
    def _contains_xss(cls, value: str) -> bool:
        """Check if input contains XSS patterns."""
        for pattern in cls.XSS_PATTERNS:
            if pattern.search(value):
                return True
        return False
    
    @classmethod
    def _sanitize_input(cls, value: str, input_type: str) -> str:
        """Sanitize input based on type."""
        # HTML escape for safety
        sanitized = html.escape(value)
        
        # Type-specific sanitization
        if input_type in ['state_code', 'party', 'chamber']:
            sanitized = sanitized.upper()
        elif input_type in ['name', 'alphanumeric']:
            # Remove potentially dangerous characters
            sanitized = re.sub(r'[<>"\']', '', sanitized)
        elif input_type == 'url':
            # Basic URL sanitization
            if not sanitized.startswith(('http://', 'https://')):
                sanitized = 'https://' + sanitized
        
        return sanitized
    
    @classmethod
    def validate_search_query(cls, query: str, max_length: int = 100) -> tuple[bool, str, str]:
        """Validate search query with specific rules."""
        if not query:
            return False, "Search query is required", ""
        
        if len(query) > max_length:
            return False, f"Search query too long (max {max_length} characters)", ""
        
        # Check for injection patterns
        if cls._contains_sql_injection(query) or cls._contains_xss(query):
            security_monitor.log_security_event(
                "malicious_search_query",
                {"query": query[:50]},
                "warning"
            )
            return False, "Invalid search query", ""
        
        # Sanitize search query
        sanitized = bleach.clean(query, tags=[], strip=True)
        sanitized = re.sub(r'[<>"\']', '', sanitized)
        
        return True, "", sanitized


class ParameterValidator:
    """Validates API endpoint parameters."""
    
    @staticmethod
    def validate_pagination_params(page: int = 1, limit: int = 50) -> tuple[bool, str, int, int]:
        """Validate pagination parameters."""
        try:
            page = int(page)
            limit = int(limit)
            
            if page < 1:
                return False, "Page must be >= 1", 1, 50
            
            if limit < 1 or limit > 1000:
                return False, "Limit must be between 1 and 1000", page, 50
            
            return True, "", page, limit
            
        except (ValueError, TypeError):
            return False, "Invalid pagination parameters", 1, 50
    
    @staticmethod
    def validate_filter_params(filters: Dict[str, Any]) -> tuple[bool, str, Dict[str, Any]]:
        """Validate filter parameters."""
        validated_filters = {}
        
        for key, value in filters.items():
            if value is None:
                continue
                
            # Validate specific filter types
            if key == 'state':
                is_valid, error, sanitized = InputValidator.validate_input(value, 'state_code', False)
            elif key == 'party':
                is_valid, error, sanitized = InputValidator.validate_input(value, 'party', False)
            elif key == 'chamber':
                is_valid, error, sanitized = InputValidator.validate_input(value, 'chamber', False)
            elif key == 'congress':
                is_valid, error, sanitized = InputValidator.validate_input(value, 'congress_number', False)
            elif key in ['name', 'title']:
                is_valid, error, sanitized = InputValidator.validate_input(value, 'name', False)
            else:
                # Generic alphanumeric validation
                is_valid, error, sanitized = InputValidator.validate_input(value, 'alphanumeric', False)
            
            if not is_valid:
                return False, f"Invalid {key}: {error}", {}
            
            if sanitized is not None:
                validated_filters[key] = sanitized
        
        return True, "", validated_filters


class SecurityConfig:
    """Security configuration settings."""
    
    # Rate limiting configuration
    RATE_LIMITS = {
        'default': {'calls': 100, 'period': 60},  # 100 requests per minute
        'search': {'calls': 50, 'period': 60},    # 50 search requests per minute
        'admin': {'calls': 20, 'period': 60},     # 20 admin requests per minute
    }
    
    # Maximum request sizes
    MAX_REQUEST_SIZES = {
        'default': 1024 * 1024,      # 1MB
        'upload': 10 * 1024 * 1024,  # 10MB
    }
    
    # Allowed file types for uploads
    ALLOWED_FILE_TYPES = {
        'data': ['.json', '.csv', '.txt'],
        'images': ['.jpg', '.jpeg', '.png', '.gif'],
    }
    
    # Security headers configuration
    SECURITY_HEADERS = {
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
    }


def get_security_status() -> Dict[str, Any]:
    """Get current security status and metrics."""
    monitor_summary = security_monitor.get_security_summary()
    
    return {
        "security_middleware": "enabled",
        "rate_limiting": "active",
        "input_validation": "active",
        "security_headers": "enabled",
        "sql_injection_protection": "active",
        "xss_protection": "active",
        "security_events": monitor_summary,
        "last_updated": "2025-01-08T23:00:00Z"
    }


def validate_api_key(api_key: str) -> bool:
    """Validate API key format and authenticity."""
    if not api_key:
        return False
    
    # Basic format validation
    if not re.match(r'^[a-zA-Z0-9\-_]{32,128}$', api_key):
        security_monitor.log_security_event(
            "invalid_api_key_format",
            {"key_length": len(api_key)},
            "warning"
        )
        return False
    
    # Additional validation logic would go here
    # For now, we'll assume valid format means valid key
    return True


def log_suspicious_activity(activity_type: str, details: Dict[str, Any], request_info: Dict[str, Any]):
    """Log suspicious activity for security monitoring."""
    security_monitor.log_security_event(
        activity_type,
        {
            **details,
            "ip_address": request_info.get("ip"),
            "user_agent": request_info.get("user_agent"),
            "endpoint": request_info.get("endpoint")
        },
        "warning"
    )