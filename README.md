# Congressional Data Automation Service

Production-ready platform providing current, accurate information about the U.S. Congress through a modern web interface and high-performance API with automated monitoring and data validation.

## 🚀 Live System Status

[![System Status](https://img.shields.io/badge/status-operational-brightgreen)](https://congressional-data-api-v2-1066017671167.us-central1.run.app/health)
[![API Performance](https://img.shields.io/badge/API-<200ms-green)](https://congressional-data-api-v2-1066017671167.us-central1.run.app)
[![Data Currency](https://img.shields.io/badge/congress-119th%20(current)-blue)](https://storage.googleapis.com/congressional-data-frontend/index.html)
[![Security](https://img.shields.io/badge/security-A+-brightgreen)](#security-features)

- **🌐 Frontend**: https://storage.googleapis.com/congressional-data-frontend/index.html
- **🔗 API**: https://congressional-data-api-v2-1066017671167.us-central1.run.app
- **📊 Coverage**: 541 Congressional members, 199 committees (119th Congress)

## ⚡ Quick Start

### Option 1: Use Live System (Recommended)
```bash
# Test the API
curl https://congressional-data-api-v2-1066017671167.us-central1.run.app/members

# Visit the web interface
open https://storage.googleapis.com/congressional-data-frontend/index.html
```

### Option 2: Local Development
```bash
# Clone and setup
git clone <repository-url>
cd congress_data_automator

# Backend
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && python main.py

# Frontend (new terminal)
cd frontend && npm install && npm start
```

### Option 3: Docker
```bash
docker-compose up -d
# Frontend: http://localhost:3000, API: http://localhost:8000
```

## 📚 Feature Catalogue

### **Data Services**
- **Current Congressional Data**: 119th Congress members and committees
- **Real-time Validation**: Wikipedia cross-reference for accuracy
- **Data Export**: Multiple formats (CSV, JSON, JSONL) with streaming
- **Advanced Search**: Full-text search with autocomplete and suggestions
- **Smart Filtering**: Complex filter combinations with validation

### **Monitoring & Operations**
- **Automated Health Checks**: 5 monitoring services for system components
- **Real-time Alerts**: Multi-channel notifications for issues
- **Performance Monitoring**: API, cache, database, and export tracking
- **Unified Dashboard**: Combined metrics and health assessment
- **Self-healing Systems**: Automatic recovery for common issues

### **Security & Performance**
- **Rate Limiting**: 100 requests/minute per IP with proper responses
- **Input Validation**: SQL injection and XSS prevention
- **Response Caching**: 50% performance improvement with intelligent TTL
- **Database Optimization**: 20 performance indexes and connection pooling
- **Security Headers**: HSTS, CSP, XSS protection, clickjacking prevention

### **User Experience**
- **Responsive Design**: Modern Material-UI interface
- **Interactive Documentation**: Live API documentation with examples
- **Progressive Loading**: Optimized loading for large datasets
- **Cross-platform Access**: Web interface and REST API
- **Developer-friendly**: Clean API design with comprehensive docs

## 🏗️ Architecture Overview

### **📊 High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Service   │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Material-UI   │    │   + Caching     │    │   Cloud SQL     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cloud Storage │    │   Cloud Run     │    │   Monitoring    │
│   Static Assets │    │   Auto-scaling  │    │   + Alerting    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Technology Stack**: React 18 + FastAPI + PostgreSQL + Google Cloud Platform

For detailed architecture documentation, see [docs/architecture.md](docs/architecture.md).

## 🛠️ Supported Runtime Matrix

| Component | Technology | Version | Platform |
|-----------|------------|---------|----------|
| **Backend** | Python | 3.9+ | Linux, macOS, Windows |
| **Frontend** | Node.js | 16+ | Cross-platform |
| **Database** | PostgreSQL | 13+ | Cloud SQL, Local |
| **Infrastructure** | Google Cloud | Current | GCP services |
| **Containers** | Docker | Latest | Multi-platform |

## 🤝 Contributing

### **How to Contribute**
1. Fork the repository and create a feature branch
2. Follow our [Development Setup Guide](docs/development.md)
3. Make changes with appropriate tests (90%+ coverage required)
4. Submit a pull request with clear description

### **Standards**
- **Code Quality**: Black formatting, ESLint compliance
- **Testing**: Unit tests for new features
- **Documentation**: Update relevant docs
- **Security**: Follow security best practices

### **Issues & Support**
- **Bug Reports**: GitHub Issues with reproduction steps
- **Feature Requests**: Include use case and implementation ideas
- **Security**: Email security concerns privately
- **Questions**: GitHub Discussions for general help

## 📄 Further Reading

### **📖 Documentation**
- **[API Reference](docs/api.md)**: Complete API documentation
- **[Architecture Guide](docs/architecture.md)**: Detailed system design
- **[Operations Runbook](docs/runbook/)**: Deployment and monitoring
- **[Development Guide](docs/development.md)**: Local setup and testing

### **📊 Project Resources**
- **[CHANGELOG.md](CHANGELOG.md)**: Version history and changes
- **[Project Rules](rules.md)**: Development guidelines
- **[Expansion Plans](docs/plans/)**: Future development options
- **[Legacy Archive](docs/archive/)**: Historical documentation

### **🔗 External Resources**
- **[Congress.gov API](https://api.congress.gov/)**: Official data source
- **[Interactive API Docs](https://congressional-data-api-v2-1066017671167.us-central1.run.app/docs)**: Live API reference
- **[FastAPI](https://fastapi.tiangolo.com/)** | **[React](https://reactjs.org/)** | **[Google Cloud](https://cloud.google.com/)**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

🤖 Built with [Memex](https://memex.tech) AI Assistant

*Production-ready Congressional data platform with automated monitoring and comprehensive security.*