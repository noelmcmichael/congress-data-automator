# Development Guide

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- Docker (optional)
- PostgreSQL (for local development)

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd congress_data_automator

# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Setup frontend
cd frontend
npm install
cd ..

# Environment configuration
cp .env.example .env
# Edit .env with your settings
```

### Local Database Setup

```bash
# Create PostgreSQL database
createdb congress_db

# Run initial migration
cd backend
python database_setup.py

# Load sample data
python load_initial_data.py
```

### Development Servers

```bash
# Terminal 1: Backend
cd backend
python main.py
# API: http://localhost:8000

# Terminal 2: Frontend
cd frontend
npm start
# Frontend: http://localhost:3000
```

## Project Structure

```
congress_data_automator/
├── backend/                 # FastAPI application
│   ├── main.py             # Application entry point
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── utils/              # Helper functions
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   ├── hooks/          # Custom hooks
│   │   └── utils/          # Utilities
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
├── services/               # Monitoring services
├── infrastructure/         # Deployment configs
└── docker-compose.yml      # Local development
```

## Development Workflow

### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/description

# Regular commits
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/description
```

### Commit Convention
```bash
feat: new feature
fix: bug fix
docs: documentation
style: formatting
refactor: code restructuring
test: adding tests
chore: maintenance
```

## Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_api.py::test_get_members
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- --testNamePattern="MemberList"
```

### Integration Tests
```bash
# Start local services
docker-compose up -d

# Run integration tests
python test_integration.py

# Cleanup
docker-compose down
```

## Code Quality

### Python Standards
- **Formatter**: Black
- **Linter**: flake8
- **Type Checking**: mypy
- **Import Sorting**: isort

```bash
# Format code
black backend/

# Lint code
flake8 backend/

# Type check
mypy backend/

# Sort imports
isort backend/
```

### JavaScript Standards
- **Formatter**: Prettier
- **Linter**: ESLint
- **Type Checking**: TypeScript

```bash
cd frontend

# Format code
npm run format

# Lint code
npm run lint

# Type check
npm run type-check
```

## Debugging

### Backend Debugging
```bash
# Debug mode
DEBUG=true python main.py

# Enable SQL logging
DATABASE_LOG_LEVEL=DEBUG python main.py

# Use debugger
import pdb; pdb.set_trace()
```

### Frontend Debugging
```bash
# Development mode
npm start

# Debug build
npm run build && npm run serve

# Browser DevTools
# React Developer Tools extension recommended
```

### Database Debugging
```bash
# Connect to local database
psql congress_db

# View tables
\dt

# Analyze queries
EXPLAIN ANALYZE SELECT * FROM members;

# Debug API queries
python debug_database.py
```

## Environment Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/congress_db

# API Configuration
SECRET_KEY=your-secret-key
CONGRESS_API_KEY=your-api-key
API_HOST=localhost
API_PORT=8000

# Development
DEBUG=true
LOG_LEVEL=DEBUG

# External Services
GOOGLE_CLOUD_PROJECT=your-project
```

### Local vs Production
- **Database**: Local PostgreSQL vs Cloud SQL
- **API**: Local server vs Cloud Run
- **Frontend**: Development server vs Cloud Storage
- **Monitoring**: Console logging vs Cloud Logging

## Performance Testing

### Load Testing
```bash
# Install artillery
npm install -g artillery

# Run load test
artillery run load-test.yml

# Monitor performance
python monitor_performance.py
```

### Profile Backend
```bash
# Install profiling tools
pip install line_profiler memory_profiler

# Profile function
@profile
def slow_function():
    pass

# Run profiler
kernprof -l -v main.py
```

## Database Development

### Migrations
```bash
# Create migration
python create_migration.py "add_new_column"

# Run migrations
python migrate.py

# Rollback migration
python migrate.py --rollback
```

### Schema Changes
```sql
-- Example migration
ALTER TABLE members ADD COLUMN new_field VARCHAR(255);
CREATE INDEX idx_members_new_field ON members(new_field);
```

### Data Seeding
```bash
# Load test data
python load_test_data.py

# Load production data (careful!)
python load_production_data.py --confirm
```

## API Development

### Adding New Endpoints
```python
# backend/routes/new_endpoint.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "Hello World"}
```

### Request/Response Models
```python
from pydantic import BaseModel

class MemberRequest(BaseModel):
    name: str
    party: str

class MemberResponse(BaseModel):
    id: int
    name: str
    party: str
```

### Authentication
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    # Validate token
    return user
```

## Frontend Development

### Component Development
```typescript
// Component structure
interface Props {
  member: Member;
}

export const MemberCard: React.FC<Props> = ({ member }) => {
  return (
    <Card>
      <CardContent>
        <Typography>{member.name}</Typography>
      </CardContent>
    </Card>
  );
};
```

### State Management
```typescript
// Using React Query for API state
import { useQuery } from 'react-query';

export const useMembers = () => {
  return useQuery('members', fetchMembers);
};
```

### Styling
```typescript
// Material-UI theming
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});
```

## Monitoring Development

### Local Monitoring
```bash
# Start monitoring services
python services/health_monitor.py

# View monitoring dashboard
open http://localhost:8001/monitoring
```

### Logging
```python
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Log events
logger.info("User action completed")
logger.error("Error occurred", exc_info=True)
```

### Metrics
```python
from prometheus_client import Counter, Histogram

# Define metrics
api_requests = Counter('api_requests_total', 'API requests')
response_time = Histogram('response_time_seconds', 'Response time')

# Record metrics
api_requests.inc()
response_time.observe(0.1)
```

## Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check database status
pg_ctl status

# Restart database
brew services restart postgresql

# Check connection
psql -h localhost -p 5432 -U username congress_db
```

#### API Not Starting
```bash
# Check port usage
lsof -i :8000

# Check environment
echo $DATABASE_URL

# Check dependencies
pip list | grep fastapi
```

#### Frontend Build Error
```bash
# Clear node modules
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version

# Clear cache
npm cache clean --force
```

### Debug Tools
- **Backend**: Python Debugger (pdb), VS Code debugger
- **Database**: pgAdmin, DBeaver, psql
- **Frontend**: React DevTools, Chrome DevTools
- **API**: Postman, curl, HTTPie
- **Performance**: Chrome DevTools, Artillery

---

For deployment information, see [Operations Runbook](runbook/).
For API details, see [API Reference](api.md).