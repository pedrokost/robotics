from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from constants import *
from robot import Robot

BrickPiSetup()
robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, None, None, None)
BrickPiSetupSensors()

# Main Program
for i in range(0, 4):
	robot.motors.forward(42, FWD_VEL)
	time.sleep(1)
	robot.motors.left90deg()
	time.sleep(1)
