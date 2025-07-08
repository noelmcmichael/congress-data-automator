# Congressional Data Automation Service - Project Rules

## 📋 Overview
This document defines the rules, standards, and best practices for the Congressional Data Automation Service project. These rules ensure code quality, maintainability, security, and operational excellence.

---

## 🔧 Development Rules

### Code Quality Standards

#### Python Backend (FastAPI)
- **Python Version**: 3.11+ required
- **Type Hints**: All functions must include type hints
- **Code Formatting**: Use Black for code formatting
- **Import Organization**: Use isort for import sorting
- **Docstrings**: All public functions and classes must have docstrings
- **Error Handling**: Always use proper exception handling with specific exception types
- **Logging**: Use structured logging with appropriate log levels

#### React Frontend (TypeScript)
- **TypeScript**: All components must be TypeScript with proper typing
- **Component Structure**: Use functional components with hooks
- **Material-UI**: Use Material-UI components for consistency
- **Code Organization**: Group related components in logical directories
- **State Management**: Use React hooks for state management
- **Error Boundaries**: Implement error boundaries for production stability

### API Design Rules

#### RESTful Principles
- **HTTP Methods**: Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- **Status Codes**: Return proper HTTP status codes
- **URL Structure**: Use noun-based URLs with consistent naming
- **Versioning**: All APIs must include version prefix (`/api/v1/`)
- **Response Format**: Consistent JSON response format
- **Error Messages**: Clear, actionable error messages

#### Data Endpoints
- **Pagination**: All list endpoints must support pagination
- **Filtering**: Support common filters (chamber, party, state, status)
- **Sorting**: Support sorting by relevant fields
- **Search**: Implement search functionality where appropriate
- **Rate Limiting**: Implement rate limiting to prevent abuse

### Database Rules

#### Schema Design
- **Normalization**: Follow 3NF principles
- **Primary Keys**: Use auto-incrementing integers for primary keys
- **Foreign Keys**: Always define foreign key relationships
- **Indexes**: Index frequently queried columns
- **Constraints**: Use database constraints for data integrity
- **Naming**: Use snake_case for table and column names

#### Data Integrity
- **Validation**: Validate data at both application and database levels
- **Transactions**: Use transactions for multi-table operations
- **Backups**: Automated daily backups with tested restore procedures
- **Migrations**: Use Alembic for all schema changes
- **Soft Deletes**: Use soft deletes for important data

---

## 🌐 Data Collection Rules

### Congress.gov API Usage

#### Rate Limiting
- **Daily Limit**: Maximum 5,000 requests per day
- **Request Frequency**: No more than 1 request per second
- **Retry Logic**: Exponential backoff for failed requests
- **Monitoring**: Track API usage and remaining quota
- **Graceful Degradation**: Handle rate limit errors gracefully

#### Data Freshness
- **Members**: Update monthly (1st of month)
- **Committees**: Update weekly (Mondays)
- **Hearings**: Update daily (6:00 AM EST)
- **Emergency Updates**: Manual updates for urgent changes
- **Validation**: Validate data integrity after each update

### Web Scraping Ethics

#### Respectful Scraping
- **robots.txt**: Always respect robots.txt files
- **Rate Limiting**: Minimum 1-second delay between requests
- **User Agent**: Use descriptive, contact-able user agent string
- **Error Handling**: Graceful degradation on scraping failures
- **Caching**: Cache scraped data to minimize requests

#### Data Quality
- **Validation**: Validate scraped data before storage
- **Confidence Scoring**: Implement confidence scoring for scraped URLs
- **Fallback Strategies**: Use multiple sources when possible
- **Quality Monitoring**: Track success rates and data quality
- **Manual Review**: Flag suspicious data for manual review

---

## 🔒 Security Rules

### Data Protection
- **Public Data Only**: Only collect publicly available congressional data
- **No PII**: Avoid collecting personal information beyond public records
- **Data Encryption**: Encrypt sensitive data in transit and at rest
- **Access Control**: Implement role-based access control
- **Audit Logging**: Log all data access and modifications

### API Security
- **Authentication**: Require authentication for admin endpoints
- **Input Validation**: Validate all inputs to prevent injection attacks
- **SQL Injection Prevention**: Use parameterized queries exclusively
- **XSS Prevention**: Sanitize all outputs to prevent XSS
- **CORS**: Configure CORS properly for frontend access

