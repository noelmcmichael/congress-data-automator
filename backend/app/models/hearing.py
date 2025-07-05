"""
Database models for congressional hearings.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Hearing(Base):
    """
    Congressional hearing.
    """
    __tablename__ = "hearings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Congress.gov identifiers
    congress_gov_id = Column(String(50), unique=True, index=True)
    
    # Basic information
    title = Column(String(500), nullable=False)
    description = Column(Text)
    
    # Committee information
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=True)
    
    # Scheduling
    scheduled_date = Column(DateTime(timezone=True))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    
    # Location
    location = Column(String(255))
    room = Column(String(100))
    
    # Status
    hearing_type = Column(String(50))  # Hearing, Markup, Business Meeting, etc.
    status = Column(String(50))  # Scheduled, Completed, Cancelled, etc.
    
    # Content
    transcript_url = Column(String(500))
    video_url = Column(String(500))
    webcast_url = Column(String(500))
    
    # Additional metadata
    congress_session = Column(Integer)
    congress_number = Column(Integer)
    
    # Scraped data
    scraped_video_urls = Column(JSON)  # Array of video URLs found through scraping
    scraped_documents = Column(JSON)  # Array of document URLs
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True))
    
    # Relationships
    committee = relationship("Committee", back_populates="hearings")
    witnesses = relationship("Witness", back_populates="hearing")
    documents = relationship("HearingDocument", back_populates="hearing")
    
    def __repr__(self):
        return f"<Hearing {self.title[:50]}... ({self.scheduled_date})>"


class Witness(Base):
    """
    Witness at a congressional hearing.
    """
    __tablename__ = "witnesses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    hearing_id = Column(Integer, ForeignKey("hearings.id"), nullable=False)
    
    # Personal information
    name = Column(String(255), nullable=False)
    title = Column(String(255))
    organization = Column(String(255))
    
    # Contact information
    email = Column(String(255))
    phone = Column(String(20))
    
    # Testimony
    testimony_url = Column(String(500))
    testimony_text = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    hearing = relationship("Hearing", back_populates="witnesses")
    
    def __repr__(self):
        return f"<Witness {self.name} - {self.hearing.title[:30]}...>"


class HearingDocument(Base):
    """
    Document associated with a hearing.
    """
    __tablename__ = "hearing_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    hearing_id = Column(Integer, ForeignKey("hearings.id"), nullable=False)
    
    # Document information
    title = Column(String(500), nullable=False)
    document_type = Column(String(50))  # Testimony, Report, Statement, etc.
    url = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(10))  # pdf, doc, txt, etc.
    
    # Content
    content = Column(Text)  # Extracted text content
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at = Column(DateTime(timezone=True))
    
    # Relationships
    hearing = relationship("Hearing", back_populates="documents")
    
    def __repr__(self):
        return f"<HearingDocument {self.title[:30]}... ({self.document_type})>"