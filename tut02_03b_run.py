from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from random import uniform

robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, LEFT_TOUCH, RIGHT_TOUCH, SONAR_SENSOR)

# Main Program
acc_err = 0
last_err = 0

while(True):
	isLeftTouch = robot.leftTouch.isTouch()
	isRightTouch = robot.rightTouch.isTouch()
	if(isLeftTouch or isRightTouch):
		robot.motors.forward(-30)
		robot.motors.right90deg()
	else:
		acc_err, last_err =robot._follow_wall_step(30, acc_err, last_err)
