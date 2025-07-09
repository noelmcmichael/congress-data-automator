# Congressional Data Platform Refinement Plan

## Overview
Transform the homepage from navigation-focused to data quality/system health dashboard while cleaning up non-functional features.

## Current State Analysis
- **Homepage**: Navigation-focused with Quick Access cards (broken navigation)
- **Senator Timeline**: Not working, not needed
- **Settings Page**: Mixed relevance, needs audit for current functionality
- **Left Navigation**: Working well for core database access

## Phase 1: Homepage Transformation (Data Quality & System Health Focus)

### Goals
- Remove broken Quick Access navigation
- Add system health monitoring dashboard
- Focus on data quality metrics and automation status
- Maintain left sidebar as primary navigation

### Implementation
1. **Remove Quick Access Cards**
   - Replace with system health dashboard
   - Fix React Router navigation issues

2. **Add Data Quality Metrics**
   - Database health indicators
   - Data freshness timestamps
   - Validation status
   - Coverage gap reports

3. **Add Automation Status**
   - Scheduled job status
   - Last run times
   - Success/failure rates
   - Queue status

4. **Add System Monitoring**
   - API health checks
   - Database connection status
   - Error rates
   - Performance metrics

## Phase 2: Remove Senator Timeline

### Goals
- Remove non-functional Senator Timeline feature
- Clean up unused code and routes

### Implementation
1. **Remove Route** from App.tsx
2. **Remove Navigation Item** from Navigation.tsx
3. **Delete Component File** SenatorTimeline.tsx
4. **Clean Up Imports**

## Phase 3: Settings Page Audit & Cleanup

### Current Settings Review
- **API Testing** (Congress API, Scrapers) - ✅ Relevant
- **Data Management switches** - ❓ May not be functional
- **System Information** - ✅ Relevant but needs update
- **Update frequency settings** - ❓ May not be connected

### Implementation
1. **Audit Functionality**
   - Test API testing features
   - Verify data management toggles
   - Check system information accuracy

2. **Remove Non-functional Features**
   - Clean up dead code
   - Remove unused toggles
   - Remove broken settings

3. **Update System Info**
   - Current API URLs
   - Accurate version numbers
   - Build timestamps

4. **Add Relevant New Settings**
   - Data quality thresholds
   - Health monitoring intervals
   - Alert preferences

## Phase 4: Comprehensive Testing & Deployment

### Implementation
1. **Local Development Setup**
   - Clean build environment
   - Fresh dependencies

2. **Component Testing**
   - Verify navigation works
   - Test new dashboard features

3. **API Integration Testing**
   - Confirm health endpoints
   - Test data quality metrics

4. **Build and Deploy**
   - Production deployment
   - Monitor for issues

5. **End-to-End Testing**
   - Full system verification
   - User acceptance testing

## Success Criteria
- Homepage shows meaningful data quality and system health information
- All navigation uses React Router (no window.location.href)
- Senator Timeline removed completely
- Settings page shows only functional, relevant features
- All changes committed and documented in README.md

## Time Estimate
- Phase 1: 2-3 hours
- Phase 2: 30 minutes
- Phase 3: 1-2 hours
- Phase 4: 1 hour
- **Total**: 4.5-6.5 hours

## Risk Assessment
- **Low Risk**: Remove Senator Timeline, fix navigation
- **Medium Risk**: Settings page audit (unknown functionality)
- **High Risk**: Homepage transformation (new API endpoints may be needed)

## Next Steps
1. Review plan with user
2. Get approval for approach
3. Begin Phase 1 implementation
4. Commit after each successful phase