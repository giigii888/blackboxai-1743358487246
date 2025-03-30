# Chatbot API Documentation

## Base URL
`https://localhost:8004` (Use `-k` flag with curl for self-signed certs)

## Authentication
- JWT Token required for protected endpoints
- Obtain via: `POST /token` with form-data:
  - `username`
  - `password`
- Include in headers: `Authorization: Bearer <token>`
- Token expires in 30 minutes

## Client Examples

### Python
```python
import requests

# Configure session
session = requests.Session()
session.verify = False  # Bypass SSL verification for dev

# Authenticate
auth_response = session.post(
    "https://localhost:8004/token",
    data={"username": "testuser", "password": "mypassword"}
)
token = auth_response.json()["access_token"]

# Set auth header
session.headers.update({"Authorization": f"Bearer {token}"})

# Call API
response = session.get("https://localhost:8004/users/")
print(response.json())
```

### JavaScript
```javascript
// Node.js example using axios
const axios = require('axios');
const https = require('https');

// Configure axios instance
const api = axios.create({
  baseURL: 'https://localhost:8004',
  httpsAgent: new https.Agent({  
    rejectUnauthorized: false // For self-signed certs
  })
});

// Authenticate and use API
async function getUsers() {
  try {
    const auth = await api.post('/token', 
      "username=testuser&password=mypassword",
      {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
    );
    
    api.defaults.headers.common['Authorization'] = `Bearer ${auth.data.access_token}`;
    const users = await api.get('/users/');
    console.log(users.data);
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
  }
}
```

## Error Handling
| Status Code | Error | Resolution |
|-------------|-------|------------|
| 400 | Bad Request | Check request body/parameters |
| 401 | Unauthorized | Provide valid JWT token |
| 404 | Not Found | Check endpoint URL |
| 429 | Too Many Requests | Wait and retry (5 requests/minute limit) |
| 500 | Server Error | Contact support |

## Example Requests

```bash
# Get token
curl -k -X POST https://localhost:8004/token \\
  -d "username=testuser&password=mypassword" \\
  -H "Content-Type: application/x-www-form-urlencoded"

# Access protected endpoint  
curl -k https://localhost:8004/users/ \\
  -H "Authorization: Bearer <token>"
```

## Endpoints
[Previous endpoint documentation...]