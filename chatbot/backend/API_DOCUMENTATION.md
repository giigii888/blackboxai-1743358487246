# Chatbot API Documentation

## Base URL
`https://localhost:8004`

## Authentication
- JWT Token required for protected endpoints
- Obtain token via `/token` endpoint
- Include in headers: `Authorization: Bearer <token>`

## Endpoints

### Authentication
`POST /token`
- Request form-data:
  - username
  - password
- Returns: 
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

### Users
`POST /users/`
- Creates new user
- Request body:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```

`GET /users/`
- Returns all users (protected)

[More endpoint documentation...]

## Examples

```bash
# Get token
curl -k -X POST https://localhost:8004/token \\
  -d "username=testuser&password=mypassword" \\
  -H "Content-Type: application/x-www-form-urlencoded"

# Access protected endpoint
curl -k https://localhost:8004/users/ \\
  -H "Authorization: Bearer <token>"