from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from  constants import *


robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, LEFT_TOUCH, RIGHT_TOUCH, SONAR_SENSOR)

# Main Program
prefer_dist = 30

while(True):
	robot.follow(prefer_dist)
