"""
Data processor for coordinating collection, transformation, and staging.

This module provides enterprise-grade data processing capabilities:
- Orchestrates multiple data collectors
- Handles data transformation and normalization
- Manages staging table operations
- Provides comprehensive error handling and logging
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from pydantic import BaseModel
import structlog

from ..core.logging import LoggerMixin
from ..core.database import DatabaseManager
from ..collectors.congress_api import CongressApiCollector
from ..collectors.web_scraping import WebScrapingCollector
from ..models.staging import StagingMember, StagingCommittee, StagingHearing


class ProcessingResult(BaseModel):
    """Result of a data processing operation."""
    success: bool
    operation: str
    records_processed: int
    records_inserted: int
    errors: List[str] = []
    duration_ms: float
    metadata: Dict[str, Any] = {}


class DataProcessor(LoggerMixin):
    """
    Enterprise-grade data processor for congressional data.
    
    Coordinates data collection from multiple sources, transforms the data,
    and stages it for validation. Provides comprehensive error handling,
    logging, and metrics.
    """
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        
        self.logger.info(
            "Data processor initialized",
            components=["congress_api", "web_scraping", "database_manager"]
        )

    async def process_members(
        self, 
        session: Session,
        current_only: bool = True,
        truncate_staging: bool = True
    ) -> ProcessingResult:
        """
        Process congressional members data.
        
        Args:
            session: Database session
            current_only: Only collect current members
            truncate_staging: Whether to truncate staging table first
            
        Returns:
            ProcessingResult: Results of the processing operation
        """
        start_time = time.time()
        operation = "process_members"
        
        self.log_operation_start(
            operation,
            current_only=current_only,
            truncate_staging=truncate_staging
        )
        
        errors = []
        records_processed = 0
        records_inserted = 0
        
        try:
            # Truncate staging table if requested
            if truncate_staging:
                self.db_manager.truncate_staging_table(session, "members")
            
            # Collect data from Congress.gov API
            async with CongressApiCollector() as api_collector:
                members_data = await api_collector.collect_all_members(current_only)
                records_processed = len(members_data)
                
                self.logger.info(
                    "Members data collected from API",
                    total_members=records_processed,
                    current_only=current_only
                )
                
                # Transform and validate data
                staging_data = []
                for member in members_data:
                    try:
                        transformed = self._transform_member_data(member)
                        staging_data.append(transformed)
                    except Exception as e:
                        errors.append(f"Transform error for member {member.get('bioguideId', 'unknown')}: {str(e)}")
                        self.logger.warning(
                            "Member transformation failed",
                            bioguide_id=member.get('bioguideId'),
                            error=str(e)
                        )
                
                # Bulk insert into staging
                if staging_data:
                    records_inserted = self.db_manager.bulk_insert(
                        session, StagingMember, staging_data
                    )
            
            duration_ms = (time.time() - start_time) * 1000
            
            self.log_operation_success(
                operation,
                duration_ms=duration_ms,
                records_processed=records_processed,
                records_inserted=records_inserted,
                error_count=len(errors)
            )
            
            return ProcessingResult(
                success=True,
                operation=operation,
                records_processed=records_processed,
                records_inserted=records_inserted,
                errors=errors,
                duration_ms=duration_ms,
                metadata={
                    "current_only": current_only,
                    "source": "congress_api"
                }
            )
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.log_operation_error(operation, e, duration_ms=duration_ms)
            
            return ProcessingResult(
                success=False,
                operation=operation,
                records_processed=records_processed,
                records_inserted=records_inserted,
                errors=[str(e)],
                duration_ms=duration_ms
            )

    async def process_committees(
        self, 
        session: Session,
        truncate_staging: bool = True
    ) -> ProcessingResult:
        """
        Process congressional committees data.
        
        Args:
            session: Database session
            truncate_staging: Whether to truncate staging table first
            
        Returns:
            ProcessingResult: Results of the processing operation
        """
        start_time = time.time()
        operation = "process_committees"
        
        self.log_operation_start(operation, truncate_staging=truncate_staging)
        
        errors = []
        records_processed = 0
        records_inserted = 0
        
        try:
            # Truncate staging table if requested
            if truncate_staging:
                self.db_manager.truncate_staging_table(session, "committees")
            
            # Collect data from Congress.gov API
            async with CongressApiCollector() as api_collector:
                committees_data = await api_collector.collect_all_committees()
                records_processed = len(committees_data)
                
                self.logger.info(
                    "Committees data collected from API",
                    total_committees=records_processed
                )
                
                # Transform and validate data
                staging_data = []
                for committee in committees_data:
                    try:
                        transformed = self._transform_committee_data(committee)
                        staging_data.append(transformed)
                    except Exception as e:
                        errors.append(f"Transform error for committee {committee.get('systemCode', 'unknown')}: {str(e)}")
                        self.logger.warning(
                            "Committee transformation failed",
                            system_code=committee.get('systemCode'),
                            error=str(e)
                        )
                
                # Bulk insert into staging
                if staging_data:
                    records_inserted = self.db_manager.bulk_insert(
                        session, StagingCommittee, staging_data
                    )
            
            duration_ms = (time.time() - start_time) * 1000
            
            self.log_operation_success(
                operation,
                duration_ms=duration_ms,
                records_processed=records_processed,
                records_inserted=records_inserted,
                error_count=len(errors)
            )
            
            return ProcessingResult(
                success=True,
                operation=operation,
                records_processed=records_processed,
                records_inserted=records_inserted,
                errors=errors,
                duration_ms=duration_ms,
                metadata={"source": "congress_api"}
            )
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.log_operation_error(operation, e, duration_ms=duration_ms)
            
            return ProcessingResult(
                success=False,
                operation=operation,
                records_processed=records_processed,
                records_inserted=records_inserted,
                errors=[str(e)],
                duration_ms=duration_ms
            )

    async def process_hearings(
        self, 
        session: Session,
        days_back: int = 30,
        include_web_scraping: bool = True,
        truncate_staging: bool = True
    ) -> ProcessingResult:
        """
        Process congressional hearings data from multiple sources.
        
        Args:
            session: Database session
            days_back: Number of days to look back for hearings
            include_web_scraping: Whether to include web scraping
            truncate_staging: Whether to truncate staging table first
            
        Returns:
            ProcessingResult: Results of the processing operation
        """
        start_time = time.time()
        operation = "process_hearings"
        
        self.log_operation_start(
            operation,
            days_back=days_back,
            include_web_scraping=include_web_scraping,
            truncate_staging=truncate_staging
        )
        
        errors = []
        records_processed = 0
        records_inserted = 0
        sources_used = []
        
        try:
            # Truncate staging table if requested
            if truncate_staging:
                self.db_manager.truncate_staging_table(session, "hearings")
            
            all_hearings = []
            
            # Collect from Congress.gov API
            async with CongressApiCollector() as api_collector:
                api_hearings = await api_collector.collect_recent_hearings(days_back)
                all_hearings.extend(api_hearings)
                sources_used.append("congress_api")
                
                self.logger.info(
                    "Hearings collected from API",
                    count=len(api_hearings),
                    days_back=days_back
                )
            
            # Collect from web scraping if enabled
            if include_web_scraping:
                async with WebScrapingCollector() as web_collector:
                    scraped_hearings = await self._scrape_committee_hearings(web_collector)
                    all_hearings.extend(scraped_hearings)
                    sources_used.append("web_scraping")
                    
                    self.logger.info(
                        "Hearings collected from web scraping",
                        count=len(scraped_hearings)
                    )
            
            # Deduplicate hearings by title and date
            deduplicated_hearings = self._deduplicate_hearings(all_hearings)
            records_processed = len(deduplicated_hearings)
            
            # Transform and validate data
            staging_data = []
            for hearing in deduplicated_hearings:
                try:
                    transformed = self._transform_hearing_data(hearing)
                    staging_data.append(transformed)
                except Exception as e:
                    errors.append(f"Transform error for hearing: {str(e)}")
                    self.logger.warning(
                        "Hearing transformation failed",
                        hearing_title=hearing.get('title', 'unknown')[:50],
                        error=str(e)
                    )
            
            # Bulk insert into staging
            if staging_data:
                records_inserted = self.db_manager.bulk_insert(
                    session, StagingHearing, staging_data
                )
            
            duration_ms = (time.time() - start_time) * 1000
            
            self.log_operation_success(
                operation,
                duration_ms=duration_ms,
                records_processed=records_processed,
                records_inserted=records_inserted,
                error_count=len(errors),
                sources=sources_used
            )
            
            return ProcessingResult(
                success=True,
                operation=operation,
                records_processed=records_processed,
                records_inserted=records_inserted,
                errors=errors,
                duration_ms=duration_ms,
                metadata={
                    "days_back": days_back,
                    "sources": sources_used,
                    "web_scraping_enabled": include_web_scraping
                }
            )
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.log_operation_error(operation, e, duration_ms=duration_ms)
            
            return ProcessingResult(
                success=False,
                operation=operation,
                records_processed=records_processed,
                records_inserted=records_inserted,
                errors=[str(e)],
                duration_ms=duration_ms
            )

    def _transform_member_data(self, member: Dict[str, Any]) -> Dict[str, Any]:
        """Transform member data for staging table."""
        # Extract terms information
        terms = member.get('terms', {})
        current_term = terms.get('item', [{}])[-1] if terms.get('item') else {}
        
        return {
            "bioguide_id": member.get('bioguideId'),
            "congress_gov_id": member.get('url', '').split('/')[-1] if member.get('url') else None,
            "first_name": member.get('firstName', ''),
            "last_name": member.get('lastName', ''),
            "middle_name": member.get('middleName'),
            "suffix": member.get('suffix'),
            "nickname": member.get('nickName'),
            "party": current_term.get('party', member.get('partyName', '')),
            "chamber": current_term.get('chamber', ''),
            "state": member.get('state', current_term.get('stateCode', '')),
            "district": current_term.get('district'),
            "term_start": self._parse_date(current_term.get('startYear')),
            "term_end": self._parse_date(current_term.get('endYear')),
            "is_current": True,  # Assuming current members
            "birth_date": self._parse_date(member.get('birthYear')),
            "raw_data": member,  # Store original data for debugging
            "collected_at": datetime.utcnow()
        }

    def _transform_committee_data(self, committee: Dict[str, Any]) -> Dict[str, Any]:
        """Transform committee data for staging table."""
        return {
            "system_code": committee.get('systemCode'),
            "name": committee.get('name', ''),
            "chamber": committee.get('chamber', ''),
            "committee_type": committee.get('type', 'Standing'),
            "is_subcommittee": committee.get('type', '').lower() == 'subcommittee',
            "parent_committee_code": committee.get('parentCommitteeCode'),
            "jurisdiction": committee.get('jurisdiction'),
            "congress_gov_url": committee.get('url'),
            "raw_data": committee,
            "collected_at": datetime.utcnow()
        }

    def _transform_hearing_data(self, hearing: Dict[str, Any]) -> Dict[str, Any]:
        """Transform hearing data for staging table."""
        return {
            "title": hearing.get('title', ''),
            "description": hearing.get('description'),
            "date_time": self._parse_datetime(hearing.get('date') or hearing.get('date_time')),
            "location": hearing.get('location'),
            "room": hearing.get('room'),
            "status": hearing.get('status', 'scheduled'),
            "committee_code": hearing.get('committee', {}).get('systemCode') if isinstance(hearing.get('committee'), dict) else hearing.get('committee'),
            "congress_gov_url": hearing.get('url'),
            "source_url": hearing.get('source_url'),
            "raw_data": hearing,
            "collected_at": datetime.utcnow()
        }

    def _parse_date(self, date_value: Any) -> Optional[datetime]:
        """Parse various date formats to datetime."""
        if not date_value:
            return None
        
        try:
            if isinstance(date_value, int):
                return datetime(date_value, 1, 1)
            elif isinstance(date_value, str):
                # Try common date formats
                for fmt in ['%Y-%m-%d', '%Y', '%m/%d/%Y']:
                    try:
                        return datetime.strptime(date_value, fmt)
                    except ValueError:
                        continue
        except Exception:
            pass
        
        return None

    def _parse_datetime(self, datetime_value: Any) -> Optional[datetime]:
        """Parse various datetime formats."""
        if not datetime_value:
            return None
        
        try:
            if isinstance(datetime_value, str):
                # Try common datetime formats
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                    try:
                        return datetime.strptime(datetime_value, fmt)
                    except ValueError:
                        continue
        except Exception:
            pass
        
        return None

    def _deduplicate_hearings(self, hearings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate hearings by title and date."""
        seen = set()
        unique_hearings = []
        
        for hearing in hearings:
            # Create a key based on title and date for deduplication
            title = hearing.get('title', '').strip().lower()
            date = hearing.get('date') or hearing.get('date_time', '')
            key = f"{title}:{date}"
            
            if key not in seen and title:
                seen.add(key)
                unique_hearings.append(hearing)
        
        self.logger.debug(
            "Hearings deduplicated",
            original_count=len(hearings),
            unique_count=len(unique_hearings),
            duplicates_removed=len(hearings) - len(unique_hearings)
        )
        
        return unique_hearings

    async def _scrape_committee_hearings(
        self, 
        web_collector: WebScrapingCollector
    ) -> List[Dict[str, Any]]:
        """Scrape hearings from committee websites."""
        # Sample committee URLs - in production, these would come from database
        committee_urls = [
            "https://www.house.gov/committees",
            "https://www.senate.gov/committees",
        ]
        
        all_hearings = []
        
        for url in committee_urls:
            try:
                hearings = await web_collector.scrape_committee_hearings(url)
                all_hearings.extend(hearings)
            except Exception as e:
                self.logger.warning(
                    "Failed to scrape committee hearings",
                    url=url,
                    error=str(e)
                )
        
        return all_hearings