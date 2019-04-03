"""
Script that moves the pepper robot with a gamepad (xbox controller)
Example:
    from PepperMotionControl import PepperMove
    motion = PepperMove()
    motion.moveForward()
"""

from naoqi import ALProxy
from inputs import get_gamepad
from RemoteControlDCM import RemoteControl
import qi
import sys
import argparse
import time

ip = None

def startPosture(app):
    session = app.session
    posture = session.service("ALRobotPosture")
    posture.goToPosture("StandInit", 0.5)

def endPosture(app):
    session = app.session
    posture = session.service("ALRobotPosture")
    posture.goToPosture("Crouch", 0.5)


"""
Logging both pressed and release
Dpad works on axis. Pressed xaxis up + xaxis release = button press
Returns the action "UP" "DOWN" "LEFT "RIGHT" 
or "X R" for release on x-axis
or "Y R" for release on y-axis
"""
def absolute(event):
        if event.code == "ABS_HAT0Y":
            if event.state == -1:
                return "UP"
            elif event.state == 1:
                return "DOWN"
            elif event.state == 0:
                return "X R"
        elif event.code == "ABS_HAT0X":
            if event.state == -1:
                return "LEFT"
            elif event.state == 1:
                return "RIGHT"
            elif event.state == 0:
                return "Y R"

        elif event.code == "ABS_X":
            valueX = event.state/32000.0
            if valueX > 1:
                valueX = 1
            elif valueX < -1:
                valueX = -1
            
            return ("ABS_X", valueX)

        elif (event.code == "ABS_Y"):
            valueY = event.state/32000.0
            if valueY > 1:
                valueY = 1
            elif valueY < -1:
                valueY = -1
            
            return ("ABS_Y", valueY)
            
        elif (event.code == "ABS_RX"):
            valueRX = event.state/32000.0
            if valueRX > 1:
                valueRX = 1
            elif valueRX < -1:
                valueRX = -1
            
            return ("ABS_RX", valueRX)
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

def main(app):
    remote = None
    if app:
        remote = RemoteControl(app)

    stop = False
    up = False
    down = False
    left = False
    right = False
    xrelease = False
    yrelease = False
    motion = 0
    turn = 0

    prevTime = 0
    while 1:
        curTime = time.time()
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                action = absolute(event)
                if type(action) == tuple:
                    if action[0] == "ABS_X":
                        pass
                    elif action[0] == "ABS_Y":
                        motion = action[1]
                    elif action[0] == "ABS_RX":
                        turn = action[1]
                

            elif (event.ev_type == "Key"):
                keyPressed = key(event)
                if (keyPressed == "Select"):
                    stop = True
                    break
                elif (keyPressed == "A"):
                    startPosture(app)
                    print "Going to posture stand"
                elif (keyPressed == "B"):
                    endPosture(app)
                    print "Going to posture zero"
                elif (keyPressed == "TL"):
                    pass
                elif (keyPressed == "TR"):
                    pass
            elif (event.ev_type == "Sync"):
                pass
                #Don't really know what to do with the sync events?
            else:
                print (event.ev_type, event.code, event.state)
        #end while

        if prevTime + 0.3 < curTime:
            print "turn {0} motion {1}".format(turn, motion)
            prevTime = curTime
            if remote:
                remote.roll(motion, turn)

        if xrelease or yrelease:
            print "x or y release with no direction. Warning!"

        if stop:
            if remote:
                remote.fullStop()
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.43.163",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--controller", type=bool, default=False,
                        help="Set this flag if only running the controller")

    args = parser.parse_args()
    app = None
    if args.controller == False:
        try:
            # Initialize qi framework.
            connection_url = "tcp://" + args.ip + ":" + str(args.port)
            ip = args.ip #Global ip. Quick fix
            app = qi.Application(["RemoteControl", "--qi-url=" + connection_url])
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + args.ip +
                   "\" on port " + str(args.port) +".\n"+
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

    main(app)
