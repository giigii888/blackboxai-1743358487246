from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
import models
import schemas
from database import get_db
from auth import get_current_active_user
from training import train_bot
import logging

router = APIRouter(
    prefix="/api/scripts",
    tags=["scripts"],
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/upload", response_model=schemas.Script)
async def upload_script(
    file: UploadFile = File(...),
    bot_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Upload a training script for a bot"""
    # Verify bot exists and user has access
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if current_user.role != "admin" and bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to upload scripts for this bot")

    try:
        # Read file content
        contents = await file.read()
        content_str = contents.decode("utf-8")

        # Create script record
        db_script = models.Script(
            content=content_str,
            bot_id=bot_id
        )
        db.add(db_script)
        db.commit()
        db.refresh(db_script)

        # Trigger training
        try:
            train_bot(bot_id, db)
        except Exception as e:
            logging.warning(f"Training failed after script upload: {str(e)}")

        return db_script

    except Exception as e:
        logging.error(f"Script upload failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Script upload failed: {str(e)}"
        )
    finally:
        await file.close()

@router.get("/", response_model=List[schemas.Script])
def read_scripts(
    bot_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List all scripts for a bot"""
    # Verify bot exists and user has access
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if current_user.role != "admin" and bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view scripts for this bot")

    scripts = db.query(models.Script).filter(
        models.Script.bot_id == bot_id
    ).offset(skip).limit(limit).all()
    return scripts

@router.delete("/{script_id}", response_model=schemas.Script)
def delete_script(
    script_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete a training script"""
    script = db.query(models.Script).filter(models.Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")

    # Verify bot exists and user has access
    bot = db.query(models.Bot).filter(models.Bot.id == script.bot_id).first()
    if current_user.role != "admin" and bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this script")

    db.delete(script)
    db.commit()

    # Retrain bot after script deletion
    try:
        train_bot(script.bot_id, db)
    except Exception as e:
        logging.warning(f"Training failed after script deletion: {str(e)}")

    return script