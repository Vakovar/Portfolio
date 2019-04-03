"""
Initializing and reacting to triggers. See PepperTriggerList.txt for possible triggers.
Example:
    leftBumper = self.memory.subscriber("LeftBumperPressed")
    leftBumper.signal.connect(self.onLeftBumper)
    def onLeftBumper(self, value):
        print value
"""

import time
import sys
import argparse
import qi

class Triggers(object):

    def __init__(self, app):
        super(Triggers, self).__init__()
        app.start()
        session = app.session
        self.memory = session.service("ALMemory")
        self.tts = session.service("ALTextToSpeech")

        # Left hand
        self.leftHandBack = self.memory.subscriber("HandLeftBackTouched")
        self.leftHandBack.signal.connect(self.onLeftHandBack)

        # Right hand
        self.rightHandBack = self.memory.subscriber("HandRightBackTouched")
        self.rightHandBack.signal.connect(self.onRightHandBack)

        # Bumpers
        self.leftBumper = self.memory.subscriber("LeftBumperPressed")
        self.leftBumper.signal.connect(self.onLeftBumper)

        self.rightBumper = self.memory.subscriber("RightBumperPressed")
        self.rightBumper.signal.connect(self.onRightBumper)

        self.backBumper = self.memory.subscriber("BackBumperPressed")
        self.backBumper.signal.connect(self.onBackBumper)

        # Sonar
        self.sonarFront = self.memory.subscriber("SonarFrontDetected")
        self.sonarFront.signal.connect(self.onSonarFront)
        self.sonar = session.service("ALSonar")
        self.sonar.subscribe("Triggers")

        # People
        self.justArrived = self.memory.subscriber("PeoplePerception/JustArrived")
        self.justArrived.signal.connect(self.onJustArrived)
        
        self.justLeft = self.memory.subscriber("PeoplePerception/JustLeft")
        self.justLeft.signal.connect(self.onJustLeft)
        
        self.visiblePeople = self.memory.subscriber("PeoplePerception/VisiblePeopleList")
        #self.visiblePeople.signal.connect(self.onVisiblePeople)

        self.youSmiling = self.memory.subscriber("FaceCharacteristics/PersonSmiling")
        self.youSmiling.signal.connect(self.onYouSmiling)
        
        #Starting ALFaceDetection
        self.face_detection = session.service("ALFaceDetection")
        self.face_detection.subscribe("Triggers")

    def onLeftHandBack(self, value):
        if value == 1.0:
            print "Hand Left Back"
            self.tts.say("Left")
        elif value == 0.0:
            self.tts.say("Off")

    def onRightHandBack(self, value):
        if value == 1.0:
            print "Hand Right Back"
            self.tts.say("Right")
        elif value == 0.0:
            self.tts.say("Off")

    def onLeftBumper(self, value):
        if value == 1.0:
            print "Left bumper"
            self.tts.say("Left")
        elif value == 0.0:
            self.tts.say("Up")
    
    def onRightBumper(self, value):
        if value == 1.0:
            print "Right Bumper"
            self.tts.say("Right")
        elif value == 0.0:
            self.tts.say("Up")

    def onBackBumper(self, value):
        if value == 1.0:
            print "Back Bumper"
            self.tts.say("Back")
        elif value == 0.0:
            self.tts.say("Up")

    def onSonarFront(self, value):
        print value

    def printSonarValue(self):
        print "Sonar: %.3f" % (self.memory.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))

    def onJustArrived(self, value):
        self.tts.say("Hi there, new person")
        print "Person arrived: %s" % (value)
    
    def onJustLeft(self, value):
        self.tts.say("Someone just left")
        print "Person left: %s" % (value)
    
    def onVisiblePeople(self, value):
        people = len(value)
        if people == 0:
            self.tts.say("Oh my, I'm all alone")
        elif people == 1:
            self.tts.say("Hey, there's another one here with me")
        elif people > 1:
            self.tts.say("Now I know of %s people in here" % (str(people)))
        print value
    
    def onYouSmiling(self, value):
        self.tts.say("Such a nice smile")
        print value

    def run(self):
        print "Starting Triggers"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping Triggers"
            #stop
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
        app = qi.Application(["Triggers", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    triggers = Triggers(app)
    triggers.run()
    