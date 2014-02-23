from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from particleFilter import *
from encoder import *
from math import *
from random import uniform
from navigator import Navigator

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
mymap.add_wall((80,0,80,150));      
mymap.draw();

canvas.drawLine((60,0,60,100))
canvas.drawLine((50,0,50,100))

# initialize particle filter
particleFilter = ParticleFilter(mymap, canvas, (50, 50, 0))


# initialize control command
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
	z = robot.sonar.getSmoothSonarDistance(0.05)
	print "Measurement : ", z
	#z = particleFilter.getIdealM()

	# motion update
	particleFilter.motionUpdate(enc_distL, enc_distR)

	# measurement update
	if(z > 0):
		particleFilter.measurementUpdate(z)
		particleFilter.normalizeWeights()
	

	# get predict state
	robotState = particleFilter.getPredictState()

	print "State : ", int(robotState[0]), int(robotState[1]), int(robotState[2]*180/pi)

	# set control signal
	robot.motors.setVel(0, 0, enc_velL, enc_velR)

	# resampling
	if(timeStep%RESAMPLING_PERIOD == 0):
		particleFilter.resample()

	# draw particle
	if(timeStep%DRAWING_PERIOD == 0):
		particleFilter.drawParticles()

