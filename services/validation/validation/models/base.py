"""Base model for validation service data models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel, Field


class BaseModel(PydanticBaseModel):
    """Base model with common fields for all data models."""
    
    created_at: Optional[datetime] = Field(
        default=None,
        description="Record creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Record last update timestamp"
    )
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
        validate_assignment = True
        use_enum_values = True
        str_strip_whitespace = True