# Gesture-Recognition-Project

## Overview
This project implements a gesture recognition system using computer vision techniques to control mouse and keyboard inputs. It utilizes the MediaPipe library for hand tracking and the PyAutoGUI library to simulate mouse movements and keyboard presses based on hand gestures.

## Features
- **Mouse Control:** Move the mouse pointer using hand gestures.
- **Keyboard Control:** Perform keyboard actions such as arrow key presses and spacebar using hand movements.
- **Zoom Functionality:** Pinch gestures to zoom in and out on the screen.

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI

You can install the required libraries using pip:

```bash```
```pip install opencv-python mediapipe pyautogui```

Usage
1. Clone the repository:
```
git clone https://github.com/yourusername/Gesture-Recognition.git
cd Gesture-Recognition
```
2. Run the main script:
```
python main.py
```

3. Follow these gestures for controls:

Left Hand:
- Move the mouse by moving your hand.
- Click by positioning your index finger tip above the middle finger pip joint.
  
Right Hand:
- Pinch to zoom in.
- Move fingers apart to zoom out.

  Acknowledgments
This project utilizes the MediaPipe library developed by Google for hand tracking.
Special thanks to the contributors and the open-source community for their continuous support.

This project is licensed under the MIT License. See the LICENSE file for details.
