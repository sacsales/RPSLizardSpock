import math 
import cv2
import mediapipe as mp
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision


print("MediaPipe version:", mp.__version__)
print("OpenCV version:", cv2.__version__)


base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)


#for the skeleton - which hand landmarks map to which? 
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),         # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),         # index
    (5, 9), (9, 10), (10, 11), (11, 12),    # middle
    (9, 13), (13, 14), (14, 15), (15, 16),  # ring
    (13, 17), (17, 18), (18, 19), (19, 20), # pinky
    (0, 17),                                # palm edge
]


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def finger_extended(lm, tip, pip):
    return dist(lm[0], lm[tip]) > dist(lm[0], lm[pip])





def draw_hand(frame, landmarks):
    h, w = frame.shape[:2]
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks] #map image coords to pixel coords


    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, points[a], points[b], (0, 255, 0), 2) #draw lines

    
    for p in points:
        cv2.circle(frame, p, 4, (0, 0, 255), -1)
        origin = (p[0] + 6, p[1] + 4)
        #cv2.putText(frame, str(p), origin, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA) to label coords 
    

 #draw hand landmark points 

def finger_up(name, finger_tip, finger_mid):
    wrist = single_hand_landmarks[5]

    tip_to_mid = dist(finger_tip, finger_mid)
    tip_to_base = dist(finger_tip, wrist)

    if tip_to_base > tip_to_mid:
        status = "up"
    else:
        status = "down"

    return status 



while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert BGR -> RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    # Detect hand landmarks from the input image
    result = detector.detect(mp_image)

    if result.hand_landmarks:
         for single_hand_landmarks in result.hand_landmarks:  #result.hand_landmarks is different positions of hand.
                draw_hand(frame, single_hand_landmarks) #single_hand_landmarks refers to an array of all the different joints in 1 hand pos...

                finger_array = [
                    ["pointer", 8, 6],
                    ["middle", 12, 10],
                    ["ring", 16, 14],
                    ["pinky", 20, 18],
                ]

                #finger name, tip, and middle joint

                for finger in finger_array:
                    name = finger[0]
                    tip = single_hand_landmarks[finger[1]]
                    mid = single_hand_landmarks[finger[2]]
                    status = finger_up(name, tip, mid)

                    h, w = frame.shape[:2]
                    origin = (int(tip.x * w), int (tip.y * h))
                    cv2.putText(frame, f"{name}: {status} ", origin, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

                 












            

    cv2.imshow("window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()
print("end")





