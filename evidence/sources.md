# Congressional Data Sources & Ingress Points Analysis

**Date**: January 8, 2025  
**Scope**: Current ingress points, rate limits, authentication, and data change patterns  
**Purpose**: Task-R1 evidence gathering for enterprise-grade refactoring

## 1. Current Ingress Points

### 1.1 Primary API Sources

#### Congress.gov API
- **Base URL**: `https://api.congress.gov/v3`
- **Authentication**: API Key (X-API-Key header)
- **Rate Limit**: 5,000 requests per day
- **Request Delay**: 1.0 seconds between requests
- **Client**: `backend/app/services/congress_api.py`
- **Endpoints Used**:
  - `/member` - Congressional members (paginated)
  - `/member/{bioguide_id}` - Member details
  - `/member/{bioguide_id}/committee-assignment` - Committee assignments
  - `/committee` - Congressional committees
  - `/committee/{code}` - Committee details
  - `/committee/{code}/member` - Committee members
  - `/hearing` - Congressional hearings
  - `/hearing/{id}` - Hearing details
  - `/bill` - Bills and resolutions (search)

#### Web Scraping Sources
- **House.gov**: Committee pages, hearing details, video streams
- **Senate.gov**: Committee pages, hearing details, video streams
- **Individual Committee Websites**: Additional hearing information
- **Rate Limit**: 1.0 seconds between requests
- **Timeout**: 30 seconds
- **User Agent**: "Congressional Data Automator (https://github.com/noelmcmichael/congress-data-automator)"
- **Scrapers**: `backend/scrapers/`
  - `base_scraper.py` - Common functionality
  - `house_scraper.py` - House-specific scraping
  - `senate_scraper.py` - Senate-specific scraping

### 1.2 Data Update Endpoints (Current Ingestion Triggers)

#### Manual Update Endpoints
- **POST** `/api/v1/update/members` - Member data collection
- **POST** `/api/v1/update/committees` - Committee data collection
- **POST** `/api/v1/update/hearings` - Hearing data collection
- **POST** `/api/v1/update/all` - Full data refresh

#### Scheduled Updates (Cloud Scheduler)
- **Members**: Monthly on 1st at 8:00 AM EST (`0 13 1 * *`)
- **Committees**: Weekly on Mondays at 7:00 AM EST (`0 12 * * 1`)
- **Hearings**: Daily at 6:00 AM EST (`0 11 * * *`)

## 2. Rate Limits & Authentication

### 2.1 Congress.gov API
- **Daily Limit**: 5,000 requests
- **Per-Request Delay**: 1.0 seconds
- **Authentication**: API Key required
- **Reset Time**: Daily at midnight
- **Current Usage**: Typically 100-500 requests per day
- **Monitoring**: Real-time tracking via `CongressApiClient.get_rate_limit_status()`

### 2.2 Web Scraping
- **Rate Limit**: 1.0 seconds between requests
- **Timeout**: 30 seconds per request
- **Authentication**: None (public websites)
- **Retry Logic**: Built into base scraper
- **User Agent**: Identified as Congressional Data Automator

### 2.3 Database Access
- **Connection**: PostgreSQL on Google Cloud SQL
- **Authentication**: IAM-based authentication
- **Connection Pool**: SQLAlchemy default
- **Migrations**: Alembic-based schema management

## 3. Database Tables & Change Frequency

### 3.1 High-Frequency Changes (> Monthly)

#### `hearings` Table
- **Change Frequency**: Multiple times per day
- **Change Types**: New hearings, status updates, location changes
- **Columns Affected**:
  - `status` (scheduled → completed)
  - `location` (room changes)
  - `date_time` (reschedules)
  - `title` (title updates)
  - `description` (agenda changes)
- **Data Sources**: Congress.gov API, web scraping
- **Update Triggers**: Daily scheduled updates, manual updates

#### `witnesses` Table
- **Change Frequency**: Weekly
- **Change Types**: New witnesses, title changes
- **Columns Affected**:
  - `name` (new witnesses)
  - `title` (title updates)
  - `organization` (affiliation changes)
- **Data Sources**: Web scraping from hearing pages

#### `hearing_documents` Table
- **Change Frequency**: Weekly
- **Change Types**: New documents, document updates
- **Columns Affected**:
  - `document_url` (new documents)
  - `document_type` (classification updates)
  - `title` (document name changes)
- **Data Sources**: Web scraping from hearing pages

