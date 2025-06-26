from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.MessageModel import Message
from app.core.database import get_db

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/history/")
def get_chat_history(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        ((Message.from_user_id == user1_id) & (Message.to_user_id == user2_id)) |
        ((Message.from_user_id == user2_id) & (Message.to_user_id == user1_id))
    ).order_by(Message.timestamp).all()

    return [
        {
            "from_user_id": m.from_user_id,
            "to_user_id": m.to_user_id,
            "content": m.content,
            "timestamp": m.timestamp.isoformat(),
        }
        for m in messages
    ]
