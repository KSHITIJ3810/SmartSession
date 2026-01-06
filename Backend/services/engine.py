import cv2
import mediapipe as mp
import time


mp_face_mesh = mp.solutions.face_mesh
gaze_detector = mp_face_mesh.FaceMesh(refine_landmarks=True)
emo_detector = mp_face_mesh.FaceMesh(refine_landmarks=True)

gaze_timer = time.time()

def check_eyes(frame):
    global gaze_timer
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = gaze_detector.process(rgb)

    if not res.multi_face_landmarks:
        return "No Face"

    pts = res.multi_face_landmarks[0].landmark
    lx = (pts[474].x + pts[475].x + pts[476].x + pts[477].x) / 4
    rx = (pts[469].x + pts[470].x + pts[471].x + pts[472].x) / 4
    ly = (pts[474].y + pts[475].y + pts[476].y + pts[477].y) / 4

    side = "Forward"
    if lx < 0.42 and rx < 0.42:
        side = "Left"
    elif lx > 0.58 and rx > 0.58:
        side = "Right"
    elif ly < 0.42:
        side = "Up"

    if side == "Forward":
        gaze_timer = time.time()
        return "Focused"
    else:
        wait = time.time() - gaze_timer
        if wait > 4:
            return f"ALERT: {side}"
        else:
            return "Focused"

def analyze_confusion(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = emo_detector.process(rgb)

    if not res.multi_face_landmarks:
        return "No Face"

    pts = res.multi_face_landmarks[0].landmark
    b_gap = abs(pts[70].x - pts[300].x)
    le = abs(pts[159].y - pts[145].y)
    re = abs(pts[386].y - pts[374].y)
    eye_avg = (le + re) / 2

    if b_gap < 0.22 and eye_avg < 0.014:
        return "Confused!"
    else:
        return "OK"