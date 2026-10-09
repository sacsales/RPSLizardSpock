import math 
import cv2
import mediapipe as mp
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision

font = cv2.FONT_HERSHEY_SIMPLEX

print("MediaPipe version:", mp.__version__)
print("OpenCV version:", cv2.__version__)


base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)
#setup the hand tracking stuff


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
#setup webcam/window frame

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
#find distance between 2 joint points



def find_origin(frame, landmark):
    h, w = frame.shape[:2]
    return int(landmark.x * w), int (landmark.y * h)



def draw_hand(frame, landmarks):
    h, w = frame.shape[:2]
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks] #map image coords to pixel coords


    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, points[a], points[b], (0, 255, 0), 2) #draw lines

    
    for p in points:
        cv2.circle(frame, p, 4, (0, 0, 255), -1)
        origin = (p[0] + 6, p[1] + 4)
        #cv2.putText(frame, str(p), origin, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA) to label coords 
        #red dots on the joints
    

 

def finger_up(name, finger_tip, finger_mid):
    wrist = single_hand_landmarks[5]

    tip_to_mid = dist(finger_tip, finger_mid)
    tip_to_base = dist(finger_tip, wrist)

    if tip_to_base > tip_to_mid:
        status = "up"
    else:
        status = "down"

    return status 
#check if a finger is fully extended. is distance between 



while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # fix colors
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    # detect hand landmarks from the input image
    result = detector.detect(mp_image)

    if result.hand_landmarks: #landmarks detected??
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
                    #cv2.putText(frame, f"{name}: {status} ", origin, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)


                pointer_tip = single_hand_landmarks[8]
                thumb_tip = single_hand_landmarks[4]
                middle_tip = single_hand_landmarks[12]
                ring_tip = single_hand_landmarks[16]

                tip_array = [pointer_tip, thumb_tip, middle_tip, ring_tip]


                pointerOrigin = (int(pointer_tip.x * w), int (pointer_tip.y * h))
                thumbOrigin = (int(thumb_tip.x * w), int (thumb_tip.y * h))

                mid_joint = single_hand_landmarks[11]
                ring_joint = single_hand_landmarks[15]


                cv2.line(frame, find_origin(frame, mid_joint), find_origin(frame, ring_joint), (0, 255, 0), 2)


                cv2.line(frame, pointerOrigin, thumbOrigin, (0, 255, 0), 2)
                thumb_pointer_dist = dist(pointer_tip, thumb_tip)
                mid_ring_dist = dist(mid_joint, ring_joint)
               

                #cv2.putText(frame, str(mid_ring_dist), find_origin(frame, mid_joint), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

                SPOCK_MID_RING_THRESHOLD = 0.09
                SPOCK_THUMB_POINTER_THRESHOLD = 0.20
                LIZARD_THUMB_POINTER_THRESHOLD = 0.10
                LIZARD_MID_RING_THRESHOLD = 0.05

                if mid_ring_dist > SPOCK_MID_RING_THRESHOLD and thumb_pointer_dist > SPOCK_THUMB_POINTER_THRESHOLD:
                    spockStatus = "spock"
                else:
                    spockStatus = "not spock"


                if thumb_pointer_dist > LIZARD_THUMB_POINTER_THRESHOLD and  mid_ring_dist < LIZARD_MID_RING_THRESHOLD:
                    lizardStatus = "lizard"
                else:
                    lizardStatus = "not lizard"

                

                


                cv2.putText(frame, spockStatus, (100,100), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, f"thumb pointer dist: {thumb_pointer_dist}", (100,150), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, lizardStatus, (100,200), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, f"mid ring dist: {mid_ring_dist}", (100,250), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

                











                





     

    cv2.imshow("window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#cleanup 
cap.release()
cv2.destroyAllWindows()
print("end")





