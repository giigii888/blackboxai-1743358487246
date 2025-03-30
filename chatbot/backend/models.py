from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    role = Column(String(20), default="user")  # 'admin' or 'user'

class Bot(Base):
    __tablename__ = "bots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    description = Column(Text)
    personality = Column(String(100))  # e.g., 'friendly', 'professional'
    owner_id = Column(Integer, ForeignKey("users.id"))
    scripts = relationship("Script", back_populates="bot")
    conversations = relationship("Conversation", back_populates="bot")

class Script(Base):
    __tablename__ = "scripts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    bot = relationship("Bot", back_populates="scripts")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(20))  # 'whatsapp', 'telegram', etc.
    user_id = Column(String(100))  # platform-specific user ID
    bot_id = Column(Integer, ForeignKey("bots.id"))
    bot = relationship("Bot", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    is_from_user = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    conversation = relationship("Conversation", back_populates="messages")