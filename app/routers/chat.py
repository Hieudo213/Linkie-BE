from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.chat import MessageCreate
from app.crud import chat as crud_chat
from app.core.connection_manager import manager  # bạn tự điều chỉnh đường dẫn
import json

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: AsyncSession = Depends(get_db)):
    await manager.connect(user_id, websocket)
    print(f"✅ User {user_id} connected. Active users: {list(manager.active_connections.keys())}")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📥 Received from user {user_id}: {data}")
            try:
                json_data = json.loads(data)
                message = MessageCreate(**json_data)

                # Lưu vào DB
                crud_chat.create_message(db, message)

                # Gửi realtime cho người nhận
                await manager.send_personal_message(message.dict(), message.receiver_id)

            except Exception as e:
                print(f"❌ Error handling message from user {user_id}: {e}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"⚠️ User {user_id} disconnected. Active users: {list(manager.active_connections.keys())}")

# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.database import get_db
# from app.schemas.chat import MessageCreate
# from app.crud import chat as crud_chat
# from app.core.connection_manager import manager
# from app.models.notification import Notification
# from datetime import datetime
# import asyncio
# import json

# router = APIRouter()

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: int, db: AsyncSession = Depends(get_db)):
#     await manager.connect(user_id, websocket)
#     print(f"✅ User {user_id} connected. Active users: {list(manager.active_connections.keys())}")
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(f"📥 Received from user {user_id}: {data}")
#             try:
#                 json_data = json.loads(data)
#                 message = MessageCreate(**json_data)

#                 # # Lưu tin nhắn vào DB
#                 # saved_message = await crud_chat.create_message(db, message)

#                 # # Gửi tin nhắn realtime cho người nhận
#                 # await manager.send_personal_message(message.dict(), message.receiver_id)
#                 saved_message = await crud_chat.create_message(db, message)
#                 await manager.send_personal_message(message.receiver_id, saved_message.dict())

#                 # 👇 Thêm phần tạo và gửi thông báo
#                 title = "Tin nhắn mới"
#                 content = f"Bạn vừa nhận được tin nhắn từ người dùng {message.sender_id}"

#                 noti = Notification(
#                     user_id=message.receiver_id,
#                     title=title,
#                     content=content,
#                     created_at=datetime.utcnow()
#                 )
#                 db.add(noti)
#                 await db.commit()
#                 await db.refresh(noti)

#                 notification_data = {
#                     "title": noti.title,
#                     "content": noti.content,
#                     "created_at": str(noti.created_at)
#                 }

#                 # Gửi WebSocket thông báo nếu người nhận đang online
#                 asyncio.create_task(manager.send_personal_message(notification_data, message.receiver_id))

#             except Exception as e:
#                 print(f"❌ Error handling message from user {user_id}: {e}")
#     except WebSocketDisconnect:
#         manager.disconnect(user_id)
#         print(f"⚠️ User {user_id} disconnected. Active users: {list(manager.active_connections.keys())}")
