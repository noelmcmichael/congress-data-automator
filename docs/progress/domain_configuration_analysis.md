# Domain Configuration Analysis: politicalequity.io

## Current Architecture Assessment

### **Deployment Infrastructure**
- **Platform**: Google Cloud Platform
- **Frontend**: React app hosted on Google Cloud Storage 
  - Current URL: `https://storage.googleapis.com/congressional-data-frontend/index.html`
  - Static site with client-side routing
- **Backend**: FastAPI on Google Cloud Run
  - Current URL: `https://congressional-data-api-v2-1066017671167.us-central1.run.app`
  - API prefix: `/api/v1/*`
- **Database**: PostgreSQL on Google Cloud SQL

### **Current API Structure**
```
Backend Routes (all prefixed with /api/v1):
├── /                          # Root status
├── /health                    # Health check  
├── /status                    # API status with rate limits
├── /cache/status             # Cache statistics
├── /data-updates/*           # Data management endpoints
├── /data-retrieval/*         # Member/committee queries
├── /relationships/*          # Member-committee relationships
├── /congress/*               # Congressional session data
├── /advanced-features/*      # Enhanced functionality
└── /monitoring/*             # Performance dashboard
```

### **CORS Configuration**
- **Current**: `allow_origins=["*"]` (permissive for development)
- **Required for Domain**: Add `politicalequity.io` to allowed origins
- **Security**: Should restrict to specific domains in production

---

## Domain Configuration Plan

### **Target Architecture**
```
https://politicalequity.io/           → React Frontend (Google Cloud Storage)
https://politicalequity.io/api/v1/*   → FastAPI Backend (Google Cloud Run)
```

### **Implementation Approach: Google Cloud Load Balancer**

#### **Why Google Cloud Load Balancer?**
1. **Native Integration**: Seamless with existing GCP infrastructure
2. **SSL Management**: Automatic Google-managed SSL certificates
3. **Performance**: Global edge locations
4. **Cost Effective**: No additional services required

#### **Load Balancer Configuration**

```yaml
URL Map:
  Default Service: frontend-bucket-backend-service
  Host Rules:
    - hosts: ['politicalequity.io']
      path_matcher: 'path-matcher-1'
  
Path Matchers:
  path-matcher-1:
    default_service: frontend-bucket-backend-service
    path_rules:
      - paths: ['/api/*']
        service: congressional-data-api-backend-service
      - paths: ['/*']  
        service: frontend-bucket-backend-service
```

#### **Backend Services Configuration**

```yaml
Frontend Backend Service:
  type: Cloud Storage Bucket
  bucket: congressional-data-frontend
  enable_cdn: true
  compression: enabled

API Backend Service:  
  type: Cloud Run
  service: congressional-data-api-v2
  protocol: HTTPS
  timeout: 30s
```

---

## Implementation Steps

### **Phase 1: Load Balancer Setup**

#### **1.1 Create Static IP Address**
```bash
gcloud compute addresses create politicalequity-ip \
    --global \
    --ip-version IPV4
```

#### **1.2 SSL Certificate (Google-Managed)**
```bash
gcloud compute ssl-certificates create politicalequity-ssl-cert \
    --domains politicalequity.io \
    --global
```

#### **1.3 Backend Services**
```bash
# Frontend (Cloud Storage)
gcloud compute backend-services create frontend-bucket-backend-service \
    --global

# API (Cloud Run)  
gcloud compute backend-services create congressional-data-api-backend-service \
    --global \
    --protocol HTTPS
```

#### **1.4 URL Map**
```bash
gcloud compute url-maps create politicalequity-url-map \
    --default-service frontend-bucket-backend-service
    
gcloud compute url-maps add-path-matcher politicalequity-url-map \
    --path-matcher-name path-matcher-1 \
    --default-service frontend-bucket-backend-service
    
gcloud compute url-maps add-host-rule politicalequity-url-map \
    --hosts politicalequity.io \
    --path-matcher path-matcher-1
```

#### **1.5 Load Balancer**
```bash
gcloud compute target-https-proxies create politicalequity-https-proxy \
    --ssl-certificates politicalequity-ssl-cert \
    --url-map politicalequity-url-map

gcloud compute forwarding-rules create politicalequity-https-rule \
    --global \
    --target-https-proxy politicalequity-https-proxy \
    --ports 443 \
    --address politicalequity-ip
```

### **Phase 2: DNS Configuration**

#### **2.1 Get Load Balancer IP**
```bash
gcloud compute addresses describe politicalequity-ip --global --format="value(address)"
```

#### **2.2 DNS Records (at Domain Registrar)**
```dns
A    politicalequity.io    [LOAD_BALANCER_IP]
AAAA politicalequity.io    [IPv6_if_available]
```

### **Phase 3: Application Updates**

