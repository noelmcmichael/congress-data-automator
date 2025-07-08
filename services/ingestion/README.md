# Congressional Data Ingestion Service

Enterprise-grade data collection and staging service for congressional information.

## Overview

The ingestion service is responsible for collecting data from multiple sources and staging it for validation. It follows enterprise-grade patterns with proper typing, logging, error handling, and observability.

## Features

- **Congress.gov API Integration**: Comprehensive API client with rate limiting
- **Web Scraping**: Respectful scraping of House.gov and Senate.gov
- **Data Staging**: Structured staging tables for raw data
- **Enterprise Logging**: Structured logging with correlation IDs
- **Health Checks**: Container-ready health endpoints
- **Type Safety**: Full type annotations with mypy validation
- **Error Handling**: Comprehensive error handling and retry logic

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Congress.gov  │    │   House.gov     │    │   Senate.gov    │
│   API Client    │    │   Scraper       │    │   Scraper       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Data Processor │
                    │  Coordinator    │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Staging Tables  │
                    │ (PostgreSQL)    │
                    └─────────────────┘
```

## Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   poetry install
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the Service**
   ```bash
   poetry run python main.py
   ```

### Docker

1. **Build Image**
   ```bash
   docker build -t congressional-ingestion .
   ```

2. **Run Container**
   ```bash
   docker run -p 8000:8000 \
     -e DATABASE_URL="postgresql://..." \
     -e CONGRESS_API_KEY="your-key" \
     congressional-ingestion
   ```

## Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `CONGRESS_API_KEY` | Congress.gov API key | `your-32-character-api-key` |
| `SECRET_KEY` | Application secret key | `your-secret-key` |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Environment name |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FORMAT` | `json` | Log format (json/text) |
| `SCRAPING_DELAY` | `1.0` | Delay between web requests |

## API Endpoints

### Health and Status

- `GET /` - Service information
- `GET /healthz` - Health check (for container orchestration)
- `GET /metrics` - Metrics for monitoring

### Data Ingestion

- `POST /ingest/members` - Ingest congressional members
- `POST /ingest/committees` - Ingest congressional committees  
- `POST /ingest/hearings` - Ingest congressional hearings

## Data Sources

### Congress.gov API
- **Rate Limit**: 5,000 requests per day
- **Endpoints**: Members, committees, hearings, bills
- **Authentication**: API key required

### Web Scraping
- **Sources**: House.gov, Senate.gov, committee websites
- **Rate Limit**: 1 second delay between requests
- **Content**: Hearing information, committee details

## Database Schema

### Staging Tables

All raw data is stored in the `staging` schema before validation:

- `staging.members` - Congressional members
- `staging.committees` - Congressional committees
- `staging.hearings` - Congressional hearings
- `staging.witnesses` - Hearing witnesses
- `staging.documents` - Hearing documents

## Development

### Code Quality

```bash
# Type checking
poetry run mypy ingestion/

# Code formatting
poetry run black ingestion/
poetry run isort ingestion/

# Testing
poetry run pytest
```

### Adding New Collectors

1. Create collector class in `ingestion/collectors/`
2. Inherit from `LoggerMixin` for consistent logging
3. Implement async methods with proper error handling
4. Add type annotations for all methods
5. Update `DataProcessor` to use new collector

### Adding New Data Types

1. Create staging model in `ingestion/models/staging.py`
2. Add transformation logic in `DataProcessor`
3. Create ingestion endpoint in `main.py`
4. Update documentation

## Monitoring

### Health Checks

The service provides health checks for container orchestration:

```bash
curl http://localhost:8000/healthz
```

### Logging

Structured JSON logging with correlation IDs:

```json
{
  "timestamp": "2025-01-08T20:00:00Z",
  "level": "info",
  "service": "congressional-ingestion",
  "operation": "collect_all_members",
  "duration_ms": 1500,
  "records_processed": 541
}
```

### Metrics

The service exposes metrics for Prometheus monitoring:

```bash
curl http://localhost:8000/metrics
```

## Error Handling

The service implements comprehensive error handling:

- **Rate Limiting**: Automatic delays and exponential backoff
- **Retry Logic**: Configurable retry attempts with backoff
- **Circuit Breaker**: Domain-level failure protection
- **Graceful Degradation**: Partial success handling
- **Error Correlation**: Structured error logging with context

## Security

- **Non-root Container**: Runs as dedicated user
- **Secrets Management**: Environment variable configuration
- **Input Validation**: Pydantic model validation
- **SQL Injection Protection**: SQLAlchemy ORM usage
- **Rate Limiting**: Respectful API and scraping behavior

## Performance

- **Async Processing**: Full async/await implementation
- **Connection Pooling**: Database and HTTP connection reuse
- **Batch Processing**: Bulk database operations
- **Memory Efficiency**: Streaming data processing
- **Background Tasks**: Non-blocking ingestion operations

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check `DATABASE_URL` format
   - Verify database accessibility
   - Confirm staging schema exists

2. **Congress API Rate Limited**
   - Check daily request count
   - Verify API key validity
   - Adjust request delays

3. **Web Scraping Blocked**
   - Check circuit breaker status
   - Verify user agent configuration
   - Review rate limiting settings

### Debug Mode

Enable debug logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
export LOG_FORMAT=text
```

## Contributing

1. Follow the established patterns in existing collectors
2. Add comprehensive type annotations
3. Include structured logging for all operations
4. Write tests for new functionality
5. Update documentation for new features

## License

Part of the Congressional Data Automation Service project.