from fastapi import APIRouter, Depends, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import json
import logging
import models
import schemas
from database import get_db
from training import ChatbotTrainer
from auth import get_current_active_user

router = APIRouter(
    prefix="/api/social",
    tags=["social"],
    dependencies=[Depends(get_current_active_user)]
)

# Common webhook verification for all platforms
async def verify_webhook(
    request: Request,
    platform: str,
    bot_id: int,
    db: Session = Depends(get_db)
):
    """Verify webhook signature and bot access"""
    # Get bot from database
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Platform-specific verification logic would go here
    # For now, we'll just log the incoming request
    body = await request.body()
    logging.info(f"Incoming {platform} webhook for bot {bot_id}: {body.decode()}")

    return bot

@router.post("/{platform}/webhook/{bot_id}")
async def handle_webhook(
    platform: str,
    bot_id: int,
    request: Request,
    db: Session = Depends(get_db),
    x_signature: Optional[str] = Header(None)
):
    """Handle incoming messages from social platforms"""
    try:
        # Verify webhook and get bot
        bot = await verify_webhook(request, platform, bot_id, db)
        
        # Parse incoming message based on platform
        if platform == "whatsapp":
            return await handle_whatsapp(request, bot, db)
        elif platform == "telegram":
            return await handle_telegram(request, bot, db)
        elif platform == "instagram":
            return await handle_instagram(request, bot, db)
        elif platform == "discord":
            return await handle_discord(request, bot, db)
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")
    
    except Exception as e:
        logging.error(f"Webhook handling failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_whatsapp(request: Request, bot: models.Bot, db: Session):
    """Process WhatsApp messages"""
    body = await request.json()
    message = body.get("messages", [{}])[0].get("text", {}).get("body", "")
    sender = body.get("messages", [{}])[0].get("from", "")
    
    # Create conversation if it doesn't exist
    conversation = db.query(models.Conversation).filter(
        models.Conversation.platform == "whatsapp",
        models.Conversation.user_id == sender,
        models.Conversation.bot_id == bot.id
    ).first()
    
    if not conversation:
        conversation = models.Conversation(
            platform="whatsapp",
            user_id=sender,
            bot_id=bot.id
        )
        db.add(conversation)
        db.commit()
    
    # Save incoming message
    db_message = models.Message(
        content=message,
        is_from_user=True,
        conversation_id=conversation.id
    )
    db.add(db_message)
    db.commit()
    
    # Generate response
    trainer = ChatbotTrainer(bot.id)
    trainer.load_training_data(db)
    response = trainer.generate_response(message)
    
    # Save bot response
    db_message = models.Message(
        content=response,
        is_from_user=False,
        conversation_id=conversation.id
    )
    db.add(db_message)
    db.commit()
    
    return JSONResponse(content={
        "messages": [{
            "from": bot.id,
            "to": sender,
            "text": {"body": response}
        }]
    })

async def handle_telegram(request: Request, bot: models.Bot, db: Session):
    """Process Telegram messages"""
    body = await request.json()
    message = body.get("message", {}).get("text", "")
    chat_id = body.get("message", {}).get("chat", {}).get("id", "")
    
    # Similar conversation handling as WhatsApp
    # Would implement Telegram-specific logic here
    
    return JSONResponse(content={
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": "Telegram response placeholder"
    })

async def handle_instagram(request: Request, bot: models.Bot, db: Session):
    """Process Instagram messages"""
    body = await request.json()
    # Instagram-specific message parsing would go here
    return JSONResponse(content={"status": "ok"})

async def handle_discord(request: Request, bot: models.Bot, db: Session):
    """Process Discord messages"""
    body = await request.json()
    # Discord-specific message parsing would go here
    return JSONResponse(content={"type": 1})  # ACK ping