from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from particleFilter import *
from encoder import *
from random import uniform
from navigator import Navigator

def drawTrajectory(points):
	n = len(points)
	for i in range(0, n):
		x0 = DISPLAY_OFFSET_X + DISPLAY_SCALE_X*points[i][0]
		y0 = DISPLAY_OFFSET_Y + DISPLAY_SCALE_Y*points[i][1]
		x1 = DISPLAY_OFFSET_X + DISPLAY_SCALE_X*points[(i + 1)%n][0]
		y1 = DISPLAY_OFFSET_Y + DISPLAY_SCALE_Y*points[(i + 1)%n][1]
		print "drawLine:" + str((x0, y0, x1, y1))

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

#
# intialize environment
#
canvas = Canvas();
mymap = Map(canvas);
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
mymap.add_wall((0,0,0,168));        # a
mymap.add_wall((0,168,84,168));     # b
mymap.add_wall((84,126,84,210));    # c
mymap.add_wall((84,210,168,210));   # d
mymap.add_wall((168,210,168,84));   # e
mymap.add_wall((168,84,210,84));    # f
mymap.add_wall((210,84,210,0));     # g
mymap.add_wall((210,0,0,0));        # h
mymap.draw();

# initialize particle filter
particleFilter = ParticleFilter(mymap, canvas)

# initialize way points
wayPoints = [(40, 0), (40, 40), (0, 40), (0, 0)]
drawTrajectory(wayPoints)
currentPointIndex = 0

# initialize control command
leftVel = 0
rightVel = 0
lastAction = 'None'

while True:
	time.sleep(0.05)

	# get encoder data (for actual run)
	#enc_distL, enc_dtL = encoder.getMovingDistance(leftMotorPort);
	#enc_distR, enc_dtR = encoder.getMovingDistance(rightMotorPort);
	#enc_velL = enc_distL/enc_dtL;
	#enc_velR = enc_distR/enc_dtR;

	#print enc_distL
	# temp encoder data (for simulation only)
	temp_dt = 0.05;
	enc_velL = leftVel;
	enc_velR = rightVel;
	enc_distL = leftVel*temp_dt;
	enc_distR = rightVel*temp_dt;

	# measure from sonar
	#z = robot.sonar.getSmoothSonarDistance(0.05)
	z = particleFilter.getIdealM()

	# motion update
	particleFilter.motionUpdate(enc_distL, enc_distR)

	# measurement update
	particleFilter.measurementUpdate(z)

	particleFilter.normalizeWeights()

	particleFilter.resample()

	# get predict state
	robotState = particleFilter.getPredictState()

	# set control signal
	#leftVel, rightVel, action = navigator.navigateToWayPoint(robotState, wayPoints[currentPointIndex])
	leftVel, rightVel, action = navigator.navigateToWayPointStateFul(robotState, enc_distL, enc_distR, wayPoints[currentPointIndex])
	if action is not lastAction:
		robot.motors.reset()
	lastAction = action

	robot.motors.setVel(leftVel, rightVel, enc_velL, enc_velR)

	# set waypoint index
	if(abs(leftVel) < NEAR_ZERO and abs(rightVel) < NEAR_ZERO):
		currentPointIndex += 1
		if(currentPointIndex >= len(wayPoints)):
			break

	# draw particle
	particleFilter.drawParticles()

