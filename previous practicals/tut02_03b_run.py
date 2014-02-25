from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from random import uniform

robot = Robot(leftMotorPort=LEFT_MOTOR,
			  rightMotorPort=RIGHT_MOTOR,
			  leftTouchPort=LEFT_TOUCH,
			  rightTouchPort=RIGHT_TOUCH,
			  sonarPort=SONAR_SENSOR)

# Main Program
acc_err = 0
last_err = 0
last_dist = 0

while(True):
	isLeftTouch = robot.leftTouch.isTouch()
	isRightTouch = robot.rightTouch.isTouch()
	if(isLeftTouch or isRightTouch):
		robot.motors.forward(-30)
		robot.motors.right90deg()
	else:
		acc_err, last_err, last_diff_vel =robot.followWallStep(30, acc_err, last_err, last_dist)