#### **3.1 CORS Configuration Update**
```python
# backend/app/core/config.py
allowed_origins: List[str] = Field(
    default=["https://politicalequity.io"], 
    env="ALLOWED_ORIGINS"
)
```

#### **3.2 Environment Variables**
```bash
# Add to backend production environment
ALLOWED_ORIGINS=["https://politicalequity.io","https://storage.googleapis.com"]
```

#### **3.3 Frontend Build Configuration**
```json
// frontend/package.json - ensure proper build for custom domain
{
  "homepage": "https://politicalequity.io"
}
```

---

## Technical Considerations

### **SSL Certificate Provisioning**
- **Timeline**: Google-managed certificates take 15-60 minutes to provision
- **Requirements**: Domain must resolve to load balancer IP first
- **Validation**: Google validates domain ownership automatically

### **DNS Propagation**
- **Timeline**: 15 minutes to 48 hours globally
- **TTL Strategy**: Set low TTL (300s) before changes for quick rollback
- **Testing**: Use multiple DNS resolvers to verify propagation

### **CORS Implications**
- **Current**: Wildcard `*` allows all origins
- **Production**: Restrict to specific domains for security
- **Transition**: Keep current origins during testing phase

### **React Router Compatibility**
- **Client-Side Routing**: React Router handles `/` paths
- **Server Configuration**: Ensure 404s redirect to `index.html`
- **API Separation**: `/api/*` paths bypass React Router

---

## Risk Assessment

### **Low Risk**
- ✅ DNS record updates (reversible)
- ✅ SSL certificate provisioning (automatic)
- ✅ Load balancer configuration (GCP native)

### **Medium Risk**
- ⚠️ CORS configuration changes (test thoroughly)
- ⚠️ DNS propagation delays (plan timing)
- ⚠️ SSL certificate validation time (first-time setup)

### **Mitigation Strategies**
1. **Staging Environment**: Test full configuration before production
2. **Gradual Rollout**: Phase DNS changes with monitoring
3. **Rollback Plan**: Keep original URLs functional during transition
4. **Monitoring**: Track API response times and error rates

---

## Performance Implications

### **Expected Improvements**
- **CDN**: Global edge caching for frontend assets
- **SSL Termination**: At load balancer level (faster)
- **Connection Pooling**: Optimized backend connections

### **Monitoring Setup**
- **Uptime**: Load balancer health checks
- **Performance**: API response times via Google Cloud Monitoring
- **SSL Health**: Certificate expiration monitoring
- **Error Rates**: 4xx/5xx response tracking

---

## Cost Implications

### **Google Cloud Load Balancer Pricing**
- **Load Balancer**: ~$18/month base cost
- **SSL Certificate**: Free (Google-managed)
- **Ingress Data**: $0.085/GB (first 1GB free)
- **Egress Data**: Standard GCP rates

### **Cost-Benefit Analysis**
- **Additional Cost**: ~$20-30/month
- **Benefits**: Professional domain, better performance, brand consistency
- **ROI**: Improved user experience and credibility

---

## Implementation Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Load Balancer Setup | 1 hour | GCP access, SSL cert provision time |
| DNS Configuration | 30 minutes | Domain registrar access |
| Application Updates | 1 hour | CORS testing, frontend rebuild |
| Testing & Validation | 1-2 hours | DNS propagation wait time |
| **Total** | **3.5-4.5 hours** | **Plus propagation delays** |

---

## Success Criteria

### **Functional Requirements**
- [ ] `https://politicalequity.io` loads React frontend
- [ ] `https://politicalequity.io/api/v1/status` returns API status
- [ ] All existing API endpoints work via new domain
- [ ] React Router navigation functions correctly
- [ ] SSL certificate shows as valid and secure

### **Performance Requirements**
- [ ] Page load time ≤ current baseline
- [ ] API response time ≤ current baseline  
- [ ] SSL handshake time < 500ms
- [ ] Global CDN cache hit rate > 80%

### **Security Requirements**
- [ ] SSL A+ rating on SSL Labs
- [ ] CORS restricted to specific domains
- [ ] No mixed content warnings
- [ ] Security headers properly configured

---

## Rollback Procedure

### **Emergency Rollback (< 5 minutes)**
1. Revert DNS A record to original IP
2. Wait for DNS propagation
3. Original URLs remain functional

### **Planned Rollback**
1. Update CORS to include original domains
2. Gradually shift DNS traffic back
3. Decomission load balancer after validation

### **Rollback Testing**
- Test rollback procedure in staging first
- Document exact steps and timings
- Prepare communication plan for users

---

## Next Steps

1. **Immediate**: Complete ICO image updates and test locally
2. **Phase 1**: Set up Google Cloud Load Balancer in staging
3. **Phase 2**: Configure DNS and test end-to-end
4. **Phase 3**: Production deployment with monitoring
5. **Phase 4**: Performance optimization and monitoring setup