"""
Hearing response schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class HearingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    congress_gov_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    committee_id: Optional[int] = None
    scheduled_date: Optional[datetime] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    room: Optional[str] = None
    hearing_type: Optional[str] = None
    status: str
    transcript_url: Optional[str] = None
    video_url: Optional[str] = None
    webcast_url: Optional[str] = None
    congress_session: Optional[int] = None
    congress_number: Optional[int] = None
    scraped_video_urls: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_scraped_at: Optional[datetime] = None