import cv2
import mediapipe as mp
import time


mp_mesh = mp.solutions.face_mesh
detector = mp_mesh.FaceMesh(refine_landmarks=True)


timer_start = time.time()
status = "Normal"

def check_eyes(img):
    global timer_start, status
    
    
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    op = detector.process(rgb_img)

    if not op.multi_face_landmarks:
        return "No Face Found"

    
    mark = op.multi_face_landmarks[0].landmark

    
    lx = (mark[474].x + mark[475].x + mark[476].x + mark[477].x) / 4
    rx = (mark[469].x + mark[470].x + mark[471].x + mark[472].x) / 4
    ly = (mark[474].y + mark[475].y + mark[476].y + mark[477].y) / 4

   
    side = "Forward"
    if lx < 0.42 and rx < 0.42:
        side = "Left"
    elif lx > 0.58 and rx > 0.58:
        side = "Right"
    elif ly < 0.42:
        side = "Up"

    
    if side == "Forward":
        timer_start = time.time() 
        return "Focused"
    else:
        wait_time = time.time() - timer_start
        if wait_time > 4:
            return f"ALERT: Looking {side}"
        else:
            return "Focused"


cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    msg = check_eyes(frame)
    cv2.putText(frame, msg, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Gaze Test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

