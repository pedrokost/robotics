from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from  constants import *

robot = Robot(leftMotorPort=LEFT_MOTOR,
			  rightMotorPort=RIGHT_MOTOR,
			  leftTouchPort=None,
			  rightTouchPort=None,
			  sonarPort=None)

# Main Program
while True :
	robot.motors
