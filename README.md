# Chessbot

<p align="center"> 
<img src="/img/img10.png" width = "400">
</p> 

The chessbot is a robot that can play a complete game of chess against a human opponent. It uses a camera to identify the move made by the human opponent. Then it calculates the best move to be made using an out-of-the-box chess engine and picks and places the required piece so as to execute the best move. The process repeats till the game comes to an end.

### Video 

<p align="center">
<a href="https://www.youtube.com/watch?v=mVN2BmjSzAE">
         <img alt="Navigation" src="/img/img11.png" width="400" >
</a>
</p>

### Architecture

<p align="center"> 
<img src="/img/img1.png" width = "400">
</p>

### Hardware:

The robotic arm is a cartesian arm with 4 DOF including the gripper. The arm has a core xy mechanism allowing for movement over a planaer surface with minimal weight on the links. 

<p align="center"> 
<img src="/img/img2.png" width = "400">
</p>

<p align="center"> 
<img src="/img/img3.png" width = "400">
</p> 

<p align="center"> 
<img src="/img/img4.png" width = "400">
</p>


The arm and gripper were designed in CREO Parametric and then 3D printed. 


<p align="center"> 
<img src="/img/img9.png" width = "400">
</p>

The cartesian arm is actuated using two stepper motors for x axis and y axis movements. A belt drive converts the rotary motion to linear motion. The gripper moves vertically and open/close using two servos. An Arduino UNO controls the stepper motor drivers and the servo motors.

## Software
:
The image processing is done using OpenCV 3.0.0 running on Python 2.7. The program uses techniques such as color detection, perspective transformation, motion detection and several other image prepossessing techniques. 

<p align="center"> 
<img src="/img/img5.png" width = "400">
</p>

The goal of the image processing algorithm is to identify the move made from an image of the board before and after the move is made.

<p align="center"> 
<img src="/img/img6.png" width = "400">
</p>

By color filtering the corner markers, finding their centroids and then performing perspective transformation, the image is transformed to include only the region that is relevant for move identification. Color filtering the white pixels helps locate the white peices which are mapped onto a matrix.

<p align="center"> 
<img src="/img/img7.png" width = "400">
</p>

Simmilarly, the state of the board after the move is made is found. By comparing the two matrices, the move made is computed and converted to chess notation. In this case 'e2e4'.

<p align="center"> 
<img src="/img/img8.png" width = "400">
</p>

Stockfish 7, the open source chess engine determines the move to be made to counter the detected move.

A video of the robot can be found [**here**](https://www.youtube.com/watch?v=mVN2BmjSzAE)
