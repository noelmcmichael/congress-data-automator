# API Reference

## Base URL
```
Production: https://congressional-data-api-v2-1066017671167.us-central1.run.app
Local: http://localhost:8000
```

## Authentication
No authentication required for read operations. Rate limiting: 100 requests/minute per IP.

## Response Format
All endpoints return JSON. Errors include standard HTTP status codes with descriptive messages.

```json
{
  "detail": "Error description",
  "status_code": 400
}
```

## Core Endpoints

### Members

#### List Members
```http
GET /members
```

**Query Parameters:**
- `party` (string): Filter by party (Republican, Democratic, Independent)
- `state` (string): Filter by state abbreviation (e.g., "CA", "TX")
- `chamber` (string): Filter by chamber (House, Senate)
- `limit` (int): Limit results (default: 100, max: 500)
- `offset` (int): Offset for pagination (default: 0)

**Response:**
```json
{
  "members": [
    {
      "id": 1,
      "name": "John Doe",
      "party": "Republican",
      "state": "TX",
      "chamber": "House",
      "district": "1",
      "leadership_position": null,
      "committees": [...]
    }
  ],
  "total": 541,
  "limit": 100,
  "offset": 0
}
```

#### Get Member
```http
GET /members/{member_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "party": "Republican",
  "state": "TX",
  "chamber": "House",
  "district": "1",
  "leadership_position": "Speaker",
  "biography": "...",
  "committees": [
    {
      "id": 1,
      "name": "House Committee on Ways and Means",
      "role": "Member"
    }
  ]
}
```

#### Search Members
```http
GET /members/search?q={query}
```

**Query Parameters:**
- `q` (string, required): Search query
- `limit` (int): Limit results
- `suggest` (bool): Return search suggestions

**Response:**
```json
{
  "members": [...],
  "suggestions": ["John Smith", "Jane Doe"],
  "total": 5
}
```

#### Export Members
```http
GET /members/export?format={format}
```

**Query Parameters:**
- `format` (string): Export format (csv, json, jsonl)
- `party`, `state`, `chamber`: Same filters as list endpoint

**Response:** File download with appropriate Content-Type

### Committees

#### List Committees
```http
GET /committees
```

**Query Parameters:**
- `chamber` (string): Filter by chamber (House, Senate, Joint)
- `type` (string): Filter by type (Standing, Select, Special)
- `limit` (int): Limit results
- `offset` (int): Offset for pagination

**Response:**
```json
{
  "committees": [
    {
      "id": 1,
      "name": "House Committee on Agriculture",
      "chamber": "House",
      "type": "Standing",
      "chair": {
        "id": 123,
        "name": "Jane Smith"
      },
      "ranking_member": {
        "id": 124,
        "name": "Bob Johnson"
      },
      "members_count": 52
    }
  ],
  "total": 199,
  "limit": 100,
  "offset": 0
}
```

#### Get Committee
```http
GET /committees/{committee_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "House Committee on Agriculture",
  "chamber": "House",
  "type": "Standing",
  "jurisdiction": "Agriculture, forestry, and related matters",
  "chair": {...},
  "ranking_member": {...},
  "members": [
    {
      "id": 1,
      "name": "John Doe",
      "party": "Republican",
      "role": "Member",
      "rank": 3
    }
  ],
  "subcommittees": [...]
}
```

### Search

#### Universal Search
```http
GET /search?q={query}&type={type}
```

**Query Parameters:**
- `q` (string, required): Search query
- `type` (string): Filter by type (members, committees, all)
- `limit` (int): Limit results

**Response:**
```json
{
  "results": {
    "members": [...],
    "committees": [...]
  },
  "suggestions": [...],
  "total": 15
}
```

