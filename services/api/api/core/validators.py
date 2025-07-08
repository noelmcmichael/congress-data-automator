"""Input validation utilities for the API service."""

from typing import Optional, List
from functools import wraps

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator

from .exceptions import ValidationError
from ..models.congress import Chamber, Party, MemberType, CommitteeType


class PaginationValidator(BaseModel):
    """Pagination parameter validator."""
    
    page: int = Field(ge=1, description="Page number (1-based)")
    size: int = Field(ge=1, le=100, description="Page size (max 100)")
    
    @validator('page')
    def validate_page(cls, v):
        """Validate page number."""
        if v < 1:
            raise ValueError("Page number must be 1 or greater")
        return v
    
    @validator('size')
    def validate_size(cls, v):
        """Validate page size."""
        if v < 1:
            raise ValueError("Page size must be 1 or greater")
        if v > 100:
            raise ValueError("Page size cannot exceed 100")
        return v


class MemberFilterValidator(BaseModel):
    """Member filter parameter validator."""
    
    chamber: Optional[Chamber] = None
    party: Optional[Party] = None
    state: Optional[str] = None
    is_current: Optional[bool] = None
    search: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field("asc", regex="^(asc|desc)$")
    
    @validator('state')
    def validate_state(cls, v):
        """Validate state abbreviation."""
        if v is None:
            return v
        
        # List of valid US state abbreviations
        valid_states = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
            'AS', 'DC', 'GU', 'MP', 'PR', 'VI'  # Territories
        }
        
        if v.upper() not in valid_states:
            raise ValueError(f"Invalid state abbreviation: {v}")
        
        return v.upper()
    
    @validator('search')
    def validate_search(cls, v):
        """Validate search term."""
        if v is None:
            return v
        
        # Basic sanitization
        v = v.strip()
        if len(v) > 100:
            raise ValueError("Search term cannot exceed 100 characters")
        
        # Check for potentially malicious characters
        dangerous_chars = ['<', '>', ';', '&', '|', '`', '$']
        if any(char in v for char in dangerous_chars):
            raise ValueError("Search term contains invalid characters")
        
        return v
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        """Validate sort field."""
        if v is None:
            return v
        
        valid_fields = ['name', 'first_name', 'last_name', 'party', 'state', 'chamber', 'term_start', 'term_end']
        if v not in valid_fields:
            raise ValueError(f"Invalid sort field: {v}. Valid fields: {', '.join(valid_fields)}")
        
        return v


class CommitteeFilterValidator(BaseModel):
    """Committee filter parameter validator."""
    
    chamber: Optional[Chamber] = None
    committee_type: Optional[CommitteeType] = None
    is_current: Optional[bool] = None
    search: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field("asc", regex="^(asc|desc)$")
    
    @validator('search')
    def validate_search(cls, v):
        """Validate search term."""
        if v is None:
            return v
        
        # Basic sanitization
        v = v.strip()
        if len(v) > 100:
            raise ValueError("Search term cannot exceed 100 characters")
        
        # Check for potentially malicious characters
        dangerous_chars = ['<', '>', ';', '&', '|', '`', '$']
        if any(char in v for char in dangerous_chars):
            raise ValueError("Search term contains invalid characters")
        
        return v
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        """Validate sort field."""
        if v is None:
            return v
        
        valid_fields = ['name', 'chamber', 'committee_type', 'established_date']
        if v not in valid_fields:
            raise ValueError(f"Invalid sort field: {v}. Valid fields: {', '.join(valid_fields)}")
        
        return v


class HearingFilterValidator(BaseModel):
    """Hearing filter parameter validator."""
    
    committee_id: Optional[int] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    search: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field("asc", regex="^(asc|desc)$")
    
    @validator('committee_id')
    def validate_committee_id(cls, v):
        """Validate committee ID."""
        if v is None:
            return v
        
        if v < 1:
            raise ValueError("Committee ID must be positive")
        
        return v
    
    @validator('status')
    def validate_status(cls, v):
        """Validate hearing status."""
        if v is None:
            return v
        
        valid_statuses = ['scheduled', 'ongoing', 'completed', 'cancelled']
        if v.lower() not in valid_statuses:
            raise ValueError(f"Invalid status: {v}. Valid statuses: {', '.join(valid_statuses)}")
        
        return v.lower()
    
    @validator('start_date', 'end_date')
    def validate_date(cls, v):
        """Validate date format."""
        if v is None:
            return v
        
        try:
            from datetime import datetime
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    @validator('search')
    def validate_search(cls, v):
        """Validate search term."""
        if v is None:
            return v
        
        # Basic sanitization
        v = v.strip()
        if len(v) > 100:
            raise ValueError("Search term cannot exceed 100 characters")
        
        # Check for potentially malicious characters
        dangerous_chars = ['<', '>', ';', '&', '|', '`', '$']
        if any(char in v for char in dangerous_chars):
            raise ValueError("Search term contains invalid characters")
        
        return v
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        """Validate sort field."""
        if v is None:
            return v
        
        valid_fields = ['title', 'date', 'time', 'status', 'committee_id']
        if v not in valid_fields:
            raise ValueError(f"Invalid sort field: {v}. Valid fields: {', '.join(valid_fields)}")
        
        return v


def validate_id_parameter(resource_id: int, resource_name: str = "Resource") -> int:
    """Validate resource ID parameter."""
    if resource_id < 1:
        raise ValidationError(
            message=f"Invalid {resource_name.lower()} ID",
            detail=f"{resource_name} ID must be a positive integer"
        )
    return resource_id


def validate_pagination_params(page: int, size: int) -> PaginationValidator:
    """Validate pagination parameters."""
    try:
        return PaginationValidator(page=page, size=size)
    except ValueError as e:
        raise ValidationError(
            message="Invalid pagination parameters",
            detail=str(e)
        )


def validate_member_filters(**filters) -> MemberFilterValidator:
    """Validate member filter parameters."""
    try:
        return MemberFilterValidator(**filters)
    except ValueError as e:
        raise ValidationError(
            message="Invalid member filter parameters",
            detail=str(e)
        )


def validate_committee_filters(**filters) -> CommitteeFilterValidator:
    """Validate committee filter parameters."""
    try:
        return CommitteeFilterValidator(**filters)
    except ValueError as e:
        raise ValidationError(
            message="Invalid committee filter parameters",
            detail=str(e)
        )


def validate_hearing_filters(**filters) -> HearingFilterValidator:
    """Validate hearing filter parameters."""
    try:
        return HearingFilterValidator(**filters)
    except ValueError as e:
        raise ValidationError(
            message="Invalid hearing filter parameters",
            detail=str(e)
        )


def validate_endpoint_params(func):
    """Decorator to validate endpoint parameters."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError:
            raise  # Re-raise validation errors
        except ValueError as e:
            raise ValidationError(
                message="Invalid parameter",
                detail=str(e)
            )
        except Exception as e:
            # Log unexpected errors but don't expose them
            from ..core.logging import logger
            logger.error(f"Unexpected error in endpoint validation: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    return wrapper