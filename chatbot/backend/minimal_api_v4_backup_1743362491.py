from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
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

# [Rest of your existing API code...]