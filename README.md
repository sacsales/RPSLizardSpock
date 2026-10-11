# Rock, Paper, Scissors, Lizard, Spock!

## ℹ️ Overview


> This program simulates the slightly convoluted game 'Rock, Paper, Scissors, Lizard, Spock' that appears on the show the Big Bang Theory, using hand tracking from the user's webcam! Play against your computer. This uses OpenCV and Mediapipe for webcam and hand tracking. 

> For reference: https://www.youtube.com/watch?v=_PUEoDYpUyQ

```
 "Scissors cuts Paper,
 Paper covers Rock,
 Rock crushes Lizard,
 Lizard poisons Spock,
 Spock smashes Scissors,
 Scissors decapitates Lizard,
 Lizard eats Paper,
 Paper disproves Spock,
 Spock vaporizes Rock,
 (and as it always has) Rock crushes Scissors."
```

## Video Demo! 
https://github.com/user-attachments/assets/b63b49ac-f5db-43ce-9a7e-aa0e7bcb7b19


## ✍️ Authors
https://github.com/sacsales (me!)


## Hey, I wanna try it on my machine!
> Cool! There are 2 ways to do this: 

### Scenario 1: I know how to clone a repo! 
> If so, awesome! Please do that.

### Scenario 2: I have no idea what the above line means/don't feel like cloning a repo/ AND I have a Mac. 
> No problem, please follow the steps below:
1. Download the latest release from the releases tab on the right-hand side of this page. Click on 'main.zip'. It should download. Unzip it!
2. Open up Terminal. Navigate to the file you you just unzipped. To do this, type `cd` and enter the file path (you can also drag and drop the folder from your finder window!) Entire command should look a little something like this:
```cd /Users/yourname/Downloads/main```
4. Run this command next: `xattr -cr .` This avoids your Mac thinking it's a sketchy program. I swear it isn't, check the code (trust me bro)
5. Last one! Run `./main.` and wait for a bit. It might ask you for camera permissions - click yes. If nothing happens after about a minute, try running the last command again. 


## 🚀 Usage

Make a pose from Rock(✊), Paper (🤚), Scissors (✌️), Lizard (🤏) or Spock (🖖) to your webcam and hold it! CPU will randomly generate a response, and a round will be played. 

Having issues? Make sure you're in a well-lit area and try to keep your hand steady. If the pose detected keeps switching, try moving your hand closer/farther from the webcam until it stabilises. 

- OpenCV version: 5.0.0
- MediaPipe version: 1.1.0
- Python Version: 3.13.16

## Pose Guide


Rock (✊)
- Checks for all fingers down, with palm towards camera. 

Paper (🤚)
- Checks for all fingers up, with palm towards camera.

Scissors (✌️)
- Checks for pointer + Middle fingers up ONLY, like a peace sign! And palm towards camera.

Lizard (🤏)
- Turn your hand to the side and make a 'C' shape. Checks for clustered fingertips + a certain distance from pointer to thumb.

Spock (🖖)
- Make a 'V'  with your middle and ring fingers, and make sure your thumb is pointed outwards. Checks for distance between ring and middle finger and distance from thumb to pointer tip. As always, palm towards camera.



## 💭 Feedback
Any ideas/comments? Say hi on discord. 

