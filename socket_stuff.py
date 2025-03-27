from typing import Dict, List, Optional
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, recipient_id: str):
        if recipient_id in self.active_connections:
            await self.active_connections[recipient_id].send_text(message)

    async def broadcast(self, message: str, sender_id: str):
        for uid, connection in self.active_connections.items():
            if uid != sender_id:
                await connection.send_text(message)

    def get_active_users(self):
        return list(self.active_connections.keys())