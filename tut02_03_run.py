from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from  constants import *

robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, LEFT_TOUCH, RIGHT_TOUCH, SONAR_SENSOR)

# Main Program
acc_err = 0

robot.follow_wall(30)
