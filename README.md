# Congressional Data Automation Service

A comprehensive service for automatically collecting, processing, and serving congressional data from multiple sources including the Congress.gov API and official congressional websites.

## Project Status

### Phase 1: Project Setup & Architecture ✅
- [x] Create GitHub repository and project structure
- [x] Define architecture and technology stack
- [x] Set up GCP project configuration
- [x] Create project rules and best practices document
- [x] Initialize development environment

### Phase 2: Infrastructure Setup 🔄
- [ ] Configure GCP services (Cloud SQL, Cloud Run, Cloud Scheduler)
- [ ] Set up CI/CD pipeline with GitHub Actions
- [ ] Configure secrets management
- [ ] Create database schema

### Phase 3: Core Data Services 📋
- [ ] Implement Congress.gov API client with rate limiting
- [ ] Create web scraping modules for House/Senate websites
- [ ] Build data processing and ETL pipeline
- [ ] Set up scheduled data updates

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

1. Clone the repository
2. Set up Python virtual environment
3. Install dependencies
4. Configure GCP credentials
5. Set up local database
6. Run development servers

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

---

🤖 Generated with [Memex](https://memex.tech)