# Project Rules and Best Practices

## Development Guidelines

### Code Quality
- **Language Standards**: Python 3.11+ with type hints, ES6+ JavaScript
- **Code Style**: Black for Python, Prettier for JavaScript
- **Linting**: pylint/flake8 for Python, ESLint for JavaScript
- **Testing**: pytest for Python, Jest for JavaScript
- **Minimum Test Coverage**: 80%

### API Design
- **RESTful Principles**: Use proper HTTP methods and status codes
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Authentication**: Use JWT tokens for API authentication
- **Versioning**: API versioning with `/v1/` prefix
- **Documentation**: OpenAPI/Swagger documentation

### Database Design
- **Normalization**: Follow 3NF principles
- **Indexing**: Index frequently queried columns
- **Migrations**: Use Alembic for database migrations
- **Backup**: Daily automated backups
- **Security**: Encrypt sensitive data at rest

### Data Collection Rules

### Congress.gov API
- **Rate Limiting**: Maximum 5000 requests per day
- **Request Frequency**: No more than 1 request per second
- **Retry Logic**: Exponential backoff for failed requests
- **Data Freshness**: 
  - Members: Update monthly
  - Committees: Update weekly
  - Hearings: Update daily
  - Active legislation: Update hourly during session

### Web Scraping Ethics
- **robots.txt**: Always respect robots.txt files
- **Rate Limiting**: Minimum 1-second delay between requests
- **User Agent**: Use descriptive, contact-able user agent string
- **Error Handling**: Graceful degradation on scraping failures
- **Caching**: Cache scraped data to minimize requests

### Infrastructure Rules

### GCP Best Practices
- **Least Privilege**: Use minimal required permissions
- **Network Security**: Use VPC and firewall rules
- **Secrets Management**: Use Google Secret Manager
- **Cost Optimization**: Use appropriate instance sizes
- **Monitoring**: Set up alerts for all services

### CI/CD Pipeline
- **Automated Testing**: Run all tests on every commit
- **Security Scanning**: Scan for vulnerabilities
- **Deployment Gates**: Require code review for production
- **Rollback Strategy**: Maintain ability to rollback quickly
- **Environment Parity**: Keep dev/staging/prod environments similar

### Deployment Strategy
- **Blue/Green Deployments**: Zero-downtime deployments
- **Health Checks**: Implement comprehensive health checks
- **Monitoring**: Real-time monitoring and alerting
- **Logging**: Structured logging with correlation IDs
- **Backup Strategy**: Regular backups with tested restore procedures

## Security Rules

### Data Protection
- **PII Handling**: Minimize collection of personal information
- **Data Encryption**: Encrypt data in transit and at rest
- **Access Control**: Role-based access control
- **Audit Logging**: Log all data access and modifications
- **Retention Policy**: Define data retention periods

### API Security
- **Authentication**: Require authentication for all endpoints
- **Authorization**: Implement proper authorization checks
- **Input Validation**: Validate all inputs
- **SQL Injection Prevention**: Use parameterized queries
- **XSS Prevention**: Sanitize all outputs

### Infrastructure Security
- **Network Security**: Use private networks where possible
- **SSL/TLS**: Use HTTPS everywhere
- **Firewall Rules**: Restrict network access
- **Vulnerability Scanning**: Regular security scans
- **Incident Response**: Have incident response plan

## Performance Rules

### Database Performance
- **Query Optimization**: Optimize slow queries
- **Connection Pooling**: Use connection pooling
- **Caching**: Implement Redis caching layer
- **Read Replicas**: Use read replicas for read-heavy workloads
- **Partitioning**: Partition large tables

### API Performance
- **Response Times**: Target < 200ms for simple queries
- **Pagination**: Implement cursor-based pagination
- **Compression**: Use gzip compression
- **CDN**: Use CDN for static assets
- **Caching**: Implement HTTP caching headers

### Frontend Performance
- **Bundle Size**: Keep bundle size < 1MB
- **Lazy Loading**: Implement lazy loading for components
- **Image Optimization**: Optimize images for web
- **Caching**: Use browser caching strategies
- **Performance Monitoring**: Monitor Core Web Vitals

## Monitoring and Alerting

### Key Metrics
- **API Response Time**: Average and 95th percentile
- **Error Rate**: 4xx and 5xx error rates
- **Database Performance**: Query execution times
- **Data Freshness**: Time since last successful update
- **Resource Utilization**: CPU, memory, disk usage

### Alerting Rules
- **Critical Alerts**: Page immediately for system-down scenarios
- **Warning Alerts**: Email for degraded performance
- **Info Alerts**: Slack notifications for deployments
- **Escalation**: Escalate unresolved critical alerts
- **Alert Fatigue**: Regularly review and tune alerts

## Compliance and Ethics

### Data Usage
- **Public Data**: Only collect publicly available data
- **Attribution**: Credit data sources appropriately
- **Update Frequency**: Respect source update schedules
- **Data Quality**: Implement data validation and cleaning
- **Error Handling**: Handle data inconsistencies gracefully

### Service Availability
- **SLA Target**: 99.9% uptime
- **Maintenance Windows**: Schedule during low usage
- **Graceful Degradation**: Partial functionality during outages
- **Status Page**: Maintain public status page
- **Communication**: Proactive communication about issues

## Change Management

### Code Changes
- **Feature Branches**: Use feature branches for development
- **Code Review**: Require peer review for all changes
- **Testing**: Require passing tests before merge
- **Documentation**: Update documentation with changes
- **Rollback Plan**: Have rollback plan for each deployment

### Schema Changes
- **Backward Compatibility**: Maintain backward compatibility
- **Migration Testing**: Test migrations on copy of production data
- **Rollback Migrations**: Create rollback migrations
- **Documentation**: Document all schema changes
- **Communication**: Notify team of breaking changes

---

Last Updated: 2025-01-04
Version: 1.0

🤖 Generated with [Memex](https://memex.tech)