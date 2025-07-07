# API Deployment Troubleshooting Plan
## Congressional Data Platform - Phase 2C API Enhancement

**Date**: January 8, 2025  
**Status**: 🔄 **SYSTEMATIC TROUBLESHOOTING TO RESOLVE CLOUD RUN DEPLOYMENT ISSUE**  
**Priority**: High - Completing remaining 10% of Phase 2 implementation

## 🎯 OBJECTIVE

Resolve the Cloud Run container startup timeout issue that prevents deployment of URL fields in committee API endpoints, completing Phase 2C of the Congressional Data Platform enhancement.

## 📋 STEP-BY-STEP TROUBLESHOOTING PLAN

### **PHASE 1: DIAGNOSIS (Steps 1-5)**

#### **Step 1: Current State Assessment**
- **Action**: Verify existing working service configuration
- **Command**: `gcloud run services describe congressional-data-api-v2`
- **Goal**: Understand working baseline configuration
- **Success Criteria**: Extract current environment variables and settings

#### **Step 2: Container Image Verification**
- **Action**: Test container image locally
- **Command**: `docker run -p 8000:8000 gcr.io/chefgavin/congress-api:phase2c-url-fix`
- **Goal**: Verify container starts correctly outside of Cloud Run
- **Success Criteria**: Container listens on port 8000 successfully

#### **Step 3: Environment Variable Analysis**
- **Action**: Compare environment variables between working and failing deployments
- **Focus**: DATABASE_URL, CONGRESS_API_KEY, SECRET_KEY, DEBUG settings
- **Goal**: Identify missing or incorrect environment variables
- **Success Criteria**: All required environment variables identified and verified

#### **Step 4: Database Connection Testing**
- **Action**: Test database connectivity from container
- **Command**: Cloud SQL Proxy connection test
- **Goal**: Ensure database is accessible from deployment environment
- **Success Criteria**: Database connection successful

#### **Step 5: Port and Network Configuration**
- **Action**: Verify container port configuration
- **Focus**: PORT environment variable, FastAPI app binding
- **Goal**: Ensure container binds to correct port
- **Success Criteria**: Container responds on expected port

### **PHASE 2: RESOLUTION (Steps 6-10)**

#### **Step 6: Fix Container Configuration**
- **Action**: Update container to use dynamic PORT environment variable
- **Code**: Modify `backend/app/main.py` to use `os.environ.get("PORT", "8000")`
- **Goal**: Ensure Cloud Run can set port dynamically
- **Success Criteria**: Container respects PORT environment variable

#### **Step 7: Rebuild Container with Fixes**
- **Action**: Build new container image with port configuration fix
- **Command**: `docker build -t gcr.io/chefgavin/congress-api:phase2c-port-fix .`
- **Goal**: Create container that works with Cloud Run port requirements
- **Success Criteria**: New container image built and tested locally

#### **Step 8: Deploy with Minimal Configuration**
- **Action**: Deploy with only essential environment variables
- **Strategy**: Start with minimal config, add variables incrementally
- **Goal**: Identify problematic environment variables
- **Success Criteria**: Container starts successfully in Cloud Run

#### **Step 9: Incremental Environment Variable Addition**
- **Action**: Add environment variables one by one
- **Order**: DATABASE_URL → SECRET_KEY → CONGRESS_API_KEY → DEBUG
- **Goal**: Find the specific variable causing startup issues
- **Success Criteria**: Identify and fix problematic variables

#### **Step 10: Full Configuration Deployment**
- **Action**: Deploy with complete working configuration
- **Command**: `gcloud run deploy` with all verified environment variables
- **Goal**: Complete deployment with URL fields working
- **Success Criteria**: All API endpoints responding with URL fields

### **PHASE 3: VALIDATION (Steps 11-15)**

#### **Step 11: API Endpoint Testing**
- **Action**: Test committee endpoint with URL fields
- **Command**: `curl "/api/v1/committees/1"` and verify URL fields present
- **Goal**: Confirm URL fields are exposed in API responses
- **Success Criteria**: hearings_url, members_url, official_website_url present

#### **Step 12: Database Schema Verification**
- **Action**: Verify database schema matches API expectations
- **Command**: Connect to database and check committee table structure
- **Goal**: Ensure schema consistency between database and API
- **Success Criteria**: All URL columns exist and populated

#### **Step 13: Multiple Committee Testing**
- **Action**: Test URL fields across multiple committees
- **Command**: Test House and Senate committees for URL field presence
- **Goal**: Verify consistent URL field availability
- **Success Criteria**: 35 committees return URL fields correctly

