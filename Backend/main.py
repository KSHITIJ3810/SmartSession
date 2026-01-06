from fastapi import FastAPI, WebSocket
import uvicorn
import json, base64, asyncio
import cv2, numpy as np

from services.engine import check_eyes, analyze_confusion


from routes import student_router, teachers_router


app = FastAPI(title="StudentEngagementApp")

@app.get("/")
def home():
    return {"msg": "Backend is ok!"}


app.include_router(student_router, prefix="/student", tags=["Student"])
app.include_router(teachers_router, prefix="/teacher", tags=["Teacher"])


teacher_connections = []

@app.websocket("/ws/student")
async def student_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            payload = json.loads(data)

            
            frame = payload.get("image") or payload.get("frame")
            student_id = payload.get("id") or payload.get("student_id")

            img = None
            if isinstance(frame, str) and frame.startswith("data:"):
                try:
                    header, b64 = frame.split(',', 1)
                    img_bytes = base64.b64decode(b64)
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                except Exception as e:
                    print("Oops, image decode fail:", e)

            if img is not None:
                try:
                    gaze = await asyncio.to_thread(check_eyes, img)
                    raw_emotion = await asyncio.to_thread(analyze_confusion, img)
                    emotion = "Confused" if "Confused" in raw_emotion else raw_emotion
                except Exception as e:
                    print("Hmm, analysis crashed:", e)
                    gaze, emotion = "Unknown", "Neutral"
            else:
                gaze, emotion = "Unknown", "Neutral"

            result = {
                "student_id": student_id,
                "gaze": gaze,
                "emotion": emotion,
                "is_proctor_alert": False
            }

            
            for teacher in teacher_connections:
                await teacher.send_json(result)

            await websocket.send_text("Frame done processing")

        except Exception as e:
            print("Error in student_ws loop:", e)
            break

@app.websocket("/ws/teacher")
async def teacher_ws(websocket: WebSocket):
    await websocket.accept()
    teacher_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print("Teacher left:", e)
        teacher_connections.remove(websocket)

if __name__ == "__main__":
    print("Starting backend server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)