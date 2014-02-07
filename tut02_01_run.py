from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from random import uniform
robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, LEFT_TOUCH, RIGHT_TOUCH, None)

# Main Program

while(True):
	isLeftTouch = robot.leftTouch.isTouch()
	isRightTouch = robot.rightTouch.isTouch()
	if(isLeftTouch and isRightTouch):
		if(uniform(0, 1) < 0.5):
			robot.motors.right90deg()
		else:
			robot.motors.left90deg()
	elif(isLeftTouch):
		robot.motors.right90deg()
	elif(isRightTouch):
		robot.motors.left90deg()
	else:
		robot.motors.setLeftSpeed(150)
		robot.motors.setRightSpeed(150)
	time.sleep(0.01)
