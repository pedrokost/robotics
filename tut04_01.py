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

leftVel = 0
rightVel = 0

while True:
	time.sleep(0.1)

	# get encoder data (for actual run)
	#enc_distL, enc_dtL = encoder.getMovingDistance(leftMotorPort);
	#enc_distR, enc_dtR = encoder.getMovingDistance(rightMotorPort);
	#enc_velL = enc_distL/enc_dtL;
	#enc_velR = enc_distR/enc_dtL;

	# temp encoder data (for simulation only)
	temp_dt = 0.5;
	enc_velL = leftVel;
	enc_velR = rightVel;
	enc_distL = leftVel*temp_dt;
	enc_distR = rightVel*temp_dt;


	# motion update
	particleFilter.motionUpdate(enc_distL, enc_distR)

	# measurement update
	particleFilter.measurementUpdate()

	# get predict state
	robotState = particleFilter.getPredictState()

	print "Current State : ", robotState[0], robotState[1], robotState[2]
	print "Goal : ", currentPointIndex, wayPoints[currentPointIndex][0], wayPoints[currentPointIndex][1]

	# set control signal
	leftVel, rightVel = navigator.navigateToWaypoint(robotState, wayPoints[currentPointIndex])
	robot.motors.setVel(leftVel, rightVel, enc_velL, enc_velR)

	# set waypoint index
	if(abs(leftVel) < NEAR_ZERO and abs(rightVel) < NEAR_ZERO):
		currentPointIndex += 1
		if(currentPointIndex >= len(wayPoints)):
			break

	# draw particle
	particleFilter.drawParticles()

