# Chatbot API Documentation
**Version**: 1.0.0  
**Base URL**: `https://localhost:8004`

## Table of Contents
1. [Authentication](#authentication)
2. [Client Examples](#client-examples)
3. [Error Handling](#error-handling) 
4. [Interactive Docs](#interactive-documentation)
5. [Endpoint Reference](#endpoint-reference)

## Authentication
```markdown
### JWT Token Flow
1. Request token from `/token` endpoint
2. Include in headers: `Authorization: Bearer <token>`
3. Tokens expire after 30 minutes

### Example Request
```bash
curl -k -X POST https://localhost:8004/token \
  -d "username=testuser&password=mypassword" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

## Client Examples
### Python
```python
# Configuration
session = requests.Session()
session.verify = False  # Dev only - remove in production
session.headers = {"Authorization": f"Bearer {token}"}

# Example API Call
response = session.get("https://localhost:8004/users/")
```

### JavaScript
```javascript
// Using Axios
const api = axios.create({
  baseURL: 'https://localhost:8004',
  httpsAgent: new https.Agent({ rejectUnauthorized: false }) // Dev only
});
```

## Error Handling
| Code | Error | Solution |
|------|-------|----------|
| 401 | Unauthorized | Check token validity |
| 429 | Rate Limited | Wait 1 minute between requests |

## Interactive Documentation
Access Swagger UI at: `https://localhost:8004/docs`

### Recommended Screenshots:
1. Authentication section
2. User management endpoints  
3. Example requests/responses

## Endpoint Reference
### `POST /token`
- Authentication endpoint
- Returns JWT token
- Rate limited (5 requests/minute)

### `GET /users`
- Returns all users
- Requires valid JWT token