from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from  constants import *



robot = Robot(leftMotorPort=LEFT_MOTOR,
			  rightMotorPort=RIGHT_MOTOR,
			  leftTouchPort=LEFT_TOUCH,
			  rightTouchPort=RIGHT_TOUCH,
			  sonarPort=SONAR_SENSOR)

# Main Program

while(True):
	robot.keepDistanceFront(30)
