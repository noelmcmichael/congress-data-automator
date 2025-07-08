"""Base models for the API service."""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationInfo


class BaseResponse(BaseModel):
    """Base response model."""
    
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )
    
    success: bool = Field(default=True, description="Request success status")
    message: Optional[str] = Field(default=None, description="Response message")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Response timestamp")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Page size")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        """Get limit for database queries."""
        return self.size


class PaginationResponse(BaseModel):
    """Pagination response metadata."""
    
    page: int = Field(description="Current page number")
    size: int = Field(description="Page size")
    total: int = Field(description="Total number of items")
    pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")
    
    @field_validator("pages", mode="before")
    @classmethod
    def calculate_pages(cls, v: Optional[int], info: ValidationInfo) -> int:
        """Calculate total pages."""
        if v is not None:
            return v
        if info.data:
            total = info.data.get("total", 0)
            size = info.data.get("size", 1)
            return (total + size - 1) // size
        return 1
    
    @field_validator("has_next", mode="before")
    @classmethod
    def calculate_has_next(cls, v: Optional[bool], info: ValidationInfo) -> bool:
        """Calculate has next page."""
        if v is not None:
            return v
        if info.data:
            page = info.data.get("page", 1)
            pages = info.data.get("pages", 1)
            return page < pages
        return False
    
    @field_validator("has_prev", mode="before")
    @classmethod
    def calculate_has_prev(cls, v: Optional[bool], info: ValidationInfo) -> bool:
        """Calculate has previous page."""
        if v is not None:
            return v
        if info.data:
            page = info.data.get("page", 1)
            return page > 1
        return False


class PaginatedResponse(BaseResponse):
    """Paginated response model."""
    
    data: List[BaseModel] = Field(description="Response data")
    pagination: PaginationResponse = Field(description="Pagination metadata")


class FilterParams(BaseModel):
    """Base filter parameters."""
    
    search: Optional[str] = Field(default=None, description="Search query")
    sort_by: Optional[str] = Field(default=None, description="Sort field")
    sort_order: Optional[str] = Field(default="asc", description="Sort order")
    
    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, v: Optional[str]) -> Optional[str]:
        """Validate sort order."""
        if v and v.lower() not in ["asc", "desc"]:
            raise ValueError("Sort order must be 'asc' or 'desc'")
        return v.lower() if v else v


class HealthCheckResponse(BaseResponse):
    """Health check response."""
    
    service: str = Field(description="Service name")
    version: str = Field(description="Service version")
    status: str = Field(description="Service status")
    checks: Dict[str, Dict[str, Union[str, bool, int]]] = Field(
        description="Health check results"
    )
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "success": True,
                "message": "Service is healthy",
                "timestamp": "2025-01-08T12:00:00Z",
                "service": "congressional_data_api",
                "version": "1.0.0",
                "status": "healthy",
                "checks": {
                    "database": {
                        "status": "healthy",
                        "latency_ms": 5,
                        "connected": True
                    },
                    "redis": {
                        "status": "healthy",
                        "latency_ms": 2,
                        "connected": True
                    }
                }
            }
        }


class ErrorResponse(BaseResponse):
    """Error response model."""
    
    success: bool = Field(default=False, description="Request success status")
    error: str = Field(description="Error type")
    detail: Optional[str] = Field(default=None, description="Error details")
    code: Optional[int] = Field(default=None, description="Error code")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Resource not found",
                "timestamp": "2025-01-08T12:00:00Z",
                "error": "NotFound",
                "detail": "Member with ID 999 not found",
                "code": 404
            }
        }