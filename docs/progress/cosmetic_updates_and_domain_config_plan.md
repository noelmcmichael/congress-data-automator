# Cosmetic Updates & Domain Configuration Plan

## Phase 1: ICO Image Integration

### Objective
Replace default React favicon with custom polequity-ico.png for brand consistency

### Acceptance Criteria
- [ ] Browser tab displays custom polequity-ico.png instead of React default
- [ ] ICO appears correctly across all modern browsers
- [ ] Frontend rebuild deploys successfully to production
- [ ] No broken icon references or 404s

### Implementation Steps
1. Copy polequity-ico.png to frontend/public/ directory
2. Update frontend/public/index.html favicon reference
3. Test locally with `npm start`
4. Rebuild frontend for production deployment
5. Verify icon loads correctly in production

### Risks
- **Low Risk**: Simple file replacement operation
- Icon size/format compatibility across browsers
- Production deployment may cache old favicon

### Test Hooks
- Browser dev tools confirm correct icon path
- Manual verification across Chrome, Firefox, Safari

---

## Phase 2: Domain Configuration Analysis

### Objective
Analyze `politicalequity.io` domain routing plan compatibility with Congressional Data Automator architecture

### Acceptance Criteria
- [ ] Complete compatibility assessment with current GCP deployment
- [ ] Identify any required architecture modifications
- [ ] Document implementation approach for DNS configuration
- [ ] Confirm frontend/backend routing patterns

### Current Architecture Assessment

#### **Frontend** 
- **Technology**: React (Create React App)
- **Current Location**: Google Cloud Storage bucket
- **URL**: https://storage.googleapis.com/congressional-data-frontend/index.html
- **Routing**: Client-side React Router

#### **Backend**
- **Technology**: FastAPI 
- **Current Location**: Google Cloud Run
- **URL**: https://congressional-data-api-v2-1066017671167.us-central1.run.app
- **Database**: PostgreSQL on Google Cloud SQL

#### **DNS Requirements Analysis**
- `https://politicalequity.io` → React frontend 
- `https://politicalequity.io/api/*` → FastAPI backend
- SSL certificate provisioning
- CORS configuration updates

### Implementation Approach Options

#### **Option A: Google Cloud Load Balancer (Recommended)**
- **Frontend**: Serve React app from Cloud Storage bucket
- **Backend**: Route `/api/*` to Cloud Run service
- **SSL**: Google-managed SSL certificates
- **Benefits**: Native GCP integration, automatic SSL renewal

#### **Option B: Cloudflare Load Balancing**
- **DNS**: Cloudflare as authoritative nameserver
- **Load Balancing**: Cloudflare's DNS-based load balancer
- **SSL**: Cloudflare SSL certificates
- **Benefits**: Better global performance, DDoS protection

#### **Option C: Hybrid Approach**
- **DNS**: Cloudflare for DNS management
- **Load Balancer**: Google Cloud Load Balancer
- **Benefits**: Best of both platforms

### Risks
- **Medium Risk**: DNS propagation delays (24-48 hours)
- **Medium Risk**: SSL certificate provisioning time
- **Low Risk**: CORS configuration changes required
- **Low Risk**: Frontend build process modifications for custom domain

### Implementation Dependencies
- Domain registrar access for `politicalequity.io`
- Google Cloud project permissions
- Production deployment access

### Test Hooks
- DNS propagation verification: `dig politicalequity.io`
- SSL certificate validation: browser security indicators
- Frontend routing: verify React Router works with custom domain
- Backend API: test all endpoints via `politicalequity.io/api/*`
- CORS validation: browser dev tools network tab

---

## Phase 3: Production Implementation

### Objective
Execute domain configuration with zero downtime

### Acceptance Criteria  
- [ ] `politicalequity.io` serves production frontend
- [ ] `politicalequity.io/api/*` routes to production backend
- [ ] SSL certificates active and valid
- [ ] No broken functionality or API calls
- [ ] Original URLs remain functional during transition

### Implementation Strategy
1. **Pre-flight**: Test configuration in staging environment
2. **DNS Setup**: Configure load balancer and SSL certificates  
3. **Gradual Rollout**: DNS TTL management for quick rollback
4. **Validation**: Comprehensive testing across all functionality
5. **Monitoring**: Track performance and error rates

### Rollback Plan
- Revert DNS A records to original configuration
- Maintain original Google Cloud URLs as backup
- 5-minute DNS TTL for rapid rollback capability

---

## Success Metrics
- **Performance**: Load time ≤ current baseline
- **Availability**: 99.9% uptime during transition
- **Security**: A+ SSL rating
- **Functionality**: All API endpoints working correctly
- **User Experience**: Seamless brand experience with custom domain

---

## Timeline Estimate
- **Phase 1 (ICO)**: 30 minutes
- **Phase 2 (Analysis)**: 1 hour  
- **Phase 3 (Implementation)**: 2-4 hours
- **Total**: 3.5-5.5 hours