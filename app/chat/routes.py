# app/chat/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app import models, schemas
from app.chat.llm import call_llm

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post(
    "", response_model=schemas.ChatResponse, status_code=status.HTTP_200_OK
)
def create_chat(
    payload: schemas.ChatCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1. Call LLM safely
    try:
        ai_response = call_llm(payload.message)
    except Exception:
        ai_response = "Sorry, the AI service is currently unavailable."

    # 2. Store chat in database
    chat = models.Chat(
        user_id=current_user.id,
        user_message=payload.message,
        ai_response=ai_response,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    # 3. Return response
    return {
        "chat_id": chat.id,
        "user_message": chat.user_message,
        "ai_response": chat.ai_response,
        "timestamp": chat.timestamp,
    }


@router.get(
    "/history",
    response_model=schemas.ChatHistoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_chat_history(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    chats = (
        db.query(models.Chat)
        .filter(models.Chat.user_id == current_user.id)
        .order_by(models.Chat.timestamp.desc())
        .all()
    )

    return {
        "total": len(chats),
        "chats": [
            {
                "chat_id": chat.id,
                "user_message": chat.user_message,
                "ai_response": chat.ai_response,
                "timestamp": chat.timestamp,
            }
            for chat in chats
        ],
    }


@router.get(
    "/{chat_id}",
    response_model=schemas.ChatResponse,
    status_code=status.HTTP_200_OK,
)
def get_chat_by_id(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    chat = (
        db.query(models.Chat)
        .filter(
            models.Chat.id == chat_id, models.Chat.user_id == current_user.id
        )
        .first()
    )

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    return {
        "chat_id": chat.id,
        "user_message": chat.user_message,
        "ai_response": chat.ai_response,
        "timestamp": chat.timestamp,
    }


@router.delete("/{chat_id}", status_code=status.HTTP_200_OK)
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    chat = (
        db.query(models.Chat)
        .filter(
            models.Chat.id == chat_id, models.Chat.user_id == current_user.id
        )
        .first()
    )

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    db.delete(chat)
    db.commit()

    return {"message": "Chat deleted successfully"}
