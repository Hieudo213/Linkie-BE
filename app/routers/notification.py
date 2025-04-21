from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.notification import NotificationOut
from app.crud import notification as crud_notification

router = APIRouter()


@router.get("/api/notifications")
def get_notification(
    index: int = Query(0),
    count: int = Query(10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = crud_notification.get_notifications(db, current_user.id, index, count)
    return {
        "code": "200",
        "message": "Lấy thông báo thành công",
        "notifications": [NotificationOut.from_orm(n) for n in notifications]
    }


@router.delete("/api/notifications/{id}")
def delete_notification(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = crud_notification.delete_notification(db, current_user.id, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Thông báo không tồn tại")
    return {
        "code": "200",
        "message": "Xóa thông báo thành công"
    }
