# Cloud Run Deployment Troubleshooting Plan

## 🚨 CURRENT ISSUE
- **Error**: Container failed to start and listen on PORT=8080 environment variable
- **Service**: congressional-data-api-v3
- **Revision**: congressional-data-api-v3-00002-xtz
- **Status**: Container timeout during startup

## 🔍 PHASE 1: DIAGNOSTIC ANALYSIS (15 minutes)

### Step 1: Check Current Service Configuration
- [ ] Examine current Cloud Run service settings
- [ ] Verify PORT environment variable configuration
- [ ] Check container image and tag
- [ ] Review service allocation settings (CPU, memory, timeout)

### Step 2: Examine Container and Port Configuration
- [ ] Analyze main.py port configuration
- [ ] Review Dockerfile CMD statement
- [ ] Check environment variable handling
- [ ] Verify uvicorn startup parameters

### Step 3: Access and Analyze Cloud Run Logs
- [ ] Get detailed logs from failed revision
- [ ] Check for specific error messages
- [ ] Identify startup sequence failures
- [ ] Look for port binding issues

## 🔧 PHASE 2: CONFIGURATION FIXES (30 minutes)

### Step 4: Fix Port Configuration Issues
- [ ] Ensure consistent PORT environment variable handling
- [ ] Update Dockerfile CMD if needed
- [ ] Fix any uvicorn startup parameters
- [ ] Test port binding locally

### Step 5: Cloud Run Service Settings
- [ ] Set correct PORT environment variable (8080 vs 8000)
- [ ] Increase startup timeout if needed
- [ ] Verify CPU and memory allocation
- [ ] Check service account permissions

### Step 6: Container Image Rebuild
- [ ] Rebuild container with fixes
- [ ] Tag with new version
- [ ] Push to Google Container Registry
- [ ] Verify image exists and is accessible

## 🚀 PHASE 3: DEPLOYMENT AND VALIDATION (20 minutes)

### Step 7: Deploy Fixed Configuration
- [ ] Deploy new container image
- [ ] Set correct environment variables
- [ ] Configure service settings
- [ ] Monitor deployment logs

### Step 8: Test Local Container First
- [ ] Run container locally with PORT=8080
- [ ] Test API endpoints
- [ ] Verify startup sequence
- [ ] Confirm port binding

### Step 9: Validate Production Deployment
- [ ] Check service health endpoint
- [ ] Test API endpoints
- [ ] Verify URL fields in API responses
- [ ] Monitor service logs

## 📊 PHASE 4: COMPLETION VALIDATION (10 minutes)

### Step 10: Complete Phase 2 Verification
- [ ] Test enhanced API endpoints
- [ ] Verify committee URL fields
- [ ] Check frontend integration
- [ ] Update README with completion status

## 🔍 DETAILED TROUBLESHOOTING CHECKLIST

### Port Configuration Issues
1. **Environment Variable Mismatch**: Cloud Run expects PORT=8080, code might use 8000
2. **Dockerfile CMD**: May not properly use PORT environment variable
3. **Uvicorn Binding**: Check if uvicorn is binding to correct host/port
4. **Startup Timeout**: Container might be taking too long to start

### Common Cloud Run Issues
1. **Container not listening on 0.0.0.0**: Must bind to all interfaces
2. **Port not from environment**: Must use PORT env var, not hardcoded
3. **Long startup time**: Database connections might be slow
4. **Health check failures**: Endpoints might not be responding

### Deployment Configuration
1. **Service account permissions**: Database access issues
2. **Environment variables**: Missing or incorrect values
3. **Resource limits**: Insufficient CPU/memory for startup
4. **Network connectivity**: Database connection issues

## 📋 SUCCESS CRITERIA

✅ **Container Starts Successfully**
- Cloud Run service shows "Serving traffic"
- Health check endpoints respond
- No timeout errors in logs

✅ **API Endpoints Working**
- /health returns 200 OK
- /api/v1/committees includes URL fields
- All existing endpoints still functional

✅ **Phase 2 Complete**
- Committee URLs visible in API responses
- Frontend integration working
- Production deployment stable

## 🎯 ESTIMATED COMPLETION TIME
- **Total**: 75 minutes
- **Critical Path**: Fix port configuration and redeploy
- **Risk**: Low - well-understood container deployment issue