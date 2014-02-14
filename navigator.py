from utilities import *
from math import *

ACCEPTABLE_ANGLE = math.pi/36  # about 5 degress
ACCEPTABLE_DISTANCE = 2  # cm

NAV_FWD_VEL = 25
NAV_ROT_VEL = 15

class Navigator:
	def navigateToWaypoint(self, robotState, goalPoint):
		"""
			This function is to obtain the proper control command (leftVel, rightVel) for 		                navigating the robot from robotState(x, y, th) to goalPoint(x, y)
		"""

		# calculate different from goal point
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
	
		prefer_th = atan2(dy, dx)
		d_th = toPIPI(prefer_th - robotState[2])

		#print "Prefer TH: ", prefer_th*180/pi
		#print "DT : ", d_th*180/pi
		# check if angle error is within acceptable region
		if(abs(d_th) >= ACCEPTABLE_ANGLE):
			print "Rotate"
			action = 'rotate'
			if(d_th > 0):
				leftVel = -NAV_ROT_VEL
				rightVel = NAV_ROT_VEL
			else:
				leftVel = NAV_ROT_VEL
				rightVel = -NAV_ROT_VEL
		elif(sqrt(dx*dx + dy*dy) >= ACCEPTABLE_DISTANCE):
			action = 'forward'
			leftVel = NAV_FWD_VEL
			rightVel = NAV_FWD_VEL
		else:
			action = 'stop'
			leftVel = 0
			rightVel = 0

		return (leftVel, rightVel, action)
