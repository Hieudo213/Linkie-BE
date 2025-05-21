from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.conversation import get_conversations, delete_conversation
from app.schemas.conversation import ConversationOut
from app.core.database import get_db

router = APIRouter()

@router.get("/conversations/{user_id}", response_model=list[ConversationOut])
def get_conversations_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    Lấy tất cả các cuộc hội thoại của người dùng
    """
    conversations = get_conversations(db, user_id)
    
    if not conversations:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc hội thoại")
    
    return conversations

@router.delete("/conversations/{conversation_id}")
def delete_conversation_by_id(conversation_id: int, db: Session = Depends(get_db)):
    """
    Xoá một cuộc trò chuyện theo ID
    """
    success = delete_conversation(db, conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc hội thoại")
    return {"detail": "Xóa cuộc hội thoại thành công"}
