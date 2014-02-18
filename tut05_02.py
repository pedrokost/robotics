from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from particleFilter import *
from encoder import *
from random import uniform
from navigator import Navigator

robot = Robot(leftMotorPort=LEFT_MOTOR,
			rightMotorPort=RIGHT_MOTOR,
			leftTouchPort=LEFT_TOUCH,
			rightTouchPort=RIGHT_TOUCH,
			sonarPort=SONAR_SENSOR)

encoder = Encoder()
navigator = Navigator()

# initialize particle filter
particleFilter = ParticleFilter()
particleFilter.initialize()

# initialize way points
wayPoints = [(84, 30), (180,30), (180,54), (126, 54), (126, 168), (126, 126), (30, 54), (84, 54), (84, 30)]

drawTrajectory(wayPoints)
currentPointIndex = 0

leftVel = 0
rightVel = 0

lastAction = 'None'


currentWaypoint = wayPoints.pop(0)
for wayPoint in wayPoints:
	# measure
	# do motion update
	# resample




while True:
	time.sleep(0.05)

	# get encoder data (for actual run)
	distL, velL = encoder.getMovingDistanceAndVelocity(leftMotorPort);
	distR, velR = encoder.getMovingDistanceAndVelocity(rightMotorPort);

	particleFilter.motionUpdate(distL, distR)
	particleFilter.measurementUpdate()
	particleFilter.normalizeWeights()
	particleFilter.resample()

	# get predict state
	robotState = particleFilter.getPredictState()

	# set control signal
	#leftVel, rightVel, action = navigator.navigateToWayPoint(robotState, wayPoints[currentPointIndex])
	leftVel, rightVel, action = navigator.navigateToWayPointStateFul(robotState, distL, distR, wayPoints[currentPointIndex])
	if action is not lastAction:
		robot.motors.reset()
	lastAction = action

	robot.motors.setVel(leftVel, rightVel, velL, velR)

	# set waypoint index
	if(abs(leftVel) < NEAR_ZERO and abs(rightVel) < NEAR_ZERO):
		currentPointIndex += 1
		if(currentPointIndex >= len(wayPoints)):
			break

	# draw particle
	particleFilter.drawParticles()

