from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from random import uniform

robot = Robot(leftMotorPort=LEFT_MOTOR,
			  rightMotorPort=RIGHT_MOTOR,
			  leftTouchPort=LEFT_TOUCH,
			  rightTouchPort=RIGHT_TOUCH)

# Main Program

while(True):
	isLeftTouch = robot.leftTouch.isTouch()
	isRightTouch = robot.rightTouch.isTouch()
	if(isLeftTouch or isRightTouch):
		robot.motors.forward(-30)
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
		robot.motors.setSpeed(150)
	time.sleep(0.01)
