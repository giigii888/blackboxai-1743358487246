from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
import models
import schemas
from routers.auth import router as auth_router
from routers.bots import router as bots_router
from routers.scripts import router as scripts_router
from routers.social_media import router as social_media_router

app = FastAPI(title="AI Chatbot API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(bots_router)
app.include_router(scripts_router)
app.include_router(social_media_router)

@app.on_event("startup")
async def startup():
    models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}