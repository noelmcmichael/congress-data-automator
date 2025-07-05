# Congressional Data Automation Service

A comprehensive service for automatically collecting, processing, and serving congressional data from multiple sources including the Congress.gov API and official congressional websites.

## Project Status

### Phase 1: Project Setup & Architecture ✅
- [x] Create GitHub repository and project structure
- [x] Define architecture and technology stack
- [x] Set up GCP project configuration
- [x] Create project rules and best practices document
- [x] Initialize development environment

### Phase 2: Infrastructure Setup ✅
- [x] Create Python virtual environment and install dependencies
- [x] Set up FastAPI application with basic endpoints
- [x] Create database models for members, committees, hearings
- [x] Implement Congress.gov API client with rate limiting
- [x] Configure structured logging and error handling
- [x] Create Docker containerization with Dockerfile
- [x] Set up CI/CD pipeline with GitHub Actions
- [x] Configure local development with Docker Compose
- [x] Create comprehensive deployment documentation
- [x] Add automated testing with pytest (16/18 tests passing)
- [ ] Configure GCP services (Cloud SQL, Cloud Run, Cloud Scheduler) - awaiting billing setup

### Phase 3: Core Data Services 🔄
- [x] Implement Congress.gov API client with rate limiting
- [x] Create web scraping modules for House/Senate websites
- [x] Build data processing and ETL pipeline
- [x] Create API endpoints for data updates and testing
- [ ] Set up scheduled data updates with background jobs
- [ ] Implement video URL extraction from committee pages
- [ ] Add data validation and error handling

### Phase 4: API & Frontend 📋
- [ ] Create public REST API
- [ ] Build React admin UI
- [ ] Add search, filter, and sort functionality

### Phase 5: Deployment & Monitoring 📋
- [ ] Deploy to production
- [ ] Set up monitoring and logging
- [ ] Performance optimization

## Architecture Overview

### Technology Stack
- **Database**: Google Cloud SQL (PostgreSQL)
- **Backend**: Python (FastAPI)
- **Frontend**: React.js
- **Infrastructure**: Google Cloud Platform
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Orchestration**: Google Cloud Run
- **Scheduling**: Google Cloud Scheduler

### GCP Services
- **Cloud SQL**: PostgreSQL database for storing congressional data
- **Cloud Run**: Containerized services for API and web scraping
- **Cloud Scheduler**: Automated data updates
- **Cloud Build**: CI/CD pipeline
- **Cloud Storage**: File storage for documents and media
- **Cloud CDN**: Content delivery for frontend

## Data Sources

### Primary Sources
1. **Congress.gov API**: Members, committees, hearings, legislation
2. **House.gov**: Committee pages, hearing details, video streams
3. **Senate.gov**: Committee pages, hearing details, video streams
4. **Individual Committee Websites**: Additional hearing information

### Data Types
- **Members**: Representatives and Senators
- **Committees**: House and Senate committees and subcommittees
- **Hearings**: Scheduled and past hearings with metadata
- **Witnesses**: Hearing witnesses and testimony
- **Videos**: Embedded video stream URLs
- **Documents**: Committee reports and testimony files

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker
- Google Cloud SDK
- GitHub CLI

### Development Setup

#### Quick Start with Docker
```bash
git clone https://github.com/noelmcmichael/congress-data-automator.git
cd congress-data-automator
docker-compose up
```

#### Manual Setup
1. Clone the repository
2. Set up Python virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -r backend/requirements.txt`
4. Configure environment variables (see .env.example)
5. Set up local database
6. Run development server: `uvicorn app.main:app --reload`

#### Testing
```bash
cd backend
pytest tests/ -v
```

## Project Structure

```
congress_data_automator/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── crud/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── scrapers/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── infrastructure/
│   ├── terraform/
│   └── docker/
├── .github/
│   └── workflows/
├── docs/
└── scripts/
```

## Progress Log

### 2025-01-04
- Initial project setup
- Created GitHub repository
- Defined architecture and technology stack
- Set up project structure
- Created rules and best practices document
- Implemented core backend structure with FastAPI
- Created database models for members, committees, hearings
- Built Congress.gov API client with rate limiting
- Set up development environment with virtual environment
- Created web scrapers for House.gov and Senate.gov
- Built data processing service to coordinate API and scraping
- Added API endpoints for data updates and testing
- Successfully tested Congress.gov API integration
- Implemented video URL extraction from committee pages
- Created Docker containerization and CI/CD pipeline
- Built comprehensive test suite with 89% pass rate
- Set up deployment configurations for multiple platforms
- Created development environment with Docker Compose
- Added automated testing and code quality checks

### 2025-01-05
- **FIXED**: Database configuration and table creation issues
- **FIXED**: Congress.gov API data parsing for member names, chambers, states
- **IMPLEMENTED**: State name to abbreviation mapping utility
- **IMPLEMENTED**: Full name parsing for congressional members
- **TESTED**: Local development environment with Docker Compose
- **VERIFIED**: API endpoints working correctly (health, status, test endpoints)
- **VERIFIED**: Congress.gov API integration functional (4999/5000 daily requests remaining)
- **VERIFIED**: Web scraper integration working for House.gov and Senate.gov
- **DEPLOYED**: Successfully deployed to Google Cloud Platform
  - **Cloud SQL**: PostgreSQL database created and configured
  - **Cloud Run**: Containerized API service deployed and running
  - **Service URL**: https://congressional-data-api-1066017671167.us-central1.run.app
  - **Status**: Production service active and responding to requests
- **TESTED**: Production deployment verification
  - Health endpoints responding correctly
  - Congress.gov API integration working in production
  - Database connection established via Cloud SQL Proxy
  - All API endpoints accessible and functional

---

🤖 Generated with [Memex](https://memex.tech)
