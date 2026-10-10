#todo: score tracking, box around hand + timer, make it pretty, README 

import math 
import cv2
import mediapipe as mp
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision
import time
import random

RANDOM_MIN = 0
RANDOM_MAX = 3


start_time = time.time()
timer_value = 0
last_pose = None 
verified_pose = None 

round = 0 

font = cv2.FONT_HERSHEY_SIMPLEX

print("MediaPipe version:", mp.__version__)
print("OpenCV version:", cv2.__version__)


base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)
#setup the hand tracking stuff


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
#setup webcam/window frame...

#for the skeleton - which hand landmarks map to which? 
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),         # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),         # pointer
    (5, 9), (9, 10), (10, 11), (11, 12),    # middle
    (9, 13), (13, 14), (14, 15), (15, 16),  # ring
    (13, 17), (17, 18), (18, 19), (19, 20), # pinky
    (0, 17),                                # palm edge
]


SPOCK_MID_RING_THRESHOLD = 0.09
SPOCK_THUMB_POINTER_THRESHOLD = 0.20
LIZARD_THUMB_POINTER_THRESHOLD = 0.10
LIZARD_MID_RING_THRESHOLD = 0.05

POSE_TIMER_VALUE = 2.0

def dist(a, b):
    #find distance between 2 joint points
    return math.hypot(a.x - b.x, a.y - b.y)

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



    
def finger_up(single_hand_landmarks, finger_tip, finger_mid):
    #open: if tip->wrist greater than mid->wrist
    wrist = single_hand_landmarks[0]

    tip_to_base = dist(finger_tip, wrist)
    mid_to_base = dist(finger_mid, wrist)

    if tip_to_base > mid_to_base:
        status = "up"
    else:
        status = "down"

    return status 

def get_finger_array(single_hand_landmarks): 
    #returns array of four fingers and if they're up/down
    finger_array = [
        ["pointer", 7, 6],
        ["middle", 11, 10],
        ["ring", 15, 14],
        ["pinky", 19, 18],
    ]
    #finger name, tip, and middle joint

    finger_status_array = [None, None, None, None]


    for i in range(len(finger_array)):
        finger = finger_array[i]
        name = finger[0]
        tip = single_hand_landmarks[finger[1]]
        mid = single_hand_landmarks[finger[2]]
        status = finger_up(single_hand_landmarks, tip, mid)

        #h, w = frame.shape[:2]
        #origin = (int(tip.x * w), int (tip.y * h))
        finger_status_array[i] = status

        #cv2.putText(frame, f"{name}: {status} ", origin, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

    return finger_status_array

def is_spock(single_hand_landmarks):

    finger_status_array = get_finger_array(single_hand_landmarks)

    if finger_status_array == ["up", "up", "up", "up"]:
        all_up = True 
    else:
        all_up = False 

    pointer_tip = single_hand_landmarks[8]
    thumb_tip = single_hand_landmarks[4]
    middle_tip = single_hand_landmarks[12]
    ring_tip = single_hand_landmarks[16]

    mid_joint = single_hand_landmarks[11]
    ring_joint = single_hand_landmarks[15]

    
    thumb_pointer_dist = dist(pointer_tip, thumb_tip)
    mid_ring_dist = dist(mid_joint, ring_joint)
    mid_pointer_dist = dist(middle_tip, pointer_tip)

    if (mid_ring_dist > SPOCK_MID_RING_THRESHOLD) and (thumb_pointer_dist > SPOCK_THUMB_POINTER_THRESHOLD) and all_up and (mid_pointer_dist < mid_ring_dist):
        spockStatus = True
    else:
        spockStatus = False


    return spockStatus

def is_lizard(single_hand_landmarks):

    pointer_tip = single_hand_landmarks[8]
    thumb_tip = single_hand_landmarks[4]

    mid_joint = single_hand_landmarks[11]
    ring_joint = single_hand_landmarks[15]


    thumb_pointer_dist = dist(pointer_tip, thumb_tip)
    mid_ring_dist = dist(mid_joint, ring_joint)

    if thumb_pointer_dist > LIZARD_THUMB_POINTER_THRESHOLD and  mid_ring_dist < LIZARD_MID_RING_THRESHOLD:
        lizardStatus = True
    else:
        lizardStatus = False

    return lizardStatus

def is_rock(single_hand_landmarks):
    finger_status_array = get_finger_array(single_hand_landmarks)

    if finger_status_array == ["down", "down", "down", "down"]:
        return True
    return False

def is_paper(single_hand_landmarks):
    finger_status_array = get_finger_array(single_hand_landmarks)

    if finger_status_array == ["up", "up", "up", "up"]:
        return True
    return False

def is_scissors(single_hand_landmarks):
    finger_status_array = get_finger_array(single_hand_landmarks)

    if finger_status_array == ['up', 'up', 'down', 'down']:
        return True
    return False

def fight(p1, p2):
    """
    This function makes a one-way comparison of the moves of the first against the second player
    and assigns and returns the result if the combination is found:
    ie, "Scissors cuts paper..."

    Parameters:
        * p1 (string): player 1's move
        * p2 (string): player 2's move

    Return:
        * result (string): The 'ruling' of the comparisons of the different moves. Empty string if
        specific combination is not found.
    """
    result = ""
    if p1 == p2:
        result = "Draw"
    elif (p1 == "scissors") and (p2 == "paper"):
        result = "Scissors cuts paper..."
    elif (p1 == "paper") and (p2 == "rock"):
        result = "paper covers Rock"
    elif (p1 == "rock") and (p2 == "lizard"):
        result = "Rock crushes Lizard..."
    elif (p1 == "lizard") and (p2 == "spock"):
        result = "Lizard poisons Spock..."
    elif (p1 == "spock") and (p2 == "scissors"):
        result = "Spock smashes Scissors..."
    elif (p1 == "scissors") and (p2 == "lizard"):
        result = "Scissors decapitate Lizard..."
    elif (p1 == "lizard") and (p2 == "paper"):
        result = "Lizard eats Paper..."
    elif (p1 == "paper") and (p2 == "spock"):
        result = "Paper disproves Spock..."
    elif (p1 == "spock") and (p2 == "rock"):
        result = "Spock vaporizes Rock..."
    elif (p1 == "rock") and (p2 == "scissors"):
        result = "(and as it always has) Rock crushes Scissors!"

    return result

def double_check(p1, p2):
    """
    If the first 'pass' of comparison returned an empty string (no move combination matches),
    this function does the comparison again, but with the order reversed:
    ie, compares second player's move to the first player's.

    Parameters:
        * p1 (string): player 1's move
        * p2 (string): player 2's move

    Return:
        * winner (string): returns which player won this round - or draw, if applicable.
    """
    winner = ""

    if fight(p1, p2) == "Draw":
        winner = "Draw! No points awarded."
    elif fight(p1,p2) != "":
        print(fight(p1, p2))
        winner = "User"
    else: #switch
        print(fight(p2, p1))
        winner = "CPU"
    return winner

def find_reason(p1, p2):
    if fight(p1, p2) == "Draw":
        reason = "Draw!"
    elif fight(p1,p2) != "":
        reason = fight(p1, p2)
    else: #switch
        reason = fight(p2, p1)
        
    return reason

def translate_choice(choice):
    """
    This function 'translates' an integer into the corresponding move.

    Parameters:
        * choice (integer) from 0-4, denoting a specific move
    Return:
        * translated (string) of the actual name of the move: ie, paper, or scissors.
    """
    translated = ""
    if choice == 0:
        translated = "rock"
    elif choice == 1:
        translated = "paper"
    elif choice == 2:
        translated = "scissors"
    elif choice == 3:
        translated = "lizard"
    elif choice == 4:
        translated = "spock"

    return translated

def computer_choice():
    """
    This function generates the computer's move in that round, by generating a random number from 0-4 and translating
    it to the move it corresponds with.

    Parameters: None
    Return: cpu_choice (string): the computer's move that turn
    """
    cpu_choice = random.randint(RANDOM_MIN, RANDOM_MAX)
    cpu_choice = translate_choice(cpu_choice)
    return cpu_choice






def main(): 

    timer_value = 0
    last_pose = None 
    verified_pose = None
    round_played = False 

    red = (0,0,255)
    blue = (255,0,0)
    box_colour = red 
    
    while cap.isOpened():

        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        x_max = 0
        y_max = 0
        x_min = w
        y_min = h

        # fix colors
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # detect hand landmarks from the input image
        result = detector.detect(mp_image)

        current_time = time.time()

        if result.hand_landmarks: #landmarks detected??
            for single_hand_landmarks in result.hand_landmarks:  #result.hand_landmarks is different positions of hand.
                    draw_hand(frame, single_hand_landmarks) #single_hand_landmarks refers to an array of all the different joints in 1 hand pos...
                    for landmark in single_hand_landmarks:
                        x, y = int(landmark.x * w), int(landmark.y * h)

                        if x > x_max:
                            x_max = x
                        if x < x_min:
                            x_min = x
                        if y > y_max:
                            y_max = y
                        if y < y_min:
                            y_min = y

                    cv2.rectangle(frame, (x_min - 15, y_min - 15), (x_max + 15, y_max + 15), box_colour, 2) #hand box 
                    cv2.rectangle(frame, (x_min - 15, y_min - 15), (x_min + 100, y_min - 40), box_colour, -1) #detected label text bg
                    
                    
                    
                    #finger_status_array = get_finger_array(single_hand_landmarks)

                    pointer_tip = single_hand_landmarks[8]
                    thumb_tip = single_hand_landmarks[4]

                    mid_joint = single_hand_landmarks[11]
                    ring_joint = single_hand_landmarks[15]
                    #define needed joint names...

                    #tip_array = [pointer_tip, thumb_tip, middle_tip, ring_tip]

                    cv2.line(frame, find_origin(frame, mid_joint), find_origin(frame, ring_joint), (0, 255, 0), 2) #spock line
                    cv2.line(frame, find_origin(frame, pointer_tip), find_origin(frame, thumb_tip), (0, 255, 0), 2) #pointer -> thumb line 

                    #cv2.putText(frame, str(mid_ring_dist), find_origin(frame, mid_joint), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

                    current_pose = "-"


                    """

                    spockStatus = is_spock(single_hand_landmarks)
                    lizardStatus = is_lizard(single_hand_landmarks)
                    
                    Debug Text, uncomment to display some values 

                    cv2.putText(frame, f"spock: {spockStatus}", (0,100), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame, f"lizard: {lizardStatus}", (0,150), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                
                    cv2.putText(frame, str(finger_status_array), (0,200), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

                    
                    #cv2.putText(frame, f"thumb pointer dist: {thumb_pointer_dist}", (0,125), font, 0.4, (255, 0, 0), 1, cv2.LINE_AA)
                    #cv2.putText(frame, f"mid ring dist: {mid_ring_dist}", (0,175), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

                    """


                    if is_lizard(single_hand_landmarks):
                        current_pose = "lizard"
                    elif is_scissors(single_hand_landmarks):
                        current_pose = "scissors"
                    elif is_spock(single_hand_landmarks):
                        current_pose = "spock"
                    elif is_paper(single_hand_landmarks):
                        current_pose = "paper"
                    elif is_rock(single_hand_landmarks):
                        current_pose = "rock"
                    else:
                        current_pose = "unknown"

                    label = f"detecting: {current_pose}"

                    #run through possible poses, set the current pose

                    

                    if last_pose == current_pose: 
                        #if no change in pose, add to pose timer
                        if not round_played:
                            status = "Hold that pose!"
                            timer_value = current_time - timer_start 
                            label = f"detecting: {current_pose}"

                            if timer_value > POSE_TIMER_VALUE: #ie, player has held pose for long enough to play it
                                verified_pose = current_pose
                                label = verified_pose
                                box_colour = blue

                                user = verified_pose
                                cpu = computer_choice()
                                
                                verdict = find_reason(user, cpu)
                                winner = double_check(user, cpu)
                                
                                round_played = True   #'pause' for this round, don't run game logic again for a bit 
                                status = "Change pose to play again"

                        else:
                            label = verified_pose
                            #display round results...
                            cv2.putText(frame, f"CPU: {cpu}", (0,225), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
                            cv2.putText(frame, f"User: {user}", (0,250), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
                            cv2.putText(frame, f"{verdict}", (0,275), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
                            cv2.putText(frame, f"{winner} wins!", (0,300), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)


                        
                    else: 
                        #pose changed, clear everything, and make a new timer
                        verified_pose = ""
                        label = ""
                        box_colour = red
                        timer_value = 0
                        status = "Pick a pose..."
                        timer_start = current_time
                        round_played = False 

                    last_pose = current_pose #for comparison: did it change recently?
                    
                    #cv2.putText(frame, f"Detected Pose: {current_pose}", (0,50), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame, status, (0,50), font, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame, label, (x_min - 15, y_min - 15), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    #set hand box text
                    
        else:
            timer_value = 0 #reset timer if user's hand not visible anymore 

        
        #cv2.putText(frame, f"verified_pose: {verified_pose}", (0,75), font, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
        #cv2.putText(frame, str(current_time - start_time), (0,100), font, 1.0, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str(f"Held for: {timer_value:.2f}"), (0,25), font, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Rock, Paper, Scissors, Lizard, Spock", frame)

        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #user_choice = verified_pose


  


    #cleanup 
    cap.release()
    cv2.destroyAllWindows()
    print("end")


# This provided line is required at the end of a Python file
# to call the main() function.
if __name__ == '__main__':
    main()
