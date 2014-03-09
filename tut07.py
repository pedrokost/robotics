from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from particleFilter import *
from encoder import *
from random import uniform
from navigator import Navigator
from math import cos, sin, atan2
from utilities import *
from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer
from place_recognizer import PlaceRecognizer
from sonarScanner import SonarScanner
from BrickPi import BrickPiSetup, PORT_4, PORT_D, BrickPiSetupSensors


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

# initialize way points
wayPoints = [(84, 30), (180,30), (180,54), (126, 54), (126, 168), (126, 126), (30, 54), (84, 54), (84, 30)]

def interpolate(points):
	p = points[0]
	newPoints = []
	for i in xrange(1, len(points)):
		newPoints.append(p)
		p2 = points[i]

		theta = atan2(p2[1] - p[1], p2[0] - p[0])

		tmpp = p
		while diffDist(p2, tmpp) > 15:
			newp = (tmpp[0] + 15*cos(theta), tmpp[1] + 15*sin(theta))

			newPoints.append(newp)
			tmpp = newp
		p = p2

	return newPoints

wayPoints = interpolate(wayPoints)

print wayPoints
#wayPoints = [(84, 30), (126,30), (126, 54), (126, 168), (126, 126), (30, 54), (84, 54), (84, 30)]
drawTrajectory(wayPoints)
currentPointIndex = 1

# TODO
# Where am I need to come in here
container = SignatureContainer()
recognizer = SignatureRecognizer(container)
sonarScanner = SonarScanner(PORT_4, PORT_D)
BrickPiSetupSensors()

placeRecognizer = PlaceRecognizer({
	'sonarScanner': sonarScanner,
	'signatureRecognizer': recognizer,
	'accurateScan': False,
	'accurateRecognition': True,
})
wayPoint, theta = placeRecognizer.whereAmI()


# initialize particle filter
particleFilter = ParticleFilter(mymap, canvas, (84, 30, 0))


# initialize control command
leftVel = 0
rightVel = 0
lastAction = 'None'
action = 'None'

timeStep = 0
while True:
	timeStep += 1
	time.sleep(0.001)

	# get encoder data (for actual run)
	enc_distL, enc_dtL = encoder.getMovingDistance(leftMotorPort);
	enc_distR, enc_dtR = encoder.getMovingDistance(rightMotorPort);
	enc_velL = enc_distL/enc_dtL;
	enc_velR = enc_distR/enc_dtR;

	#print enc_distL
	# temp encoder data (for simulation only)
	#temp_dt = 0.05;
	#enc_velL = leftVel;
	#enc_velR = rightVel;
	#enc_distL = leftVel*temp_dt;
	#enc_distR = rightVel*temp_dt;

	# measure from sonar
	# z = robot.sonar.getSmoothSonarDistance(0.05)
	print "Measurement : FAKE"
	z = particleFilter.getIdealM()

	# motion update
	particleFilter.motionUpdate(enc_distL, enc_distR)
	
	# get predict state
	robotState = particleFilter.getPredictState()
	# set control signal	
	leftVel, rightVel, action = navigator.navigateToWayPointStateFul2(robotState, enc_distL, enc_distR, wayPoints[currentPointIndex])
	robot.motors.setVel(leftVel, rightVel, enc_velL, enc_velR)

	# predict new state
	z_angle = 0
	if(timeStep > 1):
		nextState = predictState(robotState, enc_distL, enc_distR)
		m, z_angle = particleFilter._get_predict_m_beta(nextState[0], nextState[1], nextState[2])

	# measurement update
	if(z < 100 and z > 20 and abs(radToDeg(z_angle)) < 45):
		z -= 13
		print "Until Move to center"
		particleFilter.measurementUpdate(z)
		particleFilter.normalizeWeights()

	# get predict state
	robotState = particleFilter.getPredictState()
	# set control signal
	leftVel, rightVel, action = navigator.navigateToWayPointStateFul2(robotState, enc_distL, enc_distR, wayPoints[currentPointIndex])
	robot.motors.setVel(leftVel, rightVel, enc_velL, enc_velR)
	#leftVel, rightVel, action = navigator.navigateToWayPointStateFul2((0, 0, 0), enc_distL, enc_distR, (0, 5))
	#print "Command : ", leftVel, rightVel
	print "State : ", int(robotState[0]), radToDeg(robotState[2])

	#if action is not lastAction:
	#	robot.motors.reset()
	#lastAction = action

	

	# set waypoint index
	if(action == 'Complete'):
		currentPointIndex += 1
		if(currentPointIndex >= len(wayPoints)):
			break
	
	# resampling
	if(timeStep%RESAMPLING_PERIOD == 0):
		particleFilter.resample()

	# draw particle
	if(timeStep%DRAWING_PERIOD == 0):
		particleFilter.drawParticles()

