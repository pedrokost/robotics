from utilities import *
from math import *

ACCEPTABLE_ANGLE = math.pi/36
ACCEPTABLE_DISTANCE = 2

NAV_FWD_VEL = 25
NAV_ROT_VEL = 5

class Navigator:
	def navigateToWaypoint(self, robotState, goalPoint):
		"""
			This function is to obtain the proper control command (leftVel, rightVel) for 		                navigating the robot from robotState(x, y, th) to goalPoint(x, y)
		"""

		leftVel = NAV_FWD_VEL
		rightVel = NAV_FWD_VEL
		return (leftVel, rightVel)
		# calculate different from goal point
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
	
		prefer_th = atan2(dy, dx)
		d_th = toPIPI(prefer_th - robotState[2])

		# check if angle error is within acceptable region
		if(abs(d_th) >= ACCEPTABLE_ANGLE):
			if(d_th > 0):
				leftVel = -NAV_ROT_VEL
				rightVel = NAV_ROT_VEL
			else:
				leftVel = NAV_ROT_VEL
				rightVel = -NAV_ROT_VEL
		elif(sqrt(dx*dx + dy*dy) >= ACCEPTABLE_DISTANCE):
			leftVel = NAV_FWD_VEL
			rightVel = NAV_FWD_VEL
		else:
			leftVel = 0
			rightVel = 0

		return (leftVel, rightVel)