### 3.2 Medium-Frequency Changes (Monthly)

#### `committee_memberships` Table
- **Change Frequency**: Monthly (during Congress session)
- **Change Types**: Leadership changes, new assignments
- **Columns Affected**:
  - `role` (Chair, Ranking Member changes)
  - `is_current` (membership status)
  - `start_date` / `end_date` (term changes)
- **Data Sources**: Congress.gov API committee assignments

#### `committees` Table
- **Change Frequency**: Monthly
- **Change Types**: URL updates, subcommittee changes
- **Columns Affected**:
  - `official_website_url` (website changes)
  - `hearings_url` (hearing page updates)
  - `members_url` (member page updates)
  - `jurisdiction` (jurisdiction updates)
- **Data Sources**: Web scraping validation, manual updates

### 3.3 Low-Frequency Changes (< Monthly)

#### `members` Table
- **Change Frequency**: Quarterly or less
- **Change Types**: New members, contact updates, photo updates
- **Columns Affected**:
  - `is_current` (active status)
  - `phone` / `email` / `website` (contact info)
  - `photo_url` (profile photos)
  - `term_start` / `term_end` (term dates)
- **Data Sources**: Congress.gov API member endpoint

## 4. Data Processing Pipeline

### 4.1 Current Architecture
- **Monolithic Service**: Single FastAPI application
- **Components**:
  - API endpoints (`/api/v1/`)
  - Data processors (`services/data_processor.py`)
  - Web scrapers (`scrapers/`)
  - Database models (`models/`)
  - Background tasks (FastAPI BackgroundTasks)

### 4.2 Data Flow
1. **Scheduled Trigger** → Cloud Scheduler → API endpoint
2. **API Endpoint** → Background task → Data processor
3. **Data Processor** → Congress.gov API / Web scrapers
4. **Raw Data** → Validation → Database upsert
5. **Database** → API responses → Frontend

### 4.3 Current Bottlenecks
- **Single Point of Failure**: Monolithic API handles all concerns
- **Mixed Responsibilities**: Read/write operations in same service
- **No Data Validation**: Direct database writes without quality gates
- **Limited Observability**: Basic logging, no metrics
- **No Rollback Capability**: No schema versioning or migration rollbacks

## 5. External Dependencies

### 5.1 Google Cloud Platform
- **Cloud Run**: API hosting
- **Cloud SQL**: PostgreSQL database
- **Cloud Scheduler**: Automated data updates
- **Cloud Storage**: Frontend hosting
- **Cloud Monitoring**: Basic uptime monitoring

### 5.2 Third-Party Services
- **Congress.gov API**: Primary data source
- **Material-UI**: Frontend component library
- **React**: Frontend framework

## 6. Security Considerations

### 6.1 API Keys
- **Congress.gov**: Stored in environment variables
- **Database**: IAM-based authentication
- **No API Rate Limiting**: Public endpoints without authentication

### 6.2 Data Access
- **Public Data**: All congressional data is public
- **No PII**: No personally identifiable information beyond public records
- **CORS**: Currently allows all origins (`*`)

## 7. Monitoring & Observability

### 7.1 Current Monitoring
- **Health Checks**: `/health` endpoint
- **Rate Limit Tracking**: Congress.gov API usage
- **Basic Logging**: Structured logging with structlog
- **Uptime Monitoring**: Google Cloud Monitoring

### 7.2 Missing Observability
- **Request Metrics**: No latency, throughput, or error rate tracking
- **Business Metrics**: No data quality or coverage metrics
- **Distributed Tracing**: No trace correlation across services
- **Alerting**: No automated alerts for data quality issues

## 8. Recommendations for Refactoring

### 8.1 Service Separation
- **Ingestion Service**: Handle data collection and processing
- **Validation Service**: Data quality and validation pipelines
- **API Service**: Read-only public API with caching

### 8.2 Data Pipeline Improvements
- **Schema Versioning**: Implement v20250708 contract versioning
- **Data Validation**: Great Expectations for data quality
- **Pipeline Orchestration**: Dagster for workflow management
- **Monitoring**: Prometheus metrics for observability

### 8.3 Infrastructure Enhancements
- **Terraform**: Infrastructure as Code
- **Container Orchestration**: Proper service isolation
- **Database Migrations**: Alembic with rollback capabilities
- **CI/CD**: Automated testing and deployment

---

**Evidence Collection Complete**: Ready for Task-A1 (Architecture) ADR generation.