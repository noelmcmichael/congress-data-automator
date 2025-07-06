# Congressional Data Platform - Relationship Enhancement Plan

## Project Overview
Enhance the existing Congressional Data platform with relationship functionality and detailed entity pages to show connections between Members, Committees, and Hearings.

## Current State Analysis

### Database Schema ✅
- **Members**: Full model with committee_memberships relationship
- **Committees**: Full model with parent/child relationships, memberships, and hearings
- **Hearings**: Full model with committee and witness relationships
- **CommitteeMembership**: Junction table for member-committee relationships
- **Witnesses**: Related to hearings
- **HearingDocuments**: Related to hearings

### Data Quality Issues Identified
- **Committees**: Have basic data but missing parent-child relationships
- **Hearings**: Mostly empty data (no titles, dates, committee associations)
- **Committee Memberships**: Not populated in database
- **Subcommittees**: Not properly categorized

## Implementation Plan

### Phase 1: Data Enhancement & Relationship Population
**Goal**: Populate missing relationship data and improve data quality

#### Step 1.1: Enhanced Data Collection
- [ ] Update data collection scripts to fetch committee membership data
- [ ] Improve hearing data collection with proper committee associations
- [ ] Add subcommittee hierarchy data collection
- [ ] Update committee data with proper parent-child relationships

#### Step 1.2: Database Migration & Data Population
- [ ] Create migration script to populate existing relationships
- [ ] Populate committee memberships for all current members
- [ ] Establish proper committee-subcommittee hierarchies
- [ ] Associate hearings with their respective committees

### Phase 2: Backend API Enhancement
**Goal**: Create detailed entity endpoints with relationship data

#### Step 2.1: New API Endpoints
- [ ] `/api/v1/members/{id}` - Member detail with committee memberships
- [ ] `/api/v1/committees/{id}` - Committee detail with members and hearings
- [ ] `/api/v1/hearings/{id}` - Hearing detail with committee and witnesses
- [ ] `/api/v1/members/{id}/committees` - Member's committee memberships
- [ ] `/api/v1/committees/{id}/members` - Committee membership roster
- [ ] `/api/v1/committees/{id}/hearings` - Committee's hearings
- [ ] `/api/v1/committees/{id}/subcommittees` - Committee's subcommittees

#### Step 2.2: Enhanced Response Models
- [ ] Add relationship data to existing list endpoints
- [ ] Create detailed response models for entity pages
- [ ] Add aggregation endpoints for relationship statistics

### Phase 3: Frontend Enhancement
**Goal**: Create detailed entity pages with relationship navigation

#### Step 3.1: Detail Pages
- [ ] Member detail page with committee memberships and related hearings
- [ ] Committee detail page with member roster and hearing schedule
- [ ] Hearing detail page with committee context and witness list
- [ ] Subcommittee distinction and hierarchy display

#### Step 3.2: Navigation & Relationships
- [ ] Cross-entity navigation (member → committees → hearings)
- [ ] Relationship visualizations (member committee network)
- [ ] Related entities sidebar on each detail page
- [ ] Breadcrumb navigation for committee hierarchies

#### Step 3.3: Advanced Features
- [ ] Search across relationships (find members by committee)
- [ ] Filter by relationship type (committee chairs, subcommittee members)
- [ ] Relationship statistics and insights
- [ ] Timeline view of member committee service

### Phase 4: Data Visualization & Analytics
**Goal**: Visual representation of relationships and insights

#### Step 4.1: Relationship Visualizations
- [ ] Committee membership network graph
- [ ] Member collaboration matrix (shared committees)
- [ ] Hearing participation timeline
- [ ] Committee activity heatmap

#### Step 4.2: Analytics Dashboard
- [ ] Committee membership statistics
- [ ] Hearing participation analytics
- [ ] Cross-party collaboration metrics
- [ ] Subcommittee vs main committee activity

## Technical Implementation Details

### Database Enhancements
```sql
-- Committee Membership Population
INSERT INTO committee_memberships (member_id, committee_id, position, is_current)
SELECT m.id, c.id, 'Member', true
FROM members m, committees c
WHERE [committee membership logic based on scraped data]

-- Subcommittee Hierarchy
UPDATE committees 
SET parent_committee_id = [parent_id], is_subcommittee = true
WHERE [subcommittee identification logic]
```

### API Response Structure
```json
{
  "member": {
    "id": 1,
    "name": "John Doe",
    "committees": [
      {
        "id": 1,
        "name": "House Energy and Commerce",
        "position": "Member",
        "is_chair": false,
        "subcommittees": [
          {
            "id": 2,
            "name": "Health Subcommittee",
            "position": "Chair"
          }
        ]
      }
    ],
    "recent_hearings": [...],
    "statistics": {
      "total_committees": 3,
      "chair_positions": 1,
      "hearings_attended": 25
    }
  }
}
```

### Frontend Component Structure
```
components/
├── details/
│   ├── MemberDetail.tsx
│   ├── CommitteeDetail.tsx
│   └── HearingDetail.tsx
├── relationships/
│   ├── RelationshipCard.tsx
│   ├── CommitteeMembershipList.tsx
│   └── RelatedEntitiesNav.tsx
├── visualizations/
│   ├── NetworkGraph.tsx
│   ├── HeatmapChart.tsx
│   └── TimelineChart.tsx
└── common/
    ├── EntityCard.tsx
    └── RelationshipBadge.tsx
```

## Success Metrics
- [ ] All members have committee membership data
- [ ] All committees have proper parent-child relationships
- [ ] All hearings are associated with committees
- [ ] Detail pages show comprehensive relationship data
- [ ] Cross-entity navigation works seamlessly
- [ ] Users can discover relationships intuitively

## Risk Mitigation
1. **Data Quality**: Implement validation checks for relationship data
2. **Performance**: Use pagination and caching for relationship queries
3. **Complexity**: Progressive disclosure of relationship information
4. **User Experience**: Clear navigation and relationship indicators

## Timeline Estimate
- **Phase 1**: 2-3 days (data enhancement)
- **Phase 2**: 3-4 days (backend API)
- **Phase 3**: 4-5 days (frontend enhancement)
- **Phase 4**: 2-3 days (visualizations)
- **Total**: 11-15 days

## Priority Order
1. **Data Population** (Phase 1) - Foundation for everything else
2. **Member Detail Pages** (Phase 3.1) - Most user-requested feature
3. **Committee Detail Pages** (Phase 3.1) - High value for understanding
4. **Cross-entity Navigation** (Phase 3.2) - Core relationship functionality
5. **Visualizations** (Phase 4) - Advanced features for power users

This plan transforms the current data platform into a comprehensive relationship-aware system that provides deep insights into congressional structures and activities.