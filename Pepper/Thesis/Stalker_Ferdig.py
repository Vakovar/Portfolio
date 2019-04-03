"""
Project to make Pepper move and react to obsticles.
"""

import time
import sys
import argparse
import qi
import math

class Explore(object):
    """Main class"""

    def __init__(self, app):
        super(Explore, self).__init__()

        app.start()
        session = app.session

        self.memory_service = session.service("ALMemory")
        self.motion_service = session.service("ALMotion")
        self.autonomous = session.service("ALAutonomousLife")
        self.tracker_service = session.service("ALTracker")
        self.posture = session.service("ALRobotPosture")

        self.leftBumper = self.memory_service.subscriber("LeftBumperPressed")
        self.rightBumper = self.memory_service.subscriber("RightBumperPressed")        
        self.backBumper = self.memory_service.subscriber("BackBumperPressed")

        self.leftBumper.signal.connect(self.onBumper)
        self.rightBumper.signal.connect(self.onBumper)
        self.backBumper.signal.connect(self.onBumper)

        self.sonarFramme = self.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value")

        # the robot gets in position to start the script.
        self.posture.goToPosture("StandInit", 2)
        self.motion_service.waitUntilMoveIsFinished()

        self.autonomous.setSafeguardEnabled("RobotPushed", False)
        self.autonomous.setSafeguardEnabled("RobotMoved", False)
        self.autonomous.setSafeguardEnabled("RobotFell", False)

    def onBumper(self, value):
        """Bumper trigger reaction"""
        if value == 1:
            self.onStop()

    def motionRoll(self):
        print "robot is supposed to move | motionRoll"  
        self.motion_service.moveInit()
        self.motion_service.move(0.175,0,0, _async=True)

    def onStop(self):
        self.motion_service.moveInit()
        self.motion_service.move(0,0,0, _async=True)

    def bodyTurn(self):
        print "turning body"
        self.motion_service.moveInit()
        self.motion_service.moveTo(0,0,self.memory_service.getData("Device/SubDeviceList/HeadYaw/Position/Sensor/Value"), _async=True)
        #self.motion_service.waitUntilMoveIsFinished()'

    def onTurn(self, direction):
        #Turn logic

        if direction == "right": #obstacle to peppers left, turning right
            #self.onStop()
            self.motion_service.moveInit()
            self.motion_service.moveTo(0, 0, -(math.pi)/2, _async=True)
            #self.motion_service.waitUntilMoveIsFinished()
            print "onTurn Dir: Right"



        elif direction == "left":
            #self.onStop()

            print "onTurn Dir: Left"
            self.motion_service.moveInit()
            self.motion_service.moveTo(0, 0, (math.pi)/2, _async=True)
            #self.motion_service.waitUntilMoveIsFinished()


        elif direction == "back": #sonar front has detected an obstacle

            if self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Right/Sensor/Value") and self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Left/Sensor/Value") == 1: # both IR sensors triggered, makes the robot back up
                print "Backing up"
                self.motion_service.moveInit()
                self.motion_service.moveTo(-1, 0, 0, _async=True) # move back 1 meter
                self.motion_service.waitUntilMoveIsFinished()

    def run(self):
        """Logic behind moving"""
        print "Script started"

        self.scriptRunning = True

        targetName = "Target"
        faceWidth = 0.10
        #self.alreadyRollin = False
        self.tracker_service.registerTarget(targetName, faceWidth)
        self.tracker_service.track(targetName)
        try:
            while self.scriptRunning == True:
                if ( self.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value") > 0.5 and self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Left/Sensor/Value") == 0 and self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Right/Sensor/Value")== 0):
                    
                    self.tracker_service.track(targetName)
                    self.motionRoll()

                    self.Yaw = self.memory_service.getData("Device/SubDeviceList/HeadYaw/Position/Sensor/Value")
                    ## vil prove med ekstremt lite verdi her.
                    if (self.Yaw > 0.45 or self.Yaw < -0.45): # 1.05 betyr 60 graders avvik fra midten av hode
                        self.bodyTurn()

                    print "Called by Sensor name: Front Sonar Value: " + str(self.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))
                    #self.onTurn("back")

                elif self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Left/Sensor/Value") == 1:
                    print "InfraredLeft: " + str(self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Left/Sensor/Value"))
                    self.onTurn("right")

                elif self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Right/Sensor/Value") == 1:
                    print "InfraredRight: " + str(self.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Right/Sensor/Value"))
                    self.onTurn("left")

            print "Exit script"
        except KeyboardInterrupt:
            print "Stopping"
            self.scriptRunning = False
            self.onStop()
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.137.249",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["Explore", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    goex = Explore(app)
    goex.run()