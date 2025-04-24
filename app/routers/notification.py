from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from app.core.connection_manager import manager
from app.schemas.notification import NotificationSchema
from app.crud import notification as crud_noti
from app.core.database import get_db
from typing import List

router = APIRouter()

@router.websocket("/ws/notifications/{user_id}")
async def websocket_notification(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        

@router.get("/api/notifications")
def get_notifications(
    user_id: int = Query(...),
    index: int = Query(0), 
    count: int = Query(20), 
    db: Session = Depends(get_db)
):
    notis = crud_noti.get_notifications(db, user_id, index, count)
    return {
        "code": "200",
        "message": "Lấy danh sách thông báo thành công",
        "notifications": notis
    }

@router.delete("/api/notifications/{noti_id}")
def delete_notification(noti_id: int, db: Session = Depends(get_db)):
    noti = crud_noti.delete_notification(db, noti_id)
    if not noti:
        return {"code": "404", "message": "Notification not found"}
    return {"code": "200", "message": "Deleted successfully"}
