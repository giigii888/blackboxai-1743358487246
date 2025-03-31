from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint with guaranteed proper JSON formatting"""
    return {
        "message": "Chatbot API with Authentication",
        "endpoints": {
            "login": {"method": "POST", "path": "/token"},
            "create_user": {"method": "POST", "path": "/users/"},
            "list_users": {"method": "GET", "path": "/users/"},
            "get_user": {"method": "GET", "path": "/users/{user_id}"},
            "update_user": {"method": "PUT", "path": "/users/{user_id}"},
            "delete_user": {"method": "DELETE", "path": "/users/{user_id}"}
        }
    }

@app.get("/test-json")
async def test_json():
    """Validation endpoint for JSON formatting"""
    return json.dumps({
        "status": "success",
        "message": "This JSON is properly formatted",
        "details": {
            "example": "value",
            "count": 1,
            "valid": True
        }
    })