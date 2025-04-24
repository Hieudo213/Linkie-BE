from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"✅ User {user_id} connected. Active users: {list(self.active_connections.keys())}")

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)
        print(f"❌ User {user_id} disconnected. Active users: {list(self.active_connections.keys())}")

    async def send_personal_message(self, message: dict, user_id: int):
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_json(message)
                print(f"📤 Sent message to user {user_id}: {message}")
            except Exception as e:
                print(f"❌ Error sending message to user {user_id}: {e}")
                self.disconnect(user_id)

    async def send_notification(self, user_id: int, data: dict):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(data)
    
    

manager = ConnectionManager()