#### **Step 14: Frontend Integration Testing**
- **Action**: Test frontend consumption of URL fields
- **Command**: Load committee detail page and verify resource buttons
- **Goal**: Confirm end-to-end functionality works
- **Success Criteria**: Resource buttons link to correct URLs

#### **Step 15: Performance and Stability Testing**
- **Action**: Test API performance and stability with URL fields
- **Command**: Load testing with multiple requests
- **Goal**: Ensure URL fields don't impact performance
- **Success Criteria**: Response times remain under 500ms

### **PHASE 4: DOCUMENTATION (Steps 16-17)**

#### **Step 16: Update Documentation**
- **Action**: Update README.md with Phase 2C completion
- **Content**: Document URL field functionality and usage
- **Goal**: Provide clear documentation for URL field features
- **Success Criteria**: Complete documentation updated

#### **Step 17: Commit and Version Control**
- **Action**: Commit all changes to git repository
- **Command**: `git add .`, `git commit -m "Phase 2C: API Enhancement - URL fields deployed"`
- **Goal**: Document implementation for future reference
- **Success Criteria**: All changes committed with proper messages

## 🔧 TECHNICAL DEBUGGING DETAILS

### **Common Cloud Run Issues**
1. **PORT Environment Variable**: Container must bind to PORT env var, not hardcoded port
2. **Database Connection**: Cloud SQL connections require proper IAM permissions
3. **Environment Variables**: Missing or incorrect variables cause startup failures
4. **Container Health**: Container must respond to health checks within timeout
5. **Resource Allocation**: Insufficient memory or CPU can cause startup failures

### **Specific Issues to Check**
- **Database Connection String**: Verify Cloud SQL connection format
- **API Key Configuration**: Ensure Congress.gov API key is valid
- **Secret Key**: Check SECRET_KEY is properly configured
- **Debug Mode**: Verify DEBUG setting doesn't conflict with production

### **Environment Variable Format**
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
CONGRESS_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
DEBUG=false
PORT=8000
```

## 🎯 SUCCESS CRITERIA

### **Deployment Success**
- ✅ Container starts successfully in Cloud Run (no timeout)
- ✅ Health endpoint responds correctly
- ✅ Database connection established
- ✅ All environment variables configured properly

### **API Functionality**
- ✅ Committee endpoints return URL fields
- ✅ All 35 committees have URL data
- ✅ hearings_url, members_url, official_website_url present
- ✅ last_url_update timestamp accurate

### **Integration Testing**
- ✅ Frontend can consume URL fields
- ✅ Resource buttons link to correct URLs
- ✅ End-to-end functionality works
- ✅ Performance remains optimal

### **Documentation**
- ✅ README.md updated with Phase 2C completion
- ✅ All changes committed to git
- ✅ Implementation documented for future reference

## 📊 EXPECTED OUTCOMES

### **Phase 2C Completion**
- **Status**: ✅ **COMPLETE** (API Enhancement with URL fields)
- **Result**: Committee endpoints expose official resource URLs
- **Impact**: Frontend can display official resource buttons
- **User Value**: Direct access to official committee resources

### **Phase 2 Overall Status**
- **Phase 2A**: ✅ Database Enhancement (100%)
- **Phase 2B**: ✅ Web Scraping Framework (100%)
- **Phase 2C**: 🔄 API Enhancement (completing from 60% to 100%)
- **Phase 2D**: ✅ Frontend Integration (100%)
- **Phase 2E**: ✅ URL Validation (100%)
- **Overall**: 🎯 **100% COMPLETE**

## 🚀 NEXT STEPS AFTER COMPLETION

1. **URL Quality Improvement**: Fix 37 broken URLs identified during validation
2. **Performance Optimization**: Add caching for URL field queries
3. **Enhanced Documentation**: Update user guides with new features
4. **Phase 3 Planning**: Plan next enhancement phase based on user feedback

## 📝 IMPLEMENTATION NOTES

- **Time Estimate**: 2-3 hours for complete troubleshooting and resolution
- **Risk Level**: Low (existing working service as baseline)
- **Rollback Plan**: Revert to previous working container if needed
- **Dependencies**: None (all components ready for deployment)

---

**Implementation Plan**: Systematic approach to resolve Cloud Run deployment issue  
**Goal**: Complete Phase 2C API Enhancement and achieve 100% Phase 2 completion  
**Priority**: High - Complete remaining 10% of Phase 2 implementation