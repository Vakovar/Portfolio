"""
Script that moves the pepper robot with a gamepad (xbox controller)
Example:
    from PepperMotionControl import PepperMove
    motion = PepperMove()
    motion.moveForward()
"""

from naoqi import ALProxy
from inputs import get_gamepad
from PepperMotion import PepperMove
import sys

def startPosture(ip, port=9559):
    posture = ALProxy("ALRobotPosture", ip, port)
    posture.goToPosture("StandInit", 0.5)

def endPosture(ip, port=9559):
    posture = ALProxy("ALRobotPosture", ip, port)
    posture.goToPosture("Crouch", 0.5)


"""
Logging both pressed and release
Dpad works on axis. Pressed xaxis up + xaxis release = button press
Returns the action "UP" "DOWN" "LEFT "RIGHT" 
or "X R" for release on x-axis
or "Y R" for release on y-axis
"""
def absolute(event):
        if (event.code == "ABS_HAT0Y"):
            if (event.state == -1):
                return "UP"
            elif(event.state == 1):
                return "DOWN"
            elif (event.state == 0):
                return "X R"
        elif (event.code == "ABS_HAT0X"):
            if (event.state == -1):
                return "LEFT"
            elif (event.state == 1):
                return "RIGHT"
            elif (event.state == 0):
                return "Y R"

        elif (event.code == "ABS_X"):
            pass
        elif (event.code == "ABS_Y"):
            pass
        elif (event.code == "ABS_RX"):
            pass
        elif (event.code == "ABS_RY"):
            pass
        else:
            #pass
            print(event.ev_type, event.code, event.state)


def key(event):
        if (event.code == "BTN_SOUTH"):
            return "A"
        elif (event.code == "BTN_EAST"):
            return "B"
        elif (event.code == "BTN_SELECT"):
            if (event.state == 1):
                return "Select"
        elif (event.code == "BTN_TL"):
            if (event.state == 0):
                return "TL"
        elif (event.code == "BTN_TR"):
            if (event.state == 0):
                return "TR"

        print (event.ev_type, event.code, event.state)

def main():    
    argcount = len(sys.argv)
    if (argcount > 1):
        ip = str(sys.argv[1])
    else:
        print "No ip, no controll"
        sys.exit()

    motion = PepperMove(ip)

    stop = False
    up = False
    down = False
    left = False
    right = False
    xrelease = False
    yrelease = False
    turnRight = False
    turnLeft = False

    while 1:
        events = get_gamepad()
        for event in events:
            if (event.ev_type == "Absolute"):
                action = absolute(event)
                if (action == "UP"):
                    up = True
                elif (action == "DOWN"):
                    down = True
                elif (action == "RIGHT"):
                    right = True
                elif (action == "LEFT"):
                    left = True
                elif (action == "X R"):
                    xrelease = True
                elif (action == "Y R"):
                    yrelease = True
            elif (event.ev_type == "Key"):
                keyPressed = key(event)
                if (keyPressed == "Select"):
                    stop = True
                    break
                elif (keyPressed == "A"):
                    startPosture(ip)
                    print "Going to posture stand"
                elif (keyPressed == "B"):
                    endPosture(ip)
                    print "Going to posture zero"
                elif (keyPressed == "TL"):
                    turnLeft = True
                elif (keyPressed == "TR"):
                    turnRight = True
            elif (event.ev_type == "Sync"):
                pass
                #Don't really know what to do with the sync events?
            else:
                print (event.ev_type, event.code, event.state)
        if (up and xrelease):
            up = False
            xrelease = False
            motion.moveForward()
        elif (down and xrelease):
            down = False
            xrelease = False
            motion.moveBack()
        elif (right and yrelease):
            right = False
            yrelease = False
            motion.moveRight()
        elif (left and yrelease):
            left = False
            yrelease = False
            motion.moveLeft()
        elif (turnLeft):
            turnLeft = False
            motion.turnLeft()
        elif (turnRight):
            turnRight = False
            motion.turnRight()

        if (xrelease or yrelease):
            print "x or y release with no direction. Warning!"
        
        if (stop):
            print "Stopp controller"
            break


if __name__ == "__main__":
    main()
    