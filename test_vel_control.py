from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from particleFilter import *
from encoder import *
from random import uniform
from navigator import Navigator

leftMotorPort=LEFT_MOTOR
rightMotorPort=RIGHT_MOTOR

robot = Robot(leftMotorPort,
		rightMotorPort,
		leftTouchPort=LEFT_TOUCH,
		rightTouchPort=RIGHT_TOUCH,
		sonarPort=SONAR_SENSOR)

encoder = Encoder()

while True:
	time.sleep(0.05)

	# get encoder data (for actual run)
	enc_distL, enc_dtL = encoder.getMovingDistance(leftMotorPort);
	enc_distR, enc_dtR = encoder.getMovingDistance(rightMotorPort);
	enc_velL = enc_distL/enc_dtL;
	enc_velR = enc_distR/enc_dtL;

	print "Left vel : ", enc_velL
	print "Right vel : ", enc_velR

	# set control signal
	leftVel = -20
	rightVel = 20
	robot.motors.setVel(leftVel, rightVel, enc_velL, enc_velR)
