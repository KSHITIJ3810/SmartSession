from typing import List, Dict
from fastapi import WebSocket
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.student_map: Dict[WebSocket, str] = {}
        self.last_update: datetime = datetime.now()   

    async def connect(self, ws: WebSocket, student_id: str = "None"):
        await ws.accept()
        self.active_connections.append(ws)
        if student_id:
            self.student_map[ws] = student_id
        self.last_update = datetime.now()

    def disconnect(self, ws: WebSocket):
        if ws in self.active_connections:
            self.active_connections.remove(ws)
        if ws in self.student_map:
            del self.student_map[ws]
        self.last_update = datetime.now()

    async def send_personal(self, msg: dict, ws: WebSocket):
        await ws.send_json(msg)

    async def broadcast(self, msg: dict):
        for ws in self.active_connections:
            try:
                await ws.send_json(msg)
            except:
                
                self.disconnect(ws)

    def active_students(self) -> List[str]:
        return list(self.student_map.values())

manager = ConnectionManager()