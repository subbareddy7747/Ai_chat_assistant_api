# app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

# -------- AUTH SCHEMAS --------


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# -------- TOKEN SCHEMA --------


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


# -------- CHAT SCHEMAS --------


class ChatCreate(BaseModel):
    message: str


class ChatResponse(BaseModel):
    chat_id: int
    user_message: str
    ai_response: str
    timestamp: datetime


class ChatHistoryResponse(BaseModel):
    total: int
    chats: List[ChatResponse]
