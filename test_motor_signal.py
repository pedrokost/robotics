from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from particleFilter import *
from encoder import *
from random import uniform
from navigator import Navigator

def drawTrajectory(points):
	n = len(points)
	for i in range(0, n - 1):
		canvas.drawLine((points[i][0], points[i][1], points[(i + 1)%n][0], points[(i + 1)%n][1]));

#
# initialize device
#
leftMotorPort=LEFT_MOTOR
rightMotorPort=RIGHT_MOTOR

robot = Robot(leftMotorPort,
		rightMotorPort,
		leftTouchPort=LEFT_TOUCH,
		rightTouchPort=RIGHT_TOUCH,
		sonarPort=SONAR_SENSOR)

encoder = Encoder()
navigator = Navigator()

timeStep = 0
power = -260
num_test = 5
maxSleep = 30
tSleep = 0

robot.motors._setMotorPower(leftMotorPort, power)
robot.motors._setMotorPower(rightMotorPort, power)

datafile = open('motor_data.txt', 'w')

while power < 255:
	# set motor signal
	robot.motors._setMotorPower(leftMotorPort, power)
	robot.motors._setMotorPower(rightMotorPort, power)

	# get encoder data (for actual run)
	enc_distL, enc_dtL = encoder.getMovingDistance(leftMotorPort);
	enc_distR, enc_dtR = encoder.getMovingDistance(rightMotorPort);
	enc_velL = enc_distL/enc_dtL;
	enc_velR = enc_distR/enc_dtR;

	if(tSleep != 0):
		tSleep -= 1
		time.sleep(0.05)
		continue

	time.sleep(0.1)


	# write data
	datafile.write(str(power))
	datafile.write(" ")
	datafile.write(str(enc_velL))
	datafile.write(" ")
	datafile.write(str(enc_velR))
	datafile.write("\n")

	print power, enc_velL, enc_velR


	if(timeStep%num_test == 0):
		power += 10
		robot.motors._setMotorPower(leftMotorPort, power)
		robot.motors._setMotorPower(rightMotorPort, power)
		tSleep = maxSleep
		print "sleep..."
	
	timeStep += 1

datafile.close()

	