### System

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-08T10:30:00Z",
  "version": "4.0.0",
  "database": "connected",
  "api_response_time": "0.123s"
}
```

#### Monitoring Dashboard
```http
GET /monitoring
```

**Response:**
```json
{
  "system_health": {
    "overall": "healthy",
    "api": "healthy",
    "database": "healthy",
    "cache": "healthy"
  },
  "performance": {
    "api_response_time": "0.15s",
    "cache_hit_rate": "87%",
    "database_response_time": "0.02s"
  },
  "data_quality": {
    "members_count": 541,
    "committees_count": 199,
    "last_update": "2025-01-08T08:00:00Z",
    "accuracy_score": "99.2%"
  }
}
```

#### API Documentation
```http
GET /docs
```
Interactive Swagger/OpenAPI documentation

## Advanced Features

### Export Endpoints

#### Stream Export
```http
GET /export/stream?table={table}&format={format}
```

**Query Parameters:**
- `table` (string): Table to export (members, committees)
- `format` (string): Export format (csv, json, jsonl)
- Filtering parameters based on table

**Response:** Streaming download for large datasets

### Caching

API responses are cached for improved performance:
- **Member lists**: 5 minutes
- **Individual members**: 15 minutes
- **Committee lists**: 10 minutes
- **Search results**: 2 minutes

Cache headers included in responses:
```http
Cache-Control: public, max-age=300
ETag: "abc123"
Last-Modified: Mon, 08 Jan 2025 10:00:00 GMT
```

### Rate Limiting

Rate limits are enforced per IP address:
- **Limit**: 100 requests per minute
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **Exceeded**: HTTP 429 with retry information

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 75
X-RateLimit-Reset: 1641632400
```

### Error Handling

Standard HTTP status codes:
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found
- **429**: Too Many Requests (rate limited)
- **500**: Internal Server Error

Error response format:
```json
{
  "detail": "Member with id 999 not found",
  "status_code": 404,
  "timestamp": "2025-01-08T10:30:00Z"
}
```

## Data Models

### Member
```json
{
  "id": "integer",
  "name": "string",
  "party": "string (Republican|Democratic|Independent)",
  "state": "string (2-letter code)",
  "chamber": "string (House|Senate)",
  "district": "string (for House members)",
  "leadership_position": "string|null",
  "term_start": "date",
  "term_end": "date",
  "biography": "string",
  "committees": "array of committee assignments"
}
```

### Committee
```json
{
  "id": "integer",
  "name": "string",
  "chamber": "string (House|Senate|Joint)",
  "type": "string (Standing|Select|Special)",
  "jurisdiction": "string",
  "chair": "member object",
  "ranking_member": "member object",
  "members": "array of member assignments",
  "subcommittees": "array of subcommittee objects"
}
```

### Committee Assignment
```json
{
  "member_id": "integer",
  "committee_id": "integer",
  "role": "string (Chair|Ranking Member|Member)",
  "rank": "integer"
}
```

## Usage Examples

### Python
```python
import requests

# Get all Republican senators
response = requests.get(
    "https://congressional-data-api-v2-1066017671167.us-central1.run.app/members",
    params={"party": "Republican", "chamber": "Senate"}
)
members = response.json()["members"]

# Search for a member
response = requests.get(
    "https://congressional-data-api-v2-1066017671167.us-central1.run.app/members/search",
    params={"q": "John Smith"}
)
results = response.json()
```

### JavaScript
```javascript
// Fetch committee details
async function getCommittee(id) {
  const response = await fetch(
    `https://congressional-data-api-v2-1066017671167.us-central1.run.app/committees/${id}`
  );
  return response.json();
}

// Search with suggestions
async function searchMembers(query) {
  const response = await fetch(
    `https://congressional-data-api-v2-1066017671167.us-central1.run.app/members/search?q=${query}&suggest=true`
  );
  return response.json();
}
```

### curl
```bash
# Export California House members to CSV
curl -O "https://congressional-data-api-v2-1066017671167.us-central1.run.app/members/export?format=csv&state=CA&chamber=House"

# Get system health
curl "https://congressional-data-api-v2-1066017671167.us-central1.run.app/health"
```

---

For more examples and interactive testing, visit the [live API documentation](https://congressional-data-api-v2-1066017671167.us-central1.run.app/docs).