### Infrastructure Security
- **HTTPS**: Use HTTPS everywhere (TLS 1.2+)
- **Network Security**: Use VPC and firewall rules
- **Secrets Management**: Use Google Secret Manager for sensitive data
- **Regular Updates**: Keep all dependencies updated
- **Vulnerability Scanning**: Regular security scans

---

## 🏗️ Infrastructure Rules

### Google Cloud Platform

#### Service Configuration
- **Cloud Run**: Use Cloud Run for API deployment
- **Cloud SQL**: Use Cloud SQL for PostgreSQL database
- **Cloud Storage**: Use Cloud Storage for frontend hosting
- **Cloud Scheduler**: Use Cloud Scheduler for automated tasks
- **Cloud Monitoring**: Use Cloud Monitoring for system health

#### Resource Management
- **Least Privilege**: Use minimal required permissions
- **Cost Optimization**: Use appropriate instance sizes
- **Auto-scaling**: Configure auto-scaling for variable loads
- **Health Checks**: Implement comprehensive health checks
- **Monitoring**: Set up alerts for all critical services

### Deployment Strategy

#### CI/CD Pipeline
- **Automated Testing**: Run all tests on every commit
- **Code Review**: Require peer review for all changes
- **Deployment Gates**: Require passing tests before deployment
- **Rollback Strategy**: Maintain ability to rollback quickly
- **Environment Parity**: Keep dev/staging/prod environments similar

#### Deployment Process
- **Blue/Green Deployments**: Zero-downtime deployments when possible
- **Health Checks**: Verify health after each deployment
- **Monitoring**: Monitor key metrics during and after deployment
- **Logging**: Structured logging with correlation IDs
- **Communication**: Notify team of deployments and issues

---

## 📊 Performance Rules

### Response Time Targets
- **Simple Queries**: < 200ms response time
- **Complex Queries**: < 1000ms response time
- **Database Queries**: < 100ms for simple queries
- **Frontend Load**: < 3 seconds initial load time
- **API Availability**: 99.9% uptime target

### Optimization Requirements
- **Database Indexes**: Index all frequently queried columns
- **Query Optimization**: Optimize slow queries (> 1 second)
- **Caching**: Implement caching for frequently accessed data
- **Pagination**: Use cursor-based pagination for large datasets
- **Compression**: Use gzip compression for API responses

### Frontend Performance
- **Bundle Size**: Keep JavaScript bundle < 1MB
- **Image Optimization**: Optimize images for web delivery
- **Lazy Loading**: Implement lazy loading for components
- **Browser Caching**: Use appropriate cache headers
- **CDN**: Use CDN for static assets

---

## 📈 Monitoring and Alerting

### Key Metrics
- **API Response Time**: Average and 95th percentile
- **Error Rate**: 4xx and 5xx error rates
- **Database Performance**: Query execution times
- **Data Freshness**: Time since last successful update
- **Resource Utilization**: CPU, memory, disk usage

### Alerting Rules
- **Critical Alerts**: System down, database offline, API errors > 5%
- **Warning Alerts**: High response times, low API quota, failed updates
- **Info Alerts**: Successful deployments, scheduled task completion
- **Escalation**: Escalate unresolved critical alerts after 15 minutes
- **Alert Fatigue**: Regularly review and tune alerts

### Operational Excellence
- **Status Page**: Maintain public status page for service health
- **Incident Response**: Have documented incident response procedures
- **Post-Mortems**: Conduct post-mortems for all incidents
- **Regular Reviews**: Weekly operational reviews
- **Documentation**: Keep operational documentation current

---

## 🔄 Change Management

### Code Changes
- **Feature Branches**: Use feature branches for all development
- **Commit Messages**: Use conventional commit format
- **Code Review**: Require peer review for all changes
- **Testing**: Require passing tests before merge
- **Documentation**: Update documentation with changes

### Schema Changes
- **Backward Compatibility**: Maintain backward compatibility when possible
- **Migration Testing**: Test migrations on copy of production data
- **Rollback Migrations**: Create rollback migrations for all changes
- **Documentation**: Document all schema changes
- **Communication**: Notify team of breaking changes

### Release Process
- **Semantic Versioning**: Use semantic versioning for releases
- **Release Notes**: Document all changes in release notes
- **Deployment Windows**: Schedule deployments during low usage
- **Rollback Plan**: Have rollback plan for each release
- **Communication**: Proactive communication about releases

---

## 📚 Documentation Rules

### Code Documentation
- **README**: Keep README.md current and comprehensive
- **API Documentation**: Auto-generate API documentation
- **Architecture**: Document system architecture and design decisions
- **Deployment**: Document deployment procedures
- **Troubleshooting**: Document common issues and solutions

### Operational Documentation
- **Runbooks**: Create runbooks for operational tasks
- **Monitoring**: Document monitoring and alerting setup
- **Incident Response**: Document incident response procedures
- **Data Sources**: Document all data sources and their characteristics
- **Business Logic**: Document complex business logic

---

## 🎯 Quality Assurance

### Testing Requirements
- **Unit Tests**: Minimum 80% code coverage for backend
- **Integration Tests**: Test API endpoints and database interactions
- **Frontend Tests**: Test React components and user interactions
- **End-to-End Tests**: Test critical user workflows
- **Performance Tests**: Test system performance under load

### Quality Gates
- **Code Review**: All code must be reviewed by another developer
- **Automated Tests**: All tests must pass before deployment
- **Security Scan**: Security vulnerabilities must be addressed
- **Performance Check**: Performance regression tests must pass
- **Documentation**: Changes must include documentation updates

---

## 🚀 Project-Specific Rules

### Congressional Data Handling
- **Data Accuracy**: Verify data accuracy against official sources
- **Update Schedules**: Respect official update schedules
- **Data Attribution**: Credit data sources appropriately
- **Error Handling**: Handle data inconsistencies gracefully
- **Validation**: Implement comprehensive data validation

### User Experience
- **Accessibility**: Follow WCAG 2.1 AA guidelines
- **Mobile Responsive**: Ensure mobile-friendly design
- **Performance**: Optimize for fast loading times
- **Intuitive Navigation**: Design for easy navigation
- **Error Messages**: Provide clear, actionable error messages

### Compliance
- **Public Data**: Only use publicly available data
- **Attribution**: Credit all data sources
- **Privacy**: Respect privacy of congressional staff
- **Transparency**: Be transparent about data collection methods
- **Updates**: Keep data current and accurate

---

## 📞 Support and Maintenance

### Support Guidelines
- **Response Time**: Respond to issues within 24 hours
- **Issue Tracking**: Use GitHub issues for bug tracking
- **Documentation**: Document solutions to common issues
- **User Feedback**: Regularly collect and act on user feedback
- **Continuous Improvement**: Regular reviews and improvements

### Maintenance Schedule
- **Regular Updates**: Monthly dependency updates
- **Security Patches**: Apply security patches within 7 days
- **Performance Reviews**: Quarterly performance reviews
- **Code Reviews**: Annual code quality reviews
- **Documentation Updates**: Keep documentation current

---

## 📝 Rule Enforcement

### Enforcement Mechanisms
- **Code Reviews**: Enforce rules through code review process
- **Automated Testing**: Use automated tests to enforce quality
- **CI/CD Pipeline**: Enforce rules through deployment pipeline
- **Monitoring**: Monitor compliance with operational rules
- **Regular Audits**: Conduct regular compliance audits

### Violations
- **Minor Violations**: Address through code review feedback
- **Major Violations**: Require immediate remediation
- **Repeated Violations**: Escalate to project leadership
- **Security Violations**: Immediate remediation required
- **Documentation**: Document all violations and remediation

---

## 🔄 Rule Updates

### Review Process
- **Monthly Reviews**: Review rules monthly for relevance
- **Quarterly Updates**: Update rules quarterly based on lessons learned
- **Stakeholder Input**: Collect input from all team members
- **Version Control**: Track rule changes in version control
- **Communication**: Communicate rule changes to all team members

### Change Process
- **Proposal**: Propose rule changes through pull requests
- **Review**: Review proposed changes with team
- **Approval**: Require approval from project lead
- **Implementation**: Implement changes with appropriate notice
- **Training**: Provide training on new rules

---

**Last Updated**: January 8, 2025  
**Version**: 1.0  
**Next Review**: February 8, 2025

🤖 Generated with [Memex](https://memex.tech)  
Co-Authored-By: Memex <noreply@memex.tech>