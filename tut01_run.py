from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from  constants import *

robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, None, None)

# Main Program
# Left90deg()
for i in range(0, 4):
	robot.forward(42)
	time.sleep(1)
	robot.left90deg()
	time.sleep(1)

#robot.forward(40)
