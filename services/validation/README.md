# Congressional Data Validation Service

Enterprise-grade data validation and quality assurance service for Congressional data. This service transforms raw staging data into validated production data using Great Expectations and Dagster orchestration.

## 🎯 Purpose

The validation service is responsible for:
- **Data Quality Validation**: Using Great Expectations to validate data integrity
- **Pipeline Orchestration**: Using Dagster to orchestrate validation workflows
- **Schema Management**: Managing versioned database schemas
- **Data Promotion**: Promoting validated data from staging to production
- **Monitoring**: Tracking validation results and data lineage

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Ingestion       │    │ Validation      │    │ API Service     │
│ Service         │───▶│ Service         │───▶│                 │
│                 │    │                 │    │                 │
│ Raw Data        │    │ Quality Gates   │    │ Validated Data  │
│ ↓ staging.*     │    │ ↓ public.*_v*   │    │ ↓ public views  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Features

### Data Validation
- **Great Expectations**: Comprehensive data quality validation
- **Custom Expectations**: Congressional-specific validation rules
- **Automated Reporting**: Validation results and data docs
- **Threshold Monitoring**: Configurable success/failure thresholds

### Pipeline Orchestration
- **Dagster Pipelines**: Orchestrated validation workflows
- **Asset Dependencies**: Clear data lineage and dependencies
- **Scheduling**: Automated validation runs
- **Monitoring**: Pipeline execution tracking

### Schema Management
- **Versioned Schemas**: Schema versioning (v20250708)
- **Migration Support**: Database schema migrations
- **Rollback Capability**: Safe rollback procedures
- **Multi-environment**: Support for staging/production environments

## 📋 Requirements

- Python 3.9+
- PostgreSQL 12+
- Great Expectations 0.18+
- Dagster 1.8+

## 🛠️ Development Setup

1. **Install Dependencies**
   ```bash
   poetry install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

3. **Initialize Great Expectations**
   ```bash
   poetry run python -m validation.cli init-ge
   ```

4. **Run Validation Service**
   ```bash
   poetry run python -m validation.main
   ```

## 🔧 Configuration

The service uses environment variables and `.env` files for configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/congress_db

# Service Configuration
SERVICE_NAME=congressional-data-validation
SERVICE_VERSION=0.1.0
SERVICE_ENVIRONMENT=development

# Great Expectations Configuration
GE_DATA_CONTEXT_ROOT=./great_expectations
GE_STORE_BACKEND=filesystem

# Dagster Configuration
DAGSTER_HOME=./dagster_home
```

## 📊 Data Flow

1. **Ingestion**: Raw data collected into `staging.*` tables
2. **Validation**: Great Expectations validates data quality
3. **Transformation**: Data cleaning and standardization
4. **Promotion**: Validated data promoted to `public.*_v*` tables
5. **Views**: Current views point to latest validated version

## 🧪 Testing

Run the test suite:
```bash
poetry run pytest
```

With coverage:
```bash
poetry run pytest --cov=validation
```

## 📈 Monitoring

The service provides:
- **Health Checks**: `/healthz` endpoint
- **Metrics**: Prometheus-compatible metrics
- **Logging**: Structured JSON logging
- **Data Docs**: Great Expectations data documentation

## 🚢 Deployment

Build and deploy with Docker:
```bash
docker build -t congressional-data-validation .
docker run -p 8002:8002 congressional-data-validation
```

## 🔍 API Endpoints

- `GET /healthz` - Health check
- `GET /status` - Service status and statistics
- `POST /validate/{table}` - Run validation for specific table
- `POST /promote/{table}` - Promote validated data to production
- `GET /metrics` - Prometheus metrics

## 📚 Documentation

- [Great Expectations Data Docs](./great_expectations/docs/) - Auto-generated validation documentation
- [Dagster UI](http://localhost:3000) - Pipeline monitoring and execution
- [API Documentation](http://localhost:8002/docs) - OpenAPI/Swagger docs

## 🤝 Contributing

1. Follow the existing code style (Black, isort, mypy)
2. Write comprehensive tests
3. Update documentation
4. Follow semantic versioning

## 📝 License

This project is part of the Congressional Data Automation Service.

---

*Generated: January 8, 2025*
*Part of the Congressional Data Automation Service enterprise refactoring*