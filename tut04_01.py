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
navigator = Navigator()

# initialize particle filter
particleFilter = ParticleFilter()
particleFilter.initialize()

# initialize way points
wayPoints = [(40, 0), (40, 40), (0, 40), (0, 0)]
currentPointIndex = 0

while True:
	# get encoder data
	enc_distL, enc_dtL = encoder.getMovingDistance(leftMotorPort);
	enc_distR, enc_dtR = encoder.getMovingDistance(rightMotorPort);
	enc_velL = enc_distL/enc_dtL;
	enc_velR = enc_distR/enc_dtL;

	# motion update
	particleFilter.motionUpdate(enc_distL, enc_distR)

	# measurement update
	particleFilter.measurementUpdate()

	# get predict state
	robotState = particleFilter.getPredictState()

	# set waypoint index

	# set control signal
	leftVel, rightVel = navigator.navigateToWaypoint(robotState, wayPoints[currentPointIndex])
	robot.motors.setVel(leftVel, rightVel, enc_velL, enc_velR)

	# draw particle
	particleFilter.drawParticles()

