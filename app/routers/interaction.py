from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.interaction import create_interaction
from app.schemas.interaction import InteractionOut
from app.core.database import get_db

from app.models.notification import Notification
from app.core.connection_manager import manager
import asyncio

from datetime import datetime

router = APIRouter()

@router.post("/interactions", response_model=InteractionOut)
async def create_like_or_dislike(
    user_id: int, profile_id: int, is_like: bool, db: Session = Depends(get_db)
):
    """
    API ghi nhận hành động swipe (like/dislike) và kiểm tra match
    """
    print("🌀 Nhận được request swipe:", user_id, profile_id, is_like)
    interaction = create_interaction(db, user_id, profile_id, is_like)

    # Nếu là LIKE thì gửi thông báo
    if is_like:
        title = "Bạn có lượt match mới"
        content = f"Người dùng {user_id} đã thích bạn"    
        # Thay bằng tên profile người gửi 

        noti = Notification(
            user_id=profile_id,
            title=title,
            content=content,
            created_at=datetime.utcnow()
        )
        db.add(noti)
        db.commit()
        db.refresh(noti)

        notification_data = {
            # "id": noti.id,
            "title": noti.title,
            "content": noti.content,
            "created_at": str(noti.created_at)
        }

        asyncio.create_task(manager.send_personal_message(notification_data, profile_id))

    return interaction



