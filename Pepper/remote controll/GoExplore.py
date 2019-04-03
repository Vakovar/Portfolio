"""
Project to make Pepper move and react to obsticles.
"""

import time
import sys
import argparse
import qi

class GoExplore(object):
    """Main class"""

    alreadyRollin = False
    turnCount = 0
    mSpeed = 3.0

    def __init__(self, app):
        super(GoExplore, self).__init__()
        app.start()
        session = app.session
        self.dcm = session.service("DCM")
        self.memory = session.service("ALMemory")
        self.tts = session.service("ALTextToSpeech")

        self.leftBumper = self.memory.subscriber("LeftBumperPressed")
        self.leftBumper.signal.connect(self.onBumper)

        self.rightBumper = self.memory.subscriber("RightBumperPressed")
        self.rightBumper.signal.connect(self.onBumper)

        self.rightBumper = self.memory.subscriber("BackBumperPressed")
        self.rightBumper.signal.connect(self.onBumper)

        self.dcm.createAlias([
            "TheySeeMeRollin",
            [
                "WheelFL/Stiffness/Actuator/Value",
                "WheelFR/Stiffness/Actuator/Value",
                "WheelB/Stiffness/Actuator/Value",
                "WheelFL/Speed/Actuator/Value",
                "WheelFR/Speed/Actuator/Value",
                "WheelB/Speed/Actuator/Value"
            ]
        ])

        self.memory = session.service("ALMemory")

    def onBumper(self, value):
        """Bumper trigger reaction"""
        if value == 1:
            self.fullStop()
    
    def fullStop(self):
        """Stop moving instantly"""
        self.alreadyRollin = False
        self.dcm.setAlias([
            "TheySeeMeRollin",
            "ClearAll",
            "time-separate",
            0,
            [self.dcm.getTime(0)],
            [
                [0.0],
                [0.0],
                [0.0],

                [0.0],
                [0.0],
                [0.0]
            ]
        ])
        #self.tts.say("Oops")
        self.scriptRunning = False


    def turn(self, direction):
        """Make Pepper turn left or right"""
        if direction == "right":
            direct = 1.0
        elif direction == "left":
            direct = -1.0
        elif direction == "back":
            direct = -2.05
        else:
            return
        tSpeed = direct * 3.2
        self.turnCount += 1
        self.dcm.setAlias([
            "TheySeeMeRollin",
            "ClearAll",
            "time-separate",
            0,
            [self.dcm.getTime(0000), self.dcm.getTime(1250), self.dcm.getTime(2500)],
            [
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],

                [0.0, tSpeed, 0.0],
                [0.0, tSpeed, 0.0],
                [0.0, tSpeed, 0.0]
            ]
        ])
        time.sleep(2.5)

    def roll(self):
        """Pepper moves forwards. NB: She doesn't stop till you tell her to"""
        if not self.alreadyRollin:
            self.alreadyRollin = True
            self.turnCount = 0
            self.dcm.setAlias([
                "TheySeeMeRollin",
                "ClearAll",
                "time-separate",
                0,
                [self.dcm.getTime(1000), self.dcm.getTime(3000)],
                [
                    [0.0, 1.0],
                    [0.0, 1.0],
                    [0.0, 1.0],

                    [0.0, self.mSpeed],
                    [0.0, -self.mSpeed],
                    [0.0, 0.0]
                ]
            ])

    def halt(self):
        """Stop moving"""
        self.alreadyRollin = False
        self.dcm.setAlias([
            "TheySeeMeRollin",
            "ClearAll",
            "time-separate",
            0,
            [self.dcm.getTime(0), self.dcm.getTime(300)],
            [
                [1.0, 0.0],
                [1.0, 0.0],
                [1.0, 0.0],

                [self.mSpeed, 0.0],
                [-self.mSpeed, 0.0],
                [0.0, 0.0]
            ]
        ])
        time.sleep(0.3)
    
    def run(self):
        """Logic behind moving"""
        print "Rollin'"
        self.scriptRunning = True
        try:
            while self.scriptRunning:
                if self.memory.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value") > 0.5:
                    if not self.alreadyRollin:
                        self.roll()
                else:
                    if self.alreadyRollin:
                        self.halt()
                    if self.turnCount == 0:
                        self.turn("right")
                    elif self.turnCount == 1:
                        self.turn("back")
                    else:
                        self.turn("left")
                time.sleep(0.1)
            print "Exit script"
        except KeyboardInterrupt:
            print "Stoping"
            self.halt()
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.137.4",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["MoveTurn", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    goex = GoExplore(app)
    goex.run()
    time.sleep(10)
    goex.fullStop()