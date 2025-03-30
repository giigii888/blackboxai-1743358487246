from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_active_user
from training import train_bot
import models
import schemas
import logging

router = APIRouter(
    prefix="/api/bots",
    tags=["bots"],
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=schemas.Bot)
def create_bot(
    bot: schemas.BotCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new chatbot instance"""
    db_bot = models.Bot(
        name=bot.name,
        description=bot.description,
        personality=bot.personality,
        owner_id=current_user.id
    )
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

@router.get("/", response_model=List[schemas.Bot])
def read_bots(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List all bots for current user"""
    if current_user.role == "admin":
        bots = db.query(models.Bot).offset(skip).limit(limit).all()
    else:
        bots = db.query(models.Bot).filter(models.Bot.owner_id == current_user.id).offset(skip).limit(limit).all()
    return bots

@router.get("/{bot_id}", response_model=schemas.Bot)
def read_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get details for a specific bot"""
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if current_user.role != "admin" and bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this bot")
    return bot

@router.put("/{bot_id}", response_model=schemas.Bot)
def update_bot(
    bot_id: int,
    bot: schemas.BotUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update bot configuration"""
    db_bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not db_bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if current_user.role != "admin" and db_bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this bot")
    
    update_data = bot.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bot, field, value)
    
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

@router.post("/{bot_id}/train", response_model=dict)
def train_bot_endpoint(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Train a bot using its assigned scripts"""
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if current_user.role != "admin" and bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to train this bot")
    
    try:
        personality_profile = train_bot(bot_id, db)
        return {
            "status": "success",
            "bot_id": bot_id,
            "personality_profile": personality_profile
        }
    except Exception as e:
        logging.error(f"Training failed for bot {bot_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Training failed: {str(e)}"
        )