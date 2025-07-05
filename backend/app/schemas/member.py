"""
Member response schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    bioguide_id: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    nickname: Optional[str] = None
    party: str
    chamber: str
    state: str
    district: Optional[int] = None
    is_current: bool
    official_photo_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_scraped_at: Optional[datetime] = None