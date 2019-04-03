"""
Project to make Pepper move and react to obsticles.
"""

import time
import sys
import argparse
import qi

class RemoteControl(object):
    """Main class"""

    alreadyRollin = False

    def __init__(self, app):
        super(RemoteControl, self).__init__()
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
        """Bumpers trigger reaction"""
        if value == 1:
            self.fullStop()
    
    def halt(self):
        """Stop moving. Should always be executed when robot stops IF NOT fullStop()"""
        self.alreadyRollin = False

        """Gets robots current speed, to use as a relative point of slowing down."""
        curFl = self.memory.getData("Device/SubDeviceList/WheelFL/Speed/Sensor/Value")
        curFr = self.memory.getData("Device/SubDeviceList/WheelFR/Speed/Sensor/Value")
        curB = self.memory.getData("Device/SubDeviceList/WheelB/Speed/Sensor/Value")
        self.dcm.setAlias([
            "TheySeeMeRollin",
            "ClearAll",
            "time-separate",
            0,
            [self.dcm.getTime(0), self.dcm.getTime(500)],
            [
                [1.0, 0.0],
                [1.0, 0.0],
                [1.0, 0.0],

                [curFl, 0.0],
                [curFr, 0.0],
                [curB, 0.0]
            ]
        ])
        time.sleep(0.3)
    
    def fullStop(self):
        """Stop moving instantly. Use halt() on a regular basis."""
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

    def roll(self, rx, ry):
        """
        var rx: forwards(1) backwards(-1)
        var ry: right(1) left(-1)
        """

        """When she moves backwards, left-right are inverted."""
        if rx < 0:
            ry = ry*-1

        """Control code to ensure inputs are within range of 1 and -1"""
        if rx > 1:
            rx = 1
        if ry > 1:
            ry = 1
        if rx < -1:
            rx = -1
        if ry < -1:
            ry = -1
        
        #ry = ry*2
        rx = rx*2

        if self.alreadyRollin == False:
            self.alreadyRollin = True
            self.dcm.setAlias([
                "TheySeeMeRollin",
                "ClearAll",
                "time-separate",
                0,
                [self.dcm.getTime(0), self.dcm.getTime(2000)],
                [
                    [0.0, 1.0],
                    [0.0, 1.0],
                    [0.0, 1.0],

                    [0.0, (rx + ry)*3.0],
                    [0.0, (-rx + ry)*3.0],
                    [0.0, ry*3.0]
                ]
            ])
        else:
            self.dcm.setAlias([
                "TheySeeMeRollin",
                "ClearAll",
                "time-separate",
                0,
                [self.dcm.getTime(500)],
                [
                    [1.0],
                    [1.0],
                    [1.0],

                    [(rx + ry)*3.0],
                    [(-rx + ry)*3.0],
                    [ry*3.0]
                ]
            ])
    
    def run(self):
        """Logic behind moving"""
        print "Rollin'"
        try:
            while True:
                self.roll(1.0, 1.0)
                time.sleep(2)
                self.roll(1.0, 0.5)
                time.sleep(2)
                self.roll(1.0, 0.0)
                time.sleep(2)
                self.roll(1.0, -0.5)
                time.sleep(2)
                self.roll(1.0, -1.0)
                time.sleep(2)
                self.roll(1.0, 1.0)
                time.sleep(2)
                self.roll(0.5, 1.0)
                time.sleep(2)
                self.roll(0.0, 1.0)
                time.sleep(2)
                self.roll(-0.5, 1.0)
                time.sleep(2)
                self.roll(-1.0, 1.0)
                time.sleep(2)
                self.halt()
        except KeyboardInterrupt:
            print "Stoping"
            self.halt()
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.43.163",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["RemoteControl", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    remoteControl = RemoteControl(app)
    #NB: Running the class requires a lot of space, but demonstrates her movement quite nicely
    #remoteControl.run()
