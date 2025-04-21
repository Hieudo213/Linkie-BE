# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
# from sqlalchemy.orm import Session
# from app.core.websocket import manager
# from app.schemas.chat import MessageCreate
# from app.crud.chat import create_message
# from app.core.database import get_db

# router = APIRouter()

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: int):
#     await manager.connect(user_id, websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#             db: Session = next(get_db())

#             message = MessageCreate(**data)
#             saved_message = create_message(db, message)

#             await manager.send_personal_message(saved_message.__dict__, message.receiver_id)
#     except WebSocketDisconnect:
#         manager.disconnect(user_id)



# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
# from sqlalchemy.orm import Session
# from app.core.websocket import manager
# from app.schemas.chat import MessageCreate, MessageResponse
# from app.crud.chat import create_message
# from app.core.database import get_db

# router = APIRouter()

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
#     await manager.connect(user_id, websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()

#             message = MessageCreate(**data)
#             saved_message = create_message(db, message)

#             # Nếu muốn gửi lại phản hồi có định dạng JSON đúng, dùng pydantic
#             response_message = MessageResponse.from_orm(saved_message)

#             await manager.send_personal_message(response_message.dict(), message.receiver_id)
#     except WebSocketDisconnect:
#         manager.disconnect(user_id)



# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from app.core.connection_manager import manager
# from app.crud import chat as crud_chat
# from app.schemas.chat import MessageCreate
# import json

# router = APIRouter()

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: int):
#     await manager.connect(user_id, websocket)

#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(f"📥 Received from user {user_id}: {data}")

#             try:
#                 json_data = json.loads(data)
#                 message = MessageCreate(**json_data)

#                 # Lưu vào database
#                 await crud_chat.create_message(message)

#                 # Gửi cho người nhận
#                 await manager.send_personal_message(message.dict(), message.receiver_id)

#             except Exception as e:
#                 print(f"❌ Error handling message from user {user_id}: {e}")

#     except WebSocketDisconnect:
#         manager.disconnect(user_id)


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

