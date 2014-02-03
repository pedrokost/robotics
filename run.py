from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import robot


BrickPiSetup()  # setup the serial port for communication

robot = Robot()

# Main Program
# Left90deg()
for i in range(0, 4):
	robot.forward(42)
	time.sleep(1)
	robot.left90deg()
	time.sleep(1)

#robot.forward(40)