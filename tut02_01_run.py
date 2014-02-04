from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from  constants import *
from random import uniform
robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, LEFT_TOUCH, RIGHT_TOUCH)


# Main Program

while(True):
	if(robot.isLeftTouch() and robot.isRightTouch()):
		if(uniform(0, 1) < 0.5):
			robot.right90deg()
		else:
			robot.left90deg()
	elif(robot.isLeftTouch()):
		robot.right90deg()
	elif(robot.isRightTouch()):
		robot.left90deg()
	else:
		robot.setFwdSpeed(100)
	time.sleep(0.01)
