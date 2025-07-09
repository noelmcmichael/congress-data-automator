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
- [x] Set up local development environment ✅
- [x] Connect to production database via Cloud SQL proxy ✅
- [x] Inspect actual data values in database tables ✅
- [x] Verify column names and data types match expectations ✅

**KEY FINDINGS:**
- Database has correct data: 538 members, proper party/chamber/state values
- SQLAlchemy filtering works perfectly at database level
- Local filter testing returns correct results (264 Republicans, 483 House, 45 Dem CA)
- Issue is NOT in the database or SQLAlchemy logic

### Step 2: Enable SQL Query Logging
- [x] Add SQLAlchemy query logging to see actual SQL generated ✅
- [x] Create debug endpoint to log filter parameters ✅
- [x] Test filtering logic with verbose logging ✅
- [x] Compare expected vs actual SQL queries ✅

**KEY FINDINGS:**
- SQL queries are correctly generated with proper WHERE clauses
- Filter parameters are parsed correctly by FastAPI
- Database returns correct filtered results when queried directly
- Issue is NOT in SQL generation or query logic

### Step 3: Isolate Backend vs Frontend Issues
- [x] Test API endpoints directly with curl/httpie ✅
- [x] Create simple test script to verify filter behavior ✅
- [x] Test with production API vs local API ✅
- [x] Document exact differences in behavior ✅

**KEY FINDINGS:**
- Production API ignores ALL filters (returns same 50 results regardless)
- All filter combinations return identical results
- API returns same 3 members in every query: Ramirez, Sheehy, Luján
- Issue is DEFINITELY in the production API deployment

### Step 4: Database Query Verification
- [x] Run raw SQL queries directly on database ✅
- [x] Test filter conditions manually in SQL ✅
- [x] Verify data integrity and expected values ✅
- [x] Check for case sensitivity issues ✅

**KEY FINDINGS:**
- Raw SQL queries work perfectly: 264 Republicans, 483 House, 45 Dem CA
- No case sensitivity issues found
- Data integrity is excellent
- All filter combinations return correct results in database

### Step 5: SQLAlchemy Filter Logic Review
- [x] Review filter implementation in data_retrieval.py ✅
- [x] Test each filter condition individually ✅
- [x] Check for ORM query construction issues ✅
- [x] Verify parameter parsing and type conversion ✅

**KEY FINDINGS:**
- Filter implementation in data_retrieval.py looks correct
- All filter conditions work when tested individually
- No ORM query construction issues found
- Parameter parsing works correctly
- **ROOT CAUSE IDENTIFIED**: Production API is not running the latest code with filters

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

## 🎯 ROOT CAUSE IDENTIFIED

### Problem Analysis Results
After comprehensive testing, we've identified the root cause:

**The production API deployment is NOT running the latest code with filter logic.**

### Evidence:
1. **Database Level**: ✅ All filters work correctly (264 Republicans, 483 House, 45 Dem CA)
2. **SQLAlchemy Level**: ✅ Filter logic generates correct SQL queries
3. **Code Level**: ✅ Filter implementation in data_retrieval.py is correct
4. **API Level**: ❌ Production API ignores all filters, returns same 50 results

### Hypothesis:
The production service `congressional-data-api-v2-1066017671167.us-central1.run.app` is either:
1. Running an older version of the code without proper filter implementation
2. Has a deployment/caching issue preventing the latest code from running
3. Has a different configuration that's overriding the filter logic

### Next Steps:
- **Step 6**: Verify current deployment version and rebuild/redeploy
- **Step 7**: Test deployment with logging to confirm filter logic is active
- **Step 8**: Validate fixed functionality in production

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