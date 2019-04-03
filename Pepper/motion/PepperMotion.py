"""
Controller class for the pepper robot to move in different direction
Example:
    from PepperMotionControl import PepperMove
    motion = PepperMove()
    motion.moveForward()
"""
from naoqi import ALProxy
import math
import time
import sys

class PepperMove:
    speed = 0.2
    turnSpeed = math.radians(90)

    def __init__(self, ip, port=9559):
        self.motion = ALProxy("ALMotion", ip, port)

    def checkMotion(self):
        if (self.motion == None):
            print "Need to connect with ALMotion with ALProxy"
            sys.exit(0)

    def moveForward(self):
        self.checkMotion()
        self.motion.move(self.speed, 0, 0)
        time.sleep(2)
        self.motion.stopMove()

    def moveBack(self):
        self.checkMotion()
        self.motion.move(-self.speed, 0, 0)
        time.sleep(2)
        self.motion.stopMove()
    
    def moveRight(self):
        self.checkMotion()
        self.motion.move(0, -self.speed, 0)
        time.sleep(2)
        self.motion.stopMove()

    def moveLeft(self):
        self.checkMotion()
        self.motion.move(0, self.speed, 0)
        time.sleep(2)
        self.motion.stopMove()

    def turnRight(self):
        self.checkMotion()
        self.motion.move(0, 0, -self.turnSpeed)
        time.sleep(2)
        self.motion.stopMove()

    def turnLeft(self):
        self.checkMotion()
        self.motion.move(0, 0, self.turnSpeed)
        time.sleep(2)
        self.motion.stopMove()