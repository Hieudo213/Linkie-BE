from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.conversation import get_conversations
from app.schemas.conversation import ConversationOut
from app.core.database import get_db

router = APIRouter()

@router.get("/conversations/{user_id}", response_model=list[ConversationOut])
def get_conversations_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    Lấy tất cả các cuộc trò chuyện của người dùng
    """
    conversations = get_conversations(db, user_id)
    
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found")
    
    return conversations
