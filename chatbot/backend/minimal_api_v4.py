from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Authentication config
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock user database (replace with real database in production)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": pwd_context.hash("testpassword"),
    }
}

# Authentication utilities
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/")
async def create_user(user_data: dict, current_user: str = Depends(get_current_user)):
    """Create a new user (admin only)"""
    if current_user["username"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create users"
        )
    # In a real implementation, you would:
    # 1. Validate user_data
    # 2. Hash password
    # 3. Store in database
    return {"message": "User created", "data": user_data}

@app.get("/users/{user_id}")
async def read_user(user_id: int, current_user: str = Depends(get_current_user)):
    """Get a specific user's details"""
    # Mock implementation - replace with database lookup
    if user_id == 1:
        return {"id": 1, "username": "testuser", "email": "test@example.com"}
    elif user_id == 2:
        return {"id": 2, "username": "admin", "email": "admin@example.com"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@app.put("/users/{user_id}")
async def update_user(
    user_id: int, 
    user_data: dict,
    current_user: str = Depends(get_current_user)
):
    """Update a user's information"""
    # Verify permissions
    if current_user["username"] != "admin" and str(user_id) != current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update your own account"
        )
    # Mock implementation
    return {"message": f"User {user_id} updated", "data": user_data}

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: str = Depends(get_current_user)
):
    """Delete a user"""
    if current_user["username"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete users"
        )
    # Mock implementation
    return {"message": f"User {user_id} deleted"}

@app.get("/users/")
async def read_users(current_user: str = Depends(get_current_user)):
    """Protected endpoint - returns list of users"""
    return {
        "users": [
            {"username": "testuser", "email": "test@example.com"},
            {"username": "admin", "email": "admin@example.com"}
        ]
    }

@app.get("/test-json")
async def test_json():
    """Validation endpoint for JSON formatting"""
    return json.loads('''{
        "status": "success",
        "message": "This JSON is properly formatted",
        "details": {
            "example": "value",
            "count": 1,
            "valid": true
        }
    }''')