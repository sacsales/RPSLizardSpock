# Rock, Paper, Scissors, Lizard, Spock!

## ℹ️ Overview


> This program simulates the slightly convoluted game 'Rock, Paper, Scissors, Lizard, Spock' that appears on the show the Big Bang Theory, using hand tracking from the user's webcam! Play against your computer. This uses OpenCV and Mediapipe for webcam and hand tracking. 


> For reference: https://www.youtube.com/watch?v=_PUEoDYpUyQ

- "Scissors cuts Paper,
- Paper covers Rock,
- Rock crushes Lizard,
- Lizard poisons Spock,
- Spock smashes Scissors,
- Scissors decapitates Lizard,
- Lizard eats Paper,
- Paper disproves Spock,
- Spock vaporizes Rock,
- (and as it always has) Rock crushes Scissors."


### ✍️ Authors

https://github.com/sacsales (me!)


## ⬇️ Installation

Clone the repo, open it up in your favorite IDE and give it a go :]


## 🚀 Usage

Make a pose from Rock(✊), Paper (🤚), Scissors (✌️), Lizard (🤏) or Spock (🖖) to your webcam and hold it! CPU will randomly generate a response, and a round will be played. 

Having issues? Make sure you're in a well-lit area and try to keep your hand steady. If the pose detected keeps switching, try moving your hand closer/farther from the webcam until it stabilises. 

- OpenCV version: 5.0.0
- MediaPipe version: 1.1.0
- Python Version: 3.13.16

## Pose Guide


Rock ✊
- Checks for all fingers down, with palm towards camera. 

Paper 🤚
- Checks for all fingers up, with palm towards camera.

Scissors ✌️
- Checks for pointer + Middle fingers up ONLY, like a peace sign! And palm towards camera.

Lizard 🤏
- Turn your hand to the side and make a 'C' shape. Checks for clustered fingertips + a certain distance from pointer to thumb.

Spock 🖖
- Make a 'V'  with your middle and ring fingers, and make sure your thumb is pointed outwards. Checks for distance between ring and middle finger and distance from thumb to pointer tip. As always, palm towards camera.



## 💭 Feedback and Contributing
Any ideas/comments? Say hi on discord. 

