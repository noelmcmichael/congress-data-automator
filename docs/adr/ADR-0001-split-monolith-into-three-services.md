# ADR-0001: Split Monolith into Three Services

**Date**: January 8, 2025  
**Status**: Proposed  
**Context**: Enterprise-grade refactoring of Congressional Data Automation Service  
**Deciders**: Technical Team  
**Evidence**: [sources.md](../../evidence/sources.md)

## Context and Problem Statement

The Congressional Data Automation Service currently operates as a monolithic FastAPI application that handles all concerns: data ingestion, validation, storage, and API serving. Analysis of the current system (documented in `evidence/sources.md`) reveals several architectural limitations that prevent enterprise-grade reliability and scalability:

### Current Architecture Problems

1. **Mixed Responsibilities**: Single service handles both data writes (ingestion) and reads (API)
2. **Single Point of Failure**: Monolithic design creates system-wide risks
3. **No Data Quality Gates**: Direct database writes without validation pipelines
4. **Limited Observability**: Basic logging without metrics or distributed tracing
5. **Deployment Coupling**: Changes to ingestion logic require API redeployment
6. **Resource Contention**: Heavy ingestion workloads impact API response times

### Business Requirements

- **Reliability**: 99.9% uptime for public API
- **Data Quality**: Automated validation and quality monitoring
- **Scalability**: Handle increasing data volumes and API requests
- **Maintainability**: Clear separation of concerns for development teams
- **Observability**: Comprehensive monitoring and alerting

## Decision Drivers

### Technical Drivers
- **Data Change Frequency**: High-frequency changes (hearings multiple times daily) require dedicated ingestion service
- **API Performance**: Public API requires consistent sub-500ms response times
- **Data Pipeline Complexity**: Multiple sources (Congress.gov API, web scrapers) need orchestration
- **Schema Evolution**: Need for versioned contracts and migration management

### Operational Drivers
- **Team Scalability**: Different teams can own different services
- **Deployment Independence**: Services can be deployed independently
- **Resource Optimization**: CPU-intensive ingestion separate from memory-intensive API
- **Fault Isolation**: Ingestion failures don't impact API availability

## Considered Options

### Option 1: Keep Current Monolith
- **Pros**: No migration effort, familiar architecture
- **Cons**: Scalability limitations, mixed responsibilities, single point of failure
- **Verdict**: Does not meet enterprise-grade requirements

### Option 2: Split into Two Services (Ingestion + API)
- **Pros**: Separates concerns, easier than three-service split
- **Cons**: Still mixes validation with ingestion, limited pipeline orchestration
- **Verdict**: Insufficient for data quality requirements

### Option 3: Split into Three Services (Chosen)
- **Pros**: Clear separation of concerns, dedicated data quality, scalable architecture
- **Cons**: Increased complexity, requires service coordination
- **Verdict**: Best balance of reliability, scalability, and maintainability

### Option 4: Microservices Architecture (5+ Services)
- **Pros**: Ultimate flexibility and scalability
- **Cons**: Over-engineering for current requirements, excessive complexity
- **Verdict**: Premature optimization for current scale

## Decision

We will **split the monolith into three specialized services** with clear boundaries and responsibilities:

### Service 1: `/services/ingestion`
- **Responsibility**: Data collection and processing
- **Scope**: 
  - Congress.gov API client
  - Web scraping framework
  - Raw data transformation
  - Database writes (staging tables)
- **Technology**: Python + FastAPI + Dagster
- **Deployment**: Cloud Run with background processing
- **Scaling**: Auto-scale based on queue depth

### Service 2: `/services/validation`
- **Responsibility**: Data quality and validation pipelines
- **Scope**:
  - Data quality checks (Great Expectations)
  - Schema validation and migration
  - Data lineage tracking
  - Promotion to production tables
- **Technology**: Python + Great Expectations + Dagster
- **Deployment**: Cloud Run with scheduled jobs
- **Scaling**: Resource-based scaling for batch processing

### Service 3: `/services/api`
- **Responsibility**: Read-only public API
- **Scope**:
  - Public API endpoints
  - Query optimization and caching
  - API versioning and contracts
  - Request/response transformation
