"""
Advanced features API endpoints for Congressional Data Automation Service.
Includes data export and enhanced search functionality.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import structlog

from ...core.database import get_db
from ...core.security import InputValidator, ParameterValidator
from ...services.export_service import export_service
from ...services.search_service import search_service
from ...middleware.cache_middleware import cache_response

logger = structlog.get_logger()
router = APIRouter()


# ========================================
# DATA EXPORT ENDPOINTS
# ========================================

@router.get("/export/members")
async def export_members(
    format: str = Query("csv", description="Export format: csv, json, jsonl"),
    state: Optional[str] = Query(None, description="Filter by state"),
    party: Optional[str] = Query(None, description="Filter by party"),
    chamber: Optional[str] = Query(None, description="Filter by chamber"),
    voting_status: Optional[str] = Query(None, description="Filter by voting status"),
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to export"),
    db: Session = Depends(get_db)
):
    """Export members data in specified format with optional filtering."""
    try:
        # Build filters
        filters = {}
        if state:
            is_valid, error, clean_state = InputValidator.validate_input(state, 'state_code', False)
            if is_valid and clean_state:
                filters['state'] = clean_state
        
        if party:
            is_valid, error, clean_party = InputValidator.validate_input(party, 'party', False)
            if is_valid and clean_party:
                filters['party'] = clean_party
        
        if chamber:
            is_valid, error, clean_chamber = InputValidator.validate_input(chamber, 'chamber', False)
            if is_valid and clean_chamber:
                filters['chamber'] = clean_chamber
        
        if voting_status:
            filters['voting_status'] = voting_status
        
        # Parse fields list
        field_list = None
        if fields:
            field_list = [f.strip() for f in fields.split(',') if f.strip()]
        
        # Export data
        return await export_service.export_members(db, format, filters, field_list)
        
    except Exception as e:
        logger.error(f"Member export failed: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/export/committees")
async def export_committees(
    format: str = Query("csv", description="Export format: csv, json, jsonl"),
    chamber: Optional[str] = Query(None, description="Filter by chamber"),
    committee_type: Optional[str] = Query(None, description="Filter by committee type"),
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to export"),
    db: Session = Depends(get_db)
):
    """Export committees data in specified format with optional filtering."""
    try:
        # Build filters
        filters = {}
        if chamber:
            is_valid, error, clean_chamber = InputValidator.validate_input(chamber, 'chamber', False)
            if is_valid and clean_chamber:
                filters['chamber'] = clean_chamber
        
        if committee_type:
            filters['committee_type'] = committee_type
        
        # Parse fields list
        field_list = None
        if fields:
            field_list = [f.strip() for f in fields.split(',') if f.strip()]
        
        # Export data
        return await export_service.export_committees(db, format, filters, field_list)
        
    except Exception as e:
        logger.error(f"Committee export failed: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/export/hearings")
async def export_hearings(
    format: str = Query("csv", description="Export format: csv, json, jsonl"),
    committee_id: Optional[int] = Query(None, description="Filter by committee ID"),
    date_from: Optional[str] = Query(None, description="Filter by date from (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter by date to (YYYY-MM-DD)"),
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to export"),
    db: Session = Depends(get_db)
):
    """Export hearings data in specified format with optional filtering."""
    try:
        # Build filters
        filters = {}
        if committee_id:
            filters['committee_id'] = committee_id
        
        if date_from:
            is_valid, error, clean_date = InputValidator.validate_input(date_from, 'date', False)
            if is_valid and clean_date:
                filters['date_from'] = clean_date
        
        if date_to:
            is_valid, error, clean_date = InputValidator.validate_input(date_to, 'date', False)
            if is_valid and clean_date:
                filters['date_to'] = clean_date
        
        # Parse fields list
        field_list = None
        if fields:
            field_list = [f.strip() for f in fields.split(',') if f.strip()]
        
        # Export data
        return await export_service.export_hearings(db, format, filters, field_list)
        
    except Exception as e:
        logger.error(f"Hearing export failed: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


# ========================================
# ENHANCED SEARCH ENDPOINTS
# ========================================

@router.get("/search/members")
@cache_response("search", ttl=1800)  # 30 minute cache
async def search_members(
    q: str = Query(..., description="Search query", min_length=1),
    state: Optional[str] = Query(None, description="Filter by state"),
    party: Optional[str] = Query(None, description="Filter by party"),
    chamber: Optional[str] = Query(None, description="Filter by chamber"),
    voting_status: Optional[str] = Query(None, description="Filter by voting status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=1000, description="Results per page"),
    db: Session = Depends(get_db)
):
    """Search members with full-text search and filtering."""
    try:
        # Validate pagination
        is_valid, error, clean_page, clean_limit = ParameterValidator.validate_pagination_params(page, limit)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)
        
        # Build filters
        filters = {}
        if state:
            filters['state'] = state
        if party:
            filters['party'] = party
        if chamber:
            filters['chamber'] = chamber
        if voting_status:
            filters['voting_status'] = voting_status
        
        # Validate filters
        if filters:
            is_valid, error, validated_filters = ParameterValidator.validate_filter_params(filters)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            filters = validated_filters
        
        # Calculate offset
        offset = (clean_page - 1) * clean_limit
        
        # Perform search
        members, total_count = await search_service.search_members(
            db, q, filters, clean_limit, offset
        )
        
        # Calculate pagination info
        total_pages = (total_count + clean_limit - 1) // clean_limit
        
        return {
            "query": q,
            "results": [search_service._serialize_member(m) for m in members],
            "pagination": {
                "page": clean_page,
                "limit": clean_limit,
                "total_results": total_count,
                "total_pages": total_pages,
                "has_next": clean_page < total_pages,
                "has_prev": clean_page > 1
            },
            "filters": filters
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Member search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/search/committees")
@cache_response("search", ttl=1800)  # 30 minute cache
async def search_committees(
    q: str = Query(..., description="Search query", min_length=1),
    chamber: Optional[str] = Query(None, description="Filter by chamber"),
    committee_type: Optional[str] = Query(None, description="Filter by committee type"),
    parent_committee_id: Optional[str] = Query(None, description="Filter by parent committee (use 'null' for main committees)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=1000, description="Results per page"),
    db: Session = Depends(get_db)
):
    """Search committees with full-text search and filtering."""
    try:
        # Validate pagination
        is_valid, error, clean_page, clean_limit = ParameterValidator.validate_pagination_params(page, limit)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)
        
        # Build filters
        filters = {}
        if chamber:
            filters['chamber'] = chamber
        if committee_type:
            filters['committee_type'] = committee_type
        if parent_committee_id:
            filters['parent_committee_id'] = parent_committee_id
        
        # Calculate offset
        offset = (clean_page - 1) * clean_limit
        
        # Perform search
        committees, total_count = await search_service.search_committees(
            db, q, filters, clean_limit, offset
        )
        
        # Calculate pagination info
        total_pages = (total_count + clean_limit - 1) // clean_limit
        
        return {
            "query": q,
            "results": [search_service._serialize_committee(c) for c in committees],
            "pagination": {
                "page": clean_page,
                "limit": clean_limit,
                "total_results": total_count,
                "total_pages": total_pages,
                "has_next": clean_page < total_pages,
                "has_prev": clean_page > 1
            },
            "filters": filters
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Committee search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/search/hearings")
@cache_response("search", ttl=1800)  # 30 minute cache
async def search_hearings(
    q: str = Query(..., description="Search query", min_length=1),
    committee_id: Optional[int] = Query(None, description="Filter by committee ID"),
    date_from: Optional[str] = Query(None, description="Filter by date from (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter by date to (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=1000, description="Results per page"),
    db: Session = Depends(get_db)
):
    """Search hearings with full-text search and filtering."""
    try:
        # Validate pagination
        is_valid, error, clean_page, clean_limit = ParameterValidator.validate_pagination_params(page, limit)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)
        
        # Build filters
        filters = {}
        if committee_id:
            filters['committee_id'] = committee_id
        if date_from:
            filters['date_from'] = date_from
        if date_to:
            filters['date_to'] = date_to
        
        # Calculate offset
        offset = (clean_page - 1) * clean_limit
        
        # Perform search
        hearings, total_count = await search_service.search_hearings(
            db, q, filters, clean_limit, offset
        )
        
        # Calculate pagination info
        total_pages = (total_count + clean_limit - 1) // clean_limit
        
        return {
            "query": q,
            "results": [search_service._serialize_hearing(h) for h in hearings],
            "pagination": {
                "page": clean_page,
                "limit": clean_limit,
                "total_results": total_count,
                "total_pages": total_pages,
                "has_next": clean_page < total_pages,
                "has_prev": clean_page > 1
            },
            "filters": filters
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Hearing search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/search/global")
@cache_response("search", ttl=1800)  # 30 minute cache
async def global_search(
    q: str = Query(..., description="Search query", min_length=1),
    types: Optional[str] = Query(None, description="Comma-separated list of types to search: members,committees,hearings"),
    limit_per_type: int = Query(10, ge=1, le=50, description="Maximum results per type"),
    db: Session = Depends(get_db)
):
    """Perform global search across all data types."""
    try:
        # Parse search types
        search_types = None
        if types:
            search_types = [t.strip() for t in types.split(',') if t.strip()]
            valid_types = ['members', 'committees', 'hearings']
            search_types = [t for t in search_types if t in valid_types]
        
        # Perform global search
        results = await search_service.global_search(db, q, search_types, limit_per_type)
        
        return results
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Global search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/search/suggestions")
@cache_response("search", ttl=3600)  # 1 hour cache
async def get_search_suggestions(
    q: str = Query(..., description="Partial search query", min_length=2),
    type: Optional[str] = Query(None, description="Suggestion type: members,committees,states,parties"),
    limit: int = Query(10, ge=1, le=50, description="Maximum suggestions"),
    db: Session = Depends(get_db)
):
    """Get search suggestions/autocomplete results."""
    try:
        suggestions = await search_service.get_search_suggestions(db, q, type, limit)
        
        return {
            "query": q,
            "suggestions": suggestions,
            "type": type
        }
        
    except Exception as e:
        logger.error(f"Search suggestions failed: {e}")
        raise HTTPException(status_code=500, detail="Suggestions failed")


@router.get("/search/filters")
@cache_response("search", ttl=3600)  # 1 hour cache
async def get_search_filters(db: Session = Depends(get_db)):
    """Get available filter options for advanced search."""
    try:
        filters = await search_service.get_advanced_filters(db)
        
        return {
            "available_filters": filters,
            "description": "Available filter options for advanced search"
        }
        
    except Exception as e:
        logger.error(f"Get search filters failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get filter options")