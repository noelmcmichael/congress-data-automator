# Congressional Data API - Filter Debug Plan

## 🚨 Critical Issue: Search/Filter Logic Not Working

### Problem Description
- API filters are completely ignored (e.g., `?party=Republican` returns Democrats too)
- Even nonsensical filters like `?party=XYZ` return results
- Affects all endpoints: `/members`, `/committees`, `/hearings`
- Current deployment: `congressional-data-api-v2-1066017671167.us-central1.run.app`

### Root Cause Analysis Plan

## Phase 1: Local Investigation & Debugging (Steps 1-5)

### Step 1: Environment Setup & Database Inspection
- [ ] Set up local development environment
- [ ] Connect to production database via Cloud SQL proxy
- [ ] Inspect actual data values in database tables
- [ ] Verify column names and data types match expectations

### Step 2: Enable SQL Query Logging
- [ ] Add SQLAlchemy query logging to see actual SQL generated
- [ ] Create debug endpoint to log filter parameters
- [ ] Test filtering logic with verbose logging
- [ ] Compare expected vs actual SQL queries

### Step 3: Isolate Backend vs Frontend Issues
- [ ] Test API endpoints directly with curl/httpie
- [ ] Create simple test script to verify filter behavior
- [ ] Test with production API vs local API
- [ ] Document exact differences in behavior

### Step 4: Database Query Verification
- [ ] Run raw SQL queries directly on database
- [ ] Test filter conditions manually in SQL
- [ ] Verify data integrity and expected values
- [ ] Check for case sensitivity issues

### Step 5: SQLAlchemy Filter Logic Review
- [ ] Review filter implementation in data_retrieval.py
- [ ] Test each filter condition individually
- [ ] Check for ORM query construction issues
- [ ] Verify parameter parsing and type conversion

## Phase 2: Fix Implementation (Steps 6-8)

### Step 6: Implement Logging & Debugging Tools
- [ ] Add request/response logging middleware
- [ ] Create debug endpoint showing filter parameters
- [ ] Add SQL query execution logging
- [ ] Create comprehensive test cases

### Step 7: Fix Filter Logic
- [ ] Implement corrected filter conditions
- [ ] Add input validation and sanitization
- [ ] Test edge cases and error conditions
- [ ] Verify fix works for all filter combinations

### Step 8: Enhanced Testing & Validation
- [ ] Create automated test suite for all filters
- [ ] Test with real production data
- [ ] Verify no regressions in existing functionality
- [ ] Performance testing with large datasets

## Phase 3: Deployment & Verification (Steps 9-10)

### Step 9: Deployment
- [ ] Build and deploy fixed version to Cloud Run
- [ ] Run smoke tests on production environment
- [ ] Monitor logs for any deployment issues
- [ ] Update frontend to use fixed API version

### Step 10: Production Validation
- [ ] Test all filter combinations in production
- [ ] Verify frontend search functionality works
- [ ] Monitor API performance and error rates
- [ ] Document final solution and lessons learned

## Testing Strategy

### Test Cases to Implement
1. **Party Filter**: `?party=Republican` should return only Republicans
2. **State Filter**: `?state=CA` should return only California members
3. **Chamber Filter**: `?chamber=house` should return only House members
4. **Combined Filters**: `?party=Democratic&state=NY` should return NY Democrats
5. **Invalid Filters**: `?party=INVALID` should return empty results
6. **Case Sensitivity**: Test various case combinations
7. **Pagination**: Ensure filters work correctly with pagination

### Expected Outcomes
- Filters should work as expected
- Invalid filters should return appropriate responses
- Performance should remain acceptable
- No regressions in existing functionality

## Tools & Resources

### Development Tools
- Cloud SQL proxy for database access
- SQLAlchemy logging for query inspection
- Postman/curl for API testing
- Python debugging tools

### Production Services
- Backend API: https://congressional-data-api-v2-1066017671167.us-central1.run.app
- Frontend: https://storage.googleapis.com/congressional-data-frontend/index.html
- Database: Google Cloud SQL PostgreSQL

### Key Files to Modify
- `backend/app/api/v1/data_retrieval.py` - Main filter logic
- `backend/app/core/database.py` - Database connection and logging
- `backend/app/main.py` - Application configuration
- Test files for validation

## Success Criteria

1. **Functional**: All filters work correctly and return expected results
2. **Performance**: Response times remain under 500ms for typical queries
3. **Reliability**: No errors or crashes under normal usage
4. **Completeness**: All endpoints (members, committees, hearings) work correctly
5. **User Experience**: Frontend search functionality works seamlessly

## Risk Mitigation

- Use separate service deployment to avoid disrupting working features
- Implement comprehensive logging before making changes
- Test thoroughly in local environment before deploying
- Keep rollback plan ready in case issues arise

---

**Next Action**: Begin with Step 1 - Environment Setup & Database Inspection