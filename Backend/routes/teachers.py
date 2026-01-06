

from fastapi import APIRouter, WebSocket
from models import TeacherInfo, SocketMsg
from websockets_manager import manager
from datetime import datetime

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.get("/status")
async def get_status():
    
    info = TeacherInfo(
        t_id="T001",
        students=manager.active_students(),   
        updated_at=manager.last_update or datetime.now()
    )
    return info

@router.websocket("/ws")
async def teacher_ws(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_json()
            msg = SocketMsg(**data)
            
    except Exception as e:
        print("Teacher WS error:", e)
    finally:
        manager.disconnect(ws)