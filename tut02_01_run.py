from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from  constants import *

robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, LEFT_TOUCH, RIGHT_TOUCH)


# Main Program

while(True):
	if(robot.isLeftTouch()):
		robot.right90deg()
	elif(robot.isRightTouch()):
		robot.left90deg()
