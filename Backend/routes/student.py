from fastapi import APIRouter, WebSocket, UploadFile
import cv2
import numpy as np
from services.engine import check_eyes, analyze_confusion
from models import UserState
from datetime import datetime

router = APIRouter(prefix="/student", tags=["student"])

@router.post("/upload")
async def upload_video(file: UploadFile):
    # TODO: save file, run analysis
    return {"status": "received", "filename": file.filename}

@router.websocket("/ws")
async def student_ws(ws: WebSocket):
    await ws.accept()
    while True:
        
        data = await ws.receive_bytes()
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

       
        gaze_status = check_eyes(frame)
        emotion_status = analyze_confusion(frame)

       
        result = UserState(
            student_id="s123",
            look=gaze_status,
            mood=emotion_status,
            confused_val=1.0 if "Confusion" in emotion_status else 0.0,
            time=datetime.now()
        )

        await ws.send_json(result.dict())

