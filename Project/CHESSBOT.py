
import time
import copy
import imutils
import cv2
import numpy as np
import serial

from ChessBoard import ChessBoard
import subprocess, time


#################################################################


maxchess = ChessBoard()
engine = subprocess.Popen(
    'stockfish 7 x64.exe',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,)

#botmove='a0a0'

def get():
    
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    stx=""
    engine.stdin.write('isready\n')

    while True :
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        if text !='':   
            pass
        if text[0:8] == 'bestmove':        
            return text
def sget():
    
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    stx=""
    engine.stdin.write('isready\n')

    while True :
        text = engine.stdout.readline().strip()
        if text !='':   
            pass
        if text[0:8] == 'bestmove':
            mtext=text
            return mtext

def getboard():
    """ gets a text string from the board """
    btxt = raw_input("\n Enter a board message: ").lower()
    return btxt
    
def sendboard(stxt):
    """ sends a text string to the board """
    print("\n send to board: " +stxt)

def error_flag():
    global error
    error = 1

def newgame():    
    maxchess.resetBoard()
    fmove=""
    return fmove

   

def bmove(fmove):
    """ assume we get a command of the form ma1a2 from board"""    
    global botmove
    fmove=fmove
    brdmove = bmessage[1:5].lower()

    if maxchess.addTextMove(brdmove) == False :
                        etxt = "error"+ str(maxchess.getReason())+brdmove
                        maxchess.printBoard()
                        sendboard(etxt)
                        error_flag()
                        return fmove   
    else:
        maxchess.printBoard()
        fmove =fmove+" " +brdmove
        cmove = "position startpos moves"+fmove
        put(cmove)
        
        # send move to engine & get engines move        
        put("go movetime " +movetime)
        print("\n Thinking...")
        text = sget()
        
        smove = text[9:13]
        hint = text[21:25]
        
        botmove = copy.deepcopy(smove) #edited

        if maxchess.addTextMove(smove) != True :
                        stxt = "e"+ str(maxchess.getReason())+move
                        maxchess.printBoard()
                        sendboard(stxt)
        else:
                        temp=fmove
                        fmove =temp+" " +smove
                        stx = smove+hint      
                        sendboard(stx)                        
                        print ("\n computer move: " +smove)
                        maxchess.printBoard()
                        return fmove
        

def put(command):
    engine.stdin.write(command+'\n')



#################################### IMAGE PROCESSING ##################################

    
def color_filter(img,condition):
    #returns img with color filtered acc to condition 0 for yellow and codition 1 for white
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if condition==0:                    #yellow
        lower = np.array([25,85,0])
        upper = np.array([38,255,255])
    elif condition==1:                  #white
        lower = np.array([0,0,132])
        upper = np.array([180,21,255])
    elif condition==2:                  #green
        lower = np.array([64,59,102])
        upper = np.array([87,150,255])
    mask = cv2.inRange(hsv, lower, upper)  
    res = cv2.bitwise_and(img,img, mask= mask)

    return res

def presence_detect(res):
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    size=0
    for x in cnts:    
        size+=1
    if size == 0:
        return 0
    return 1


def center_detect(res):
    #returns an array of centre xy for res

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    
    blurred = cv2.GaussianBlur(opening, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    size=0
    for x in cnts:    
        size+=1
    #print 'size:',size

    # loop over the contours
    n=0
    pt=np.zeros((size,2),dtype=int)
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] == 0:
            print 'zero division error'
            return pt,size
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])       
        #stores loc of point in array
        pt[n,0]=cX
        pt[n,1]=cY       
        n+=1
    return pt,size


def perspective_transformation(img):
    #returns image within square defined by pt
    global pt
    for x in range(0,4):
        for y in range(0,3):
          if pt[y][0]+pt[y][1] > pt[y+1][0]+pt[y+1][1]:
            temp = copy.deepcopy(pt[y])
            pt[y] = copy.deepcopy(pt[y+1])
            pt[y+1] = copy.deepcopy(temp)
    if pt[1][0]<pt[2][0]:
        temp = copy.deepcopy(pt[1])
        pt[1] = copy.deepcopy(pt[2])
        pt[2] = copy.deepcopy(temp)    
    #print pt 
            
    pts1 = np.float32(pt)
    pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(300,300))
    return dst


def piece_location(loc,size):
    #returns matrix showing position of white pieces

    flag=0
    cell=300/8
    position=np.zeros((8,8),dtype=int)
    
    for x in range (0,size):                #runs through the number of peices
        flag=0
        for y in range (0,8):               #no of rows
            for z in range (0,8):           #no of columns
                 if loc[x][0]< (y+1)*cell and loc[x][1]< (z+1)*cell:
                    position[z][y]=1
                    flag=1 
                    break 
            if flag==1:
                break                 
    return position  

    
def motion(t0,t1):
    #returns if motion detected
    
    while True:
      d = cv2.absdiff(t1, t0)
      m= np.mean(d)
      
      if m>2 and m<10:
    
        print 'Motion detected! Checking for move ...'  
        return 
      
      t0 = t1
      t1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)

         
def identify_move(pos1,pos2):
    #identifies move based on two position matrices
    d=pos2-pos1
    flag=0

    castlingk=np.zeros_like(d)
    castlingq=np.zeros_like(d)

    castlingk[0]=[-1,1,1,-1,0,0,0,0]
    castlingq[0]=[0,0,0,-1,1,1,0,-1]

    if np.all(d==castlingk):
        return 'e1g1'
    if np.all(d==castlingq):
        return 'e1c1'
        
    for x in range (0,8):
        for y in range (0,8):
            if d[x][y]==1:
                place=[x,y]
                flag=1
            elif d[x][y]==-1:
                pick=[x,y]
        
    cell1=chr(104-pick[1])+str(1+pick[0])
    cell2=chr(104-place[1])+str(1+place[0])
    
    move=cell1+cell2
    return move


def show(img):
    #displays image
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def setup():
    #initail corner detection for pt

    while(1):
 
        # Take each frame
        s,frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break      
        cv2.imshow('frame',frame)
   
    #filters out all except corners   
    corners = color_filter(frame,0)
    show(corners)
    #find centre of corners
    pt,s = center_detect(corners)
    return pt


def caliberate_arm():

    print 'BEGIN CALIBERATION. MOVE ARM TO H4'

    while True:
        c = raw_input('Enter command: ')
        ser_comm(c)
        if c == 'q':
            break
        
    s,frame = cap.read()
    
    gripper = color_filter(frame,2)
    h4,ss = center_detect(gripper)
    print 'Position of h4: ',h4

    i=0
    
    while True:
        ser_comm('1')
        i=i+1
        if i>20:
            break

    return h4

    
def Position1():
    #finds position before human move
    while(1):
 
        # Take each frame
        s,frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break      
        cv2.imshow('frame',frame)
      
    #perspective transform to obtain board
    board=perspective_transformation(frame)
    #show(board)

    #filter all except white pieces in board
    pieces=color_filter(board,1)
    show(pieces)

    #find centre of pieces
    board1,s1=center_detect(pieces)

    #find position of pieces
    pos1=piece_location(board1,s1)
    #print pos1
    return pos1,s1


def testPosition1():
    #finds position before human move
    frame = cap.read()[1]
    t = [frame,frame,frame]
    pos=np.zeros((8,8),dtype=int)
    pos1=[pos,pos,pos]
    while True:
        t0 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
        t1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
      
        trial=0

        while trial<3:
            t[trial] = cap.read()[1]
            trans = perspective_transformation(t[trial])
            pieces = color_filter(trans,1)
            board1,s1 = center_detect(pieces)
            pos1[trial] = piece_location(board1,s1)
            time.sleep(1)
            trial+=1
            print "trial",trial,
        print '\n'
        
        if np.all(pos1[0]==pos1[1]) and np.all(pos1[1]==pos1[2])and np.all(pos1[0]==pos1[2]):
                return pos1[0],s1


def Position2(pos1,s1):
    #finds position after human move
    frame = cap.read()[1]
    t = [frame,frame,frame]
    pos2 = [pos1,pos1,pos1]

    while True:
        t0 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
        t1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
      
        #motion(t0,t1)#maybe remove
        trial=0

        while trial<3:
            t[trial] = cap.read()[1]
            trans = perspective_transformation(t[trial])
            pieces = color_filter(trans,1)
            board2,s2 = center_detect(pieces)
            pos2[trial] = piece_location(board2,s2)
            time.sleep(0.5)
            trial+=1
            print "trial",trial,
        
        
        if np.all(pos2[0]==pos2[1]) and np.all(pos2[1]==pos2[2])and np.all(pos2[0]==pos2[2]):
            if np.any(pos2[0]!=pos1)and s1==s2:
                return pos2[0]

            
##########################################ARM CONTROL#####################################################
def wait():
    raw_input('continue')

def makemove(source,destination):
    global pos2

    arm_h4()
    print 'INITIATION DONE'
    wait()
    if pos2[int(destination[1])-1][104-ord(destination[0])]==1:

        print 'OCCUPIED',destination
        arm_movement('h4',destination)
        g_move(1)
        g_z(1)
        g_move(0)
        g_z(0)

        leaveboard()

        g_move(1)
        g_move(0)

        arm_h4()
           
    else:
        print 'EMPTY',destination
    wait()
    arm_movement('h4',source)
    g_move(1)
    g_z(1)
    g_move(0)
    g_z(0)
    wait()
    arm_movement(source,destination)
    g_z(1)
    g_move(1)
    g_z(0)
    g_move(0)
    wait()

    leaveboard()
    
    time.sleep(3)   
    wait()


def leaveboard():
    arm_h4()
    distance = 20
    i=0
    while True:
        ser_comm('1')
        print 'l',
        i=i+1
        if i > distance:
            print '\n'
            break


def arm_h4():
    #h4 position
    global h4
    print 'TO H4...'
    xdiff=300
    ydiff=300
    
    accuracy = 10

    while abs(xdiff) > accuracy or abs(ydiff) > accuracy:
        time.sleep(0.1)

        frame = cap.read()[1]        
        #show(gripper)
        gripper=color_filter(frame,2)

        if presence_detect(gripper) == 0:
            print 'not found'
            continue
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        dilation = cv2.dilate(gripper,kernel,iterations = 1)

        g,s = center_detect(dilation)
        #print 'gripper',g
        if s != 1:
            print 'multiple green'
            continue
        
        xpix = h4[0][1]
        ypix = h4[0][0]

        xdiff = g[0][1] - xpix                  #REVIEW
        ydiff = g[0][0] - ypix
        
        #print 'xdiff',xdiff,'ydiff',ydiff

        if ydiff > accuracy:
            #serialcomm left
            ser_comm('1')           
        elif ydiff < -1*accuracy:
            #serialcomm right
            ser_comm('2')
        elif xdiff > accuracy:
            #serialcomm up
            ser_comm('3')
        elif xdiff < -1*accuracy:
            #seialcomm down
            ser_comm('4')
        
    print '\n'

 

def arm_movement(source,destination):       
    print 'MOVING FROM ',source,' TO ',destination
    
    

    alpha1 = ord(source[0])
    num1 = int(source[1])
    alpha2 = ord(destination[0])
    num2 = int(destination[1])

    x = alpha2 - alpha1
    y = num2 - num1

    print 'Row move: ',x
    print 'Column move: ',y
     
    if x<0:
        for i in range (0,10*abs(x)):
            ser_comm('2')            
    elif x>0:
        for i in range (0,10*abs(x)):
            ser_comm('1')
            
    if y<0:
        for i in range (0,10*abs(y)):
            ser_comm('3')            
    elif y>0:
        for i in range (0,10*abs(y)):
            ser_comm('4')
            
    t = (abs(x)+abs(y))*0.5
    print 'WAIT for ',t
    time.sleep(t)
    print destination,' REACHED'

    

def g_move(action):         #open or close gripper
    if action == 1:
        #gripper open
        ser_comm('9')
    elif action == 0:
        #gripper close
        ser_comm('8')
    time.sleep(1)


def g_z(action):            #moves gripper up or down
    if action == 1:
        #gripper down
        ser_comm('7')
        
    elif action == 0:
        #gripper up
        ser_comm('6')
    time.sleep(2)
    

def ser_comm(data):  ################################
    global ser
    #ser.write(data)

    if data == '1':
        print 'l',
    elif data == '2':
        print 'r',
    elif data == '3':
        print 'u',
    elif data == '4':
        print 'd',
    elif data == '6':
        print 'g_up',
    elif data == '7':
        print 'g_down',
    elif data == '8':
        print 'g_close',
    elif data == '9':
        print 'g_open',
    time.sleep(0.1)
    

 
   
###########################  MAIN   ####################################        

usbport= 'COM3'
#ser = serial.Serial(usbport,9600,timeout = 1) ################################

skill = "10"
movetime = "4000"
fmove = newgame()


cap = cv2.VideoCapture(0)

pt = setup()
h4 = caliberate_arm()



while True:
    
    #pos1,s1=Position1()
    pos1,s1=testPosition1()    
    print pos1
    print "MAKE MOVE!"
    while True:                 #repeats if error in move
        error=0
        pos2=Position2(pos1,s1)    
        print 'Move identified!'    

        mymove=identify_move(pos1,pos2)
        print 'My move: ',mymove
        
        bmessage = 'm'+mymove    #  ENGINE       
   
        fmove=fmove
        fmove = bmove(fmove)
        if error == 0:
            break
        print '\nRepeat move!'         
    
    print botmove


    source = botmove[0]+botmove[1]
    destination = botmove[2]+botmove[3]    
    
    makemove(source,destination);
    print 'MOVE MADE!'
    print 'Please wait...'
    time.sleep(3)
         
  