- **Technology**: Python + FastAPI + Redis
- **Deployment**: Cloud Run with minimum instances
- **Scaling**: Auto-scale based on request volume

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ingestion     │    │   Validation    │    │      API        │
│   Service       │    │   Service       │    │    Service      │
│                 │    │                 │    │                 │
│ • Congress API  │    │ • Great Expect. │    │ • Public API    │
│ • Web Scrapers  │    │ • Data Quality  │    │ • Caching       │
│ • ETL Pipeline  │    │ • Schema Valid. │    │ • Rate Limiting │
│ • Raw Data      │    │ • Lineage       │    │ • Documentation │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Staging        │    │  Validation     │    │   Production    │
│  Tables         │    │  Results        │    │   Views         │
│                 │    │                 │    │                 │
│ • Raw ingestion │    │ • Quality logs  │    │ • core_members  │
│ • Unvalidated   │    │ • Test results  │    │ • core_hearings │
│ • Temporary     │    │ • Lineage data  │    │ • core_committees│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Consequences

### Positive Consequences

1. **Improved Reliability**
   - API service can remain available during ingestion failures
   - Independent scaling based on service-specific needs
   - Circuit breakers prevent cascading failures

2. **Enhanced Data Quality**
   - Dedicated validation service with Great Expectations
   - Automated data quality monitoring and alerting
   - Clear data lineage and audit trails

3. **Better Observability**
   - Service-specific metrics and monitoring
   - Distributed tracing across the pipeline
   - Business metrics for data coverage and quality

4. **Team Scalability**
   - Clear ownership boundaries
   - Independent deployment pipelines
   - Specialized skill requirements per service

5. **Performance Optimization**
   - API service optimized for response time
   - Ingestion service optimized for throughput
   - Validation service optimized for data quality

### Negative Consequences

1. **Increased Complexity**
   - Service coordination and communication
   - Distributed system debugging challenges
   - Network latency between services

2. **Operational Overhead**
   - Multiple deployment pipelines
   - Service discovery and health checks
   - Inter-service monitoring and alerting

3. **Data Consistency**
   - Eventually consistent data across services
   - Need for saga patterns or event sourcing
   - Potential for data synchronization issues

4. **Development Complexity**
   - Local development environment setup
   - Integration testing across services
   - Version compatibility management

## Implementation Plan

### Phase 1: Foundation (Weeks 1-2)
- Create service directory structure
- Implement `/services/ingestion` with existing collectors
- Add typing and structured logging per rules.md
- Implement basic health checks and metrics

### Phase 2: Validation Pipeline (Weeks 3-4)
- Implement `/services/validation` with Great Expectations
- Create Dagster pipeline for data quality
- Add schema versioning (v20250708)
- Implement data lineage tracking

### Phase 3: API Service (Weeks 5-6)
- Create read-only `/services/api` service
- Implement caching and query optimization
- Add API versioning and documentation
- Implement rate limiting and monitoring

### Phase 4: Infrastructure (Weeks 7-8)
- Terraform infrastructure as code
- CI/CD pipelines for each service
- Monitoring and alerting setup
- Load testing and performance optimization

## Success Metrics

### Technical Metrics
- **API Latency**: p95 < 500ms for 24 hours in staging
- **Data Quality**: ≥ 98% coverage in Dagster job `promote_members`
- **Service Availability**: ≥ 99.9% uptime per service
- **Test Coverage**: ≥ 80% across all services

### Business Metrics
- **Data Freshness**: Hearings updated within 6 hours
- **API Reliability**: Zero API downtime during ingestion
- **Development Velocity**: Independent service deployments
- **Incident Response**: Service-specific incident isolation

## Compliance and Governance

### Schema Versioning
- **First Version**: v20250708 (canonical baseline)
- **Migration Strategy**: Alembic with rollback capabilities
- **Breaking Changes**: New contract version + migration script
- **Backward Compatibility**: Maintain previous version for 6 months

### Security Considerations
- **API Authentication**: Service-to-service authentication
- **Data Access**: Role-based access control
- **Secrets Management**: Google Secret Manager
- **Network Security**: VPC and firewall rules

### Monitoring and Alerting
- **Prometheus Metrics**: Request latency, error rates, queue depth
- **Grafana Dashboards**: Service health and business metrics
- **PagerDuty Alerting**: Critical service failures
- **Log Aggregation**: Centralized logging with correlation IDs

## Links and References

- [Evidence Analysis](../../evidence/sources.md)
- [Current Architecture](../../README.md)
- [Rules and Guidelines](../../rules.md)
- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Dagster Documentation](https://docs.dagster.io/)

---

**Next Steps**: Proceed with Task-C1 (Code) to scaffold `/services/ingestion` with existing collectors.