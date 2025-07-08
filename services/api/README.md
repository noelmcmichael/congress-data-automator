# Congressional Data API Service

Enterprise-grade read-only FastAPI service for accessing validated congressional data.

## Overview

The API service provides a high-performance, scalable REST API for accessing congressional data that has been validated through the validation service. It includes caching, rate limiting, and comprehensive error handling.

## Features

- **High Performance**: FastAPI-based with async support
- **Data Validation**: Pydantic models for request/response validation
- **Caching**: Redis-based caching for frequently accessed data
- **Rate Limiting**: Configurable rate limiting to prevent abuse
- **Comprehensive API**: Full CRUD operations for congressional data
- **OpenAPI Documentation**: Automatic API documentation generation
- **Health Checks**: Detailed health monitoring endpoints
- **Error Handling**: Comprehensive error handling and logging

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL database (with validated data)
- Redis (for caching)
- Poetry for dependency management

### Installation

```bash
# Install dependencies
poetry install

# Copy environment configuration
cp .env.example .env

# Edit .env with your configuration
```

### Configuration

Key environment variables:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/congress_data

# API
API_HOST=0.0.0.0
API_PORT=8003

# Redis
REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Running the Service

```bash
# Development mode (with auto-reload)
python main.py dev

# Production mode
python main.py api

# Initialize service only
python main.py init
```

### API Documentation

- **Swagger UI**: `http://localhost:8003/docs`
- **ReDoc**: `http://localhost:8003/redoc`

## Architecture

### Project Structure

```
api/
├── core/           # Core functionality
│   ├── config.py   # Configuration management
│   ├── logging.py  # Structured logging
│   └── exceptions.py # Custom exceptions
├── models/         # Pydantic models
│   ├── base.py     # Base models
│   └── congress.py # Congressional data models
├── database/       # Database layer
│   ├── models.py   # SQLAlchemy models
│   └── connection.py # Database connection management
├── endpoints/      # API endpoints
│   ├── members.py  # Member endpoints
│   ├── committees.py # Committee endpoints
│   └── hearings.py # Hearing endpoints
└── utils/          # Utility functions
```

### Data Models

#### Members
- **GET /api/v1/members**: List members with filtering and pagination
- **GET /api/v1/members/{id}**: Get member details
- **GET /api/v1/members/{id}/committees**: Get member committee assignments

#### Committees
- **GET /api/v1/committees**: List committees with filtering and pagination
- **GET /api/v1/committees/{id}**: Get committee details
- **GET /api/v1/committees/{id}/members**: Get committee member roster
- **GET /api/v1/committees/{id}/subcommittees**: Get committee subcommittees

#### Hearings
- **GET /api/v1/hearings**: List hearings with filtering and pagination
- **GET /api/v1/hearings/{id}**: Get hearing details
- **GET /api/v1/hearings/{id}/witnesses**: Get hearing witnesses

### Health Checks

- **GET /health**: Simple health check
- **GET /healthz**: Detailed health check with database status

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api --cov-report=html

# Run specific test file
pytest tests/test_members.py
```

### Code Quality

```bash
# Format code
black api/
isort api/

# Lint code
flake8 api/

# Type checking
mypy api/
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_test.py --host=http://localhost:8003
```

## Deployment

### Docker

```bash
# Build image
docker build -t congressional-data-api .

# Run container
docker run -p 8003:8003 congressional-data-api
```

### Environment Variables

Production environment variables:

```bash
DATABASE_URL=postgresql://user:password@prod-db:5432/congress_data
REDIS_URL=redis://prod-redis:6379/0
ENVIRONMENT=production
LOG_LEVEL=INFO
API_WORKERS=4
```

## API Usage Examples

### Get All Members

```bash
curl "http://localhost:8003/api/v1/members?page=1&size=20"
```

### Filter Members by State

```bash
curl "http://localhost:8003/api/v1/members?state=CA&party=Democratic"
```

### Get Member Details

```bash
curl "http://localhost:8003/api/v1/members/1"
```

### Search Committees

```bash
curl "http://localhost:8003/api/v1/committees?search=judiciary"
```

### Get Committee Members

```bash
curl "http://localhost:8003/api/v1/committees/1/members"
```

## Performance

### Caching Strategy

- **Member data**: Cached for 1 hour
- **Committee data**: Cached for 6 hours
- **Hearing data**: Cached for 30 minutes
- **Search results**: Cached for 15 minutes

### Rate Limiting

- **Default**: 100 requests per minute per IP
- **Authenticated**: 1000 requests per minute per user
- **Burst**: 10 requests per second

### Database Optimization

- **Connection pooling**: 20 connections with 10 overflow
- **Query optimization**: Optimized joins and indexes
- **Read replicas**: Support for read-only replicas

## Monitoring

### Health Checks

- **Database connectivity**: Connection and query tests
- **Redis connectivity**: Cache availability tests
- **Memory usage**: Memory consumption monitoring
- **Response times**: API response time tracking

### Logging

- **Structured logging**: JSON format with correlation IDs
- **Request logging**: All API requests logged
- **Error logging**: Comprehensive error tracking
- **Performance logging**: Response time and resource usage

## Security

### Input Validation

- **Pydantic models**: Comprehensive input validation
- **SQL injection protection**: Parameterized queries
- **XSS prevention**: Input sanitization
- **CORS configuration**: Proper origin restrictions

### Rate Limiting

- **IP-based limiting**: Per-IP request limits
- **User-based limiting**: Per-user request limits
- **Endpoint-specific limits**: Different limits per endpoint
- **Burst protection**: Short-term burst prevention

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.