from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "user"

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Bot schemas
class BotBase(BaseModel):
    name: str
    description: Optional[str] = None
    personality: Optional[str] = "neutral"

class BotCreate(BotBase):
    pass

class BotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[str] = None

class Bot(BotBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

# Script schemas
class ScriptBase(BaseModel):
    content: str

class ScriptCreate(ScriptBase):
    bot_id: int

class Script(ScriptBase):
    id: int
    bot_id: int
    class Config:
        orm_mode = True

# Message schemas
class MessageBase(BaseModel):
    content: str
    is_from_user: bool

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

# Conversation schemas
class ConversationBase(BaseModel):
    platform: str
    user_id: str

class ConversationCreate(ConversationBase):
    bot_id: int

class Conversation(ConversationBase):
    id: int
    bot_id: int
    messages: List[Message] = []
    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Training response
class TrainingResult(BaseModel):
    bot_id: int
    status: str
    personality_profile: dict
    trained_at: datetime = datetime.now()