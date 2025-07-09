"""
Data export service for Congressional Data Automation Service.
Provides CSV, JSON, and other export formats with filtering.
"""
import csv
import json
import io
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import structlog
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session

from ..models.member import Member
from ..models.committee import Committee
from ..models.hearing import Hearing
# from ..models.committee_membership import CommitteeMembership
from ..core.security import InputValidator, ParameterValidator

logger = structlog.get_logger()


class DataExporter:
    """Handles data export operations."""
    
    SUPPORTED_FORMATS = ['csv', 'json', 'jsonl']
    
    def __init__(self):
        self.mime_types = {
            'csv': 'text/csv',
            'json': 'application/json',
            'jsonl': 'application/x-jsonlines'
        }
    
    async def export_members(
        self,
        db: Session,
        format: str = 'csv',
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None
    ) -> StreamingResponse:
        """Export members data in specified format."""
        if format not in self.SUPPORTED_FORMATS:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
        
        # Validate filters
        if filters:
            is_valid, error, validated_filters = ParameterValidator.validate_filter_params(filters)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            filters = validated_filters
        
        # Build query
        query = db.query(Member)
        
        # Apply filters
        if filters:
            if 'state' in filters:
                query = query.filter(Member.state == filters['state'])
            if 'party' in filters:
                query = query.filter(Member.party == filters['party'])
            if 'chamber' in filters:
                query = query.filter(Member.chamber == filters['chamber'])
            if 'voting_status' in filters:
                query = query.filter(Member.voting_status == filters['voting_status'])
        
        # Execute query
        members = query.all()
        
        # Convert to export format
        if format == 'csv':
            return self._export_members_csv(members, fields)
        elif format == 'json':
            return self._export_members_json(members, fields)
        elif format == 'jsonl':
            return self._export_members_jsonl(members, fields)
    
    async def export_committees(
        self,
        db: Session,
        format: str = 'csv',
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None
    ) -> StreamingResponse:
        """Export committees data in specified format."""
        if format not in self.SUPPORTED_FORMATS:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
        
        # Build query
        query = db.query(Committee)
        
        # Apply filters
        if filters:
            if 'chamber' in filters:
                query = query.filter(Committee.chamber == filters['chamber'])
            if 'committee_type' in filters:
                query = query.filter(Committee.committee_type == filters['committee_type'])
        
        # Execute query
        committees = query.all()
        
        # Convert to export format
        if format == 'csv':
            return self._export_committees_csv(committees, fields)
        elif format == 'json':
            return self._export_committees_json(committees, fields)
        elif format == 'jsonl':
            return self._export_committees_jsonl(committees, fields)
    
    async def export_hearings(
        self,
        db: Session,
        format: str = 'csv',
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None
    ) -> StreamingResponse:
        """Export hearings data in specified format."""
        if format not in self.SUPPORTED_FORMATS:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
        
        # Build query
        query = db.query(Hearing)
        
        # Apply filters
        if filters:
            if 'committee_id' in filters:
                query = query.filter(Hearing.committee_id == filters['committee_id'])
            if 'date_from' in filters:
                query = query.filter(Hearing.date >= filters['date_from'])
            if 'date_to' in filters:
                query = query.filter(Hearing.date <= filters['date_to'])
        
        # Execute query
        hearings = query.all()
        
        # Convert to export format
        if format == 'csv':
            return self._export_hearings_csv(hearings, fields)
        elif format == 'json':
            return self._export_hearings_json(hearings, fields)
        elif format == 'jsonl':
            return self._export_hearings_jsonl(hearings, fields)
    
    def _export_members_csv(self, members: List[Member], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export members as CSV."""
        # Default fields if not specified
        if not fields:
            fields = [
                'bioguide_id', 'first_name', 'last_name', 'party', 'state', 
                'district', 'chamber', 'voting_status', 'url'
            ]
        
        def generate_csv():
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fields)
            
            # Write header
            writer.writeheader()
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)
            
            # Write data rows
            for member in members:
                row = {}
                for field in fields:
                    value = getattr(member, field, '')
                    # Handle None values
                    row[field] = value if value is not None else ''
                
                writer.writerow(row)
                yield output.getvalue()
                output.seek(0)
                output.truncate(0)
        
        filename = f"members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        
        return StreamingResponse(
            generate_csv(),
            media_type=self.mime_types['csv'],
            headers=headers
        )
    
    def _export_members_json(self, members: List[Member], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export members as JSON."""
        data = []
        for member in members:
            member_dict = {}
            if fields:
                for field in fields:
                    value = getattr(member, field, None)
                    member_dict[field] = value
            else:
                member_dict = {
                    'bioguide_id': member.bioguide_id,
                    'first_name': member.first_name,
                    'last_name': member.last_name,
                    'party': member.party,
                    'state': member.state,
                    'district': member.district,
                    'chamber': member.chamber,
                    'voting_status': member.voting_status,
                    'url': member.url
                }
            data.append(member_dict)
        
        def generate_json():
            yield json.dumps({
                'export_timestamp': datetime.now().isoformat(),
                'total_records': len(data),
                'data': data
            }, indent=2, default=str)
        
        filename = f"members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        
        return StreamingResponse(
            generate_json(),
            media_type=self.mime_types['json'],
            headers=headers
        )
    
    def _export_members_jsonl(self, members: List[Member], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export members as JSON Lines."""
        def generate_jsonl():
            for member in members:
                member_dict = {}
                if fields:
                    for field in fields:
                        value = getattr(member, field, None)
                        member_dict[field] = value
                else:
                    member_dict = {
                        'bioguide_id': member.bioguide_id,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'party': member.party,
                        'state': member.state,
                        'district': member.district,
                        'chamber': member.chamber,
                        'voting_status': member.voting_status,
                        'url': member.url
                    }
                yield json.dumps(member_dict, default=str) + '\n'
        
        filename = f"members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        
        return StreamingResponse(
            generate_jsonl(),
            media_type=self.mime_types['jsonl'],
            headers=headers
        )
    
    def _export_committees_csv(self, committees: List[Committee], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export committees as CSV."""
        if not fields:
            fields = ['committee_code', 'name', 'chamber', 'committee_type', 'url']
        
        def generate_csv():
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fields)
            
            writer.writeheader()
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)
            
            for committee in committees:
                row = {}
                for field in fields:
                    value = getattr(committee, field, '')
                    row[field] = value if value is not None else ''
                
                writer.writerow(row)
                yield output.getvalue()
                output.seek(0)
                output.truncate(0)
        
        filename = f"committees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        
        return StreamingResponse(generate_csv(), media_type=self.mime_types['csv'], headers=headers)
    
    def _export_committees_json(self, committees: List[Committee], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export committees as JSON."""
        data = []
        for committee in committees:
            committee_dict = {}
            if fields:
                for field in fields:
                    value = getattr(committee, field, None)
                    committee_dict[field] = value
            else:
                committee_dict = {
                    'committee_code': committee.committee_code,
                    'name': committee.name,
                    'chamber': committee.chamber,
                    'committee_type': committee.committee_type,
                    'url': committee.url
                }
            data.append(committee_dict)
        
        def generate_json():
            yield json.dumps({
                'export_timestamp': datetime.now().isoformat(),
                'total_records': len(data),
                'data': data
            }, indent=2, default=str)
        
        filename = f"committees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        
        return StreamingResponse(generate_json(), media_type=self.mime_types['json'], headers=headers)
    
    def _export_committees_jsonl(self, committees: List[Committee], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export committees as JSON Lines."""
        def generate_jsonl():
            for committee in committees:
                committee_dict = {}
                if fields:
                    for field in fields:
                        value = getattr(committee, field, None)
                        committee_dict[field] = value
                else:
                    committee_dict = {
                        'committee_code': committee.committee_code,
                        'name': committee.name,
                        'chamber': committee.chamber,
                        'committee_type': committee.committee_type,
                        'url': committee.url
                    }
                yield json.dumps(committee_dict, default=str) + '\n'
        
        filename = f"committees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        
        return StreamingResponse(generate_jsonl(), media_type=self.mime_types['jsonl'], headers=headers)
    
    def _export_hearings_csv(self, hearings: List[Hearing], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export hearings as CSV."""
        if not fields:
            fields = ['id', 'title', 'date', 'committee_id', 'url']
        
        def generate_csv():
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fields)
            
            writer.writeheader()
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)
            
            for hearing in hearings:
                row = {}
                for field in fields:
                    value = getattr(hearing, field, '')
                    # Convert date to string if present
                    if field == 'date' and value:
                        value = value.strftime('%Y-%m-%d') if hasattr(value, 'strftime') else str(value)
                    row[field] = value if value is not None else ''
                
                writer.writerow(row)
                yield output.getvalue()
                output.seek(0)
                output.truncate(0)
        
        filename = f"hearings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        
        return StreamingResponse(generate_csv(), media_type=self.mime_types['csv'], headers=headers)
    
    def _export_hearings_json(self, hearings: List[Hearing], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export hearings as JSON."""
        data = []
        for hearing in hearings:
            hearing_dict = {}
            if fields:
                for field in fields:
                    value = getattr(hearing, field, None)
                    # Convert date to string if present
                    if field == 'date' and value:
                        value = value.strftime('%Y-%m-%d') if hasattr(value, 'strftime') else str(value)
                    hearing_dict[field] = value
            else:
                hearing_dict = {
                    'id': hearing.id,
                    'title': hearing.title,
                    'date': hearing.date.strftime('%Y-%m-%d') if hearing.date else None,
                    'committee_id': hearing.committee_id,
                    'url': hearing.url
                }
            data.append(hearing_dict)
        
        def generate_json():
            yield json.dumps({
                'export_timestamp': datetime.now().isoformat(),
                'total_records': len(data),
                'data': data
            }, indent=2, default=str)
        
        filename = f"hearings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        
        return StreamingResponse(generate_json(), media_type=self.mime_types['json'], headers=headers)
    
    def _export_hearings_jsonl(self, hearings: List[Hearing], fields: Optional[List[str]] = None) -> StreamingResponse:
        """Export hearings as JSON Lines."""
        def generate_jsonl():
            for hearing in hearings:
                hearing_dict = {}
                if fields:
                    for field in fields:
                        value = getattr(hearing, field, None)
                        # Convert date to string if present
                        if field == 'date' and value:
                            value = value.strftime('%Y-%m-%d') if hasattr(value, 'strftime') else str(value)
                        hearing_dict[field] = value
                else:
                    hearing_dict = {
                        'id': hearing.id,
                        'title': hearing.title,
                        'date': hearing.date.strftime('%Y-%m-%d') if hearing.date else None,
                        'committee_id': hearing.committee_id,
                        'url': hearing.url
                    }
                yield json.dumps(hearing_dict, default=str) + '\n'
        
        filename = f"hearings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        
        return StreamingResponse(generate_jsonl(), media_type=self.mime_types['jsonl'], headers=headers)


# Global export service instance
export_service = DataExporter()