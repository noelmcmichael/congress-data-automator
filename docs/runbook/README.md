# Operations Runbook

## Overview

This runbook contains operational procedures for the Congressional Data Automation Service production environment.

## Quick Reference

### System Status
- **Frontend**: https://storage.googleapis.com/congressional-data-frontend/index.html
- **API**: https://congressional-data-api-v2-1066017671167.us-central1.run.app
- **Health Check**: `curl https://congressional-data-api-v2-1066017671167.us-central1.run.app/health`
- **Monitoring**: `curl https://congressional-data-api-v2-1066017671167.us-central1.run.app/monitoring`

### Emergency Contacts
- **Primary**: Development Team
- **Escalation**: Project Owner
- **GCP Support**: Google Cloud Support (if enabled)

## Common Procedures

### System Health Check
```bash
# API health
curl https://congressional-data-api-v2-1066017671167.us-central1.run.app/health

# Database connectivity
gcloud sql instances describe congress-db --project=your-project

# Cloud Run status
gcloud run services describe congressional-data-api --region=us-central1
```

### Restart Services
```bash
# Restart API service
gcloud run services update congressional-data-api \
  --region=us-central1 \
  --project=your-project

# Restart Cloud SQL (if needed)
gcloud sql instances restart congress-db --project=your-project
```

### View Logs
```bash
# API logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=congressional-data-api" \
  --limit=100 --format=json

# Database logs
gcloud logging read "resource.type=gce_instance AND protoPayload.serviceName=cloudsql.googleapis.com" \
  --limit=50
```

## Detailed Procedures

### [Deployment](deployment.md)
- Production deployment steps
- Rollback procedures
- Environment management

### [Monitoring](monitoring.md)
- Alert configuration
- Dashboard access
- Performance metrics

### [Troubleshooting](troubleshooting.md)
- Common issues and solutions
- Debug procedures
- Performance optimization

### [Maintenance](maintenance.md)
- Regular maintenance tasks
- Database optimization
- System updates

### [Security](security.md)
- Security incident response
- Access management
- Compliance procedures

## Incident Response

### Severity Levels
- **P1**: Complete system outage
- **P2**: Partial service degradation
- **P3**: Non-critical issues
- **P4**: Enhancement requests

### Response Procedures
1. **Assess impact and severity**
2. **Check system health endpoints**
3. **Review recent deployments**
4. **Check GCP console for alerts**
5. **Escalate if needed**

### Recovery Procedures
1. **Immediate**: Restart affected services
2. **Short-term**: Rollback recent changes
3. **Long-term**: Root cause analysis and fixes

---

For specific operational procedures, see the individual documents in this directory.