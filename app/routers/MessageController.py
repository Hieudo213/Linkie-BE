import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect
from app.core.database import get_db
from app.core.WebSocketConfig import ws_manager
from app.models.MessageModel import Message

router = APIRouter(
    tags=["Location"]
)


@router.websocket("/ws/chat/{user_id}")
async def websocket_chat_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await ws_manager.connect(websocket, user_id, conn_type="chat")  # ✅ RẤT QUAN TRỌNG

    try:
        while True:
            data = await websocket.receive_text()

            try:
                payload = json.loads(data)
                to_user_id = payload.get("to_user_id")
                content = payload.get("content")
                if not to_user_id or not content:
                    raise ValueError
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid message format")

            # Lưu vào DB
            new_message = Message(from_user_id=user_id, to_user_id=to_user_id, content=content)
            db.add(new_message)
            db.commit()

            # Gửi tin nhắn tới chat socket của người nhận
            await ws_manager.send_to(to_user_id, "chat", f"New message from {user_id}: {content}")

            # Gửi thông báo tới notification socket của người nhận
            await ws_manager.send_to(to_user_id, "notification", f"You have a new message from user {user_id}")

    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, "chat")


@router.websocket("/ws/notifications/{user_id}")
async def websocket_notification_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await ws_manager.connect(websocket, user_id, conn_type="notification")

    try:
        while True:
            await websocket.receive_text()  # hoặc dùng await asyncio.sleep(10)

    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, "notification")
