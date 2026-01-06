import cv2
import mediapipe as mp


f_mesh = mp.solutions.face_mesh


face_tool = f_mesh.FaceMesh(refine_landmarks=True)


cam = cv2.VideoCapture(0)


current_status = "Scanning..."

while True:
    ret, frame = cam.read()
    if not ret:
        break

    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    op = face_tool.process(frame_rgb)

    if op.multi_face_landmarks:
        
        points = op.multi_face_landmarks[0].landmark

        
        b_gap = abs(points[70].x - points[300].x)
        
        
        left_e = abs(points[159].y - points[145].y)
        right_e = abs(points[386].y - points[374].y)
        eye_avg = (left_e + right_e) / 2

        
        if b_gap < 0.22 and eye_avg < 0.014:
            current_status = "Confusion Detected!"
            my_color = (0, 0, 255) 
        else:
            current_status = "All Good"
            my_color = (0, 255, 0) 

       
        cv2.putText(frame, f"Status: {current_status}", (20, 40), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, my_color, 2)
    else:
        cv2.putText(frame, "Face Not Found", (20, 40), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 2)

    
    cv2.imshow('My Confusion Tracker', frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

