from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# Pydantic model
class UserCreate(BaseModel):
    username: str
    email: str

# FastAPI app
app = FastAPI()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.post("/users/")
async def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/")
async def root():
    return {
        "message": "Minimal Chatbot API working", 
        "endpoints": {
            "create_user": {"method": "POST", "path": "/users/", "body": {"username": "string", "email": "string"}},
            "get_user": {"method": "GET", "path": "/users/{user_id}"},
            "test_data": {"method": "GET", "path": "/test-user/"}
        }
    }

@app.get("/test-user/")
async def test_user(db: SessionLocal = Depends(get_db)):
    """Test endpoint that creates and returns a sample user"""
    test_user = User(username="testuser", email="test@example.com")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    return test_user
