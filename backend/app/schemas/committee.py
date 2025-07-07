"""
Committee response schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class CommitteeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    chamber: str
    committee_code: Optional[str] = None
    congress_gov_id: Optional[str] = None
    is_active: bool
    is_subcommittee: bool
    parent_committee_id: Optional[int] = None
    website: Optional[str] = None
    
    # Official URLs
    hearings_url: Optional[str] = None
    members_url: Optional[str] = None
    official_website_url: Optional[str] = None
    last_url_update: Optional[datetime] = None
    
    created_at: datetime
    updated_at: Optional[datetime] = None