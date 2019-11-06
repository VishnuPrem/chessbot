# Chessbot

The chessbot is a robot that can play a complete game of chess against a human opponent. It uses a camera to identify the move made by the human opponent. Then it calculates the best move to be made using an out-of-the-box chess engine and picks and places the required piece so as to execute the best move. The process repeats till the game comes to an end. A video of the robot can be found [here](https://www.youtube.com/watch?v=mVN2BmjSzAE)

![GitHub Logo](/img/img1.png)

<p align="center">
  <img width="460" height="300" src="/img/img1.png">
</p>

### Hardware:

The robotic arm is a cartesian arm. Hence it is able to move in 3 axes. The manipulator is a gripper. Hence it has 4 degrees of freedom. The joints of the arm were designed in CREO Parametric and then 3D printed using PLA. 


Electrical Elements:
The cartesian arm is actuated using two stepper motors for x axis and y axis movements. A belt drive converts the rotary motion to linear motion. The gripper moves vertically and open/close using two servos. An Arduino UNO controls the stepper motor drivers and the servo motors.

Programming Elements:
The image processing is done using OpenCV 3.0.0 running on Python 2.7. The program uses techniques such as color detection, perspective transformation, motion detection and several other image prepossessing techniques. There is constant communication between the PC and Arduino board by serial communication. The best move to be made is calculated using 'Stockfish 7', which is an open source chess engine.

The Project folder contains all contents that contribute towards the software of the chessbot


CHESSBOT.py contains the main program which performs the image processing of the chessbot as well as the serial communication to the arduino.

Chessbot.pptx contains the explanation of contruction and working of the project

chessbot pic.docx contains furthur images 

stockfish 7 x64.exe is the chess engine used

ChessBoard.py is a library utilised during interaction with the chess engine. It is not written by me.

For any more information contact vishnu.prem06@gmail.com


