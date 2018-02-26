# Chessbot

The chessbot is a robot that can play a complete game of chess against a human opponent. It uses image processing to track the movement of pieces by the human opponent. Then it calculates the best move to be made and picks and places the required piece to execute the best move. The process repeats till the game comes to an end.

Mechanical Elements
The robotic arm is a cartesian arm. Hence it is able to move in 3 axes. The manipulator is a gripper. Hence it has 4 degrees of freedom. The joints of the arm are to be designed in CREO Parametric and then 3D printed using PLA. 
The chess board will have red and black squares so that the white pieces will contrast with the board making it easier to detect for image processing.

Electrical Elements
The cartesian arm will be actuated using two stepper motors for x axis and y axis movements. A belt drive will convert the rotary motion to linear motion. The gripper will move vertically and open/close using two servos. An Arduino UNO will control the stepper motor drivers and the servo motors.

Programming Elements
The image processing will be done using OpenCV 3.0.0 running on Python 2.7. The program will use techniques such as color detection, perspective transformation, motion detection and several other image prepossessing techniques. There is constant communication between the PC and Arduino board by serial communication. A GUI on the PC helps to interact with the robot and observe its moves. The GUI is written in Python as well. The best move to be made is calculated using a chess engine called stockfish 7 which is an open source chess engine.

The Project folder contains all contents that contribute towards the software of the chessbot


CHESSBOT.py contains the main program which performs the image processing of the chessbot as well as the serial communication to the arduino.

Chessbot.pptx contains the explanation of contruction and working of the project

chessbot pic.docx contains furthur images 

stockfish 7 x64.exe is the chess engine used

ChessBoard.py is a library utilised during interaction with the chess engine. It is not written by me.

For any more information contact vishnu.prem06@gmail.com

NOTE: I am relatively new to Github and an amateur programmer. Please excuse the lack of professionalism in my work.
