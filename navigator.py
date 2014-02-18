from utilities import *
from math import *
from constants import *

ACCEPTABLE_ANGLE = pi/180  # about 1 degress
ACCEPTABLE_DISTANCE = 1  # cm

NAV_FWD_VEL = 5
NAV_ROT_VEL = 3

class Navigator:
	def __init__(self):
		self.lastGoalPoint = (0, 0)
		self.navState = 'None'
		self.dToGo = 0
		self.thToGo = 0

	def navigateToWayPointStateFul(self, robotState, enc_distL, enc_distR, goalPoint):
		if(self.lastGoalPoint != goalPoint): # just order to go to this point first time!
			self.lastGoalPoint = goalPoint
			self.navState = 'Rotate' # rotate first
			dx = goalPoint[0] - robotState[0]
			dy = goalPoint[1] - robotState[1]
	
			prefer_th = atan2(dy, dx)
			self.thToGo = toPIPI(prefer_th - robotState[2])	

		# set control command		 
		if(self.navState == 'Rotate'):
			# set new state
			motionTH = (enc_distR - enc_distL)/(2*RW_DIST) #estamate moved angle
			self.thToGo -= motionTH			

			# check if the robot is at the goal angle
			if(abs(self.thToGo) <= ACCEPTABLE_ANGLE):
				self.navState = 'Translate'
				self.dToGo = diffDist(robotState, goalPoint)
			else:
				# set control command
				if(self.thToGo > 0):
					action = 'RotateCCW'
					leftVel = -NAV_ROT_VEL
					rightVel = NAV_ROT_VEL
				else:
					action = 'RotateCW'
					leftVel = NAV_ROT_VEL
					rightVel = -NAV_ROT_VEL

		
		if(self.navState == 'Translate'):
			motionD  = (enc_distR + enc_distL)/2
			self.dToGo -= motionD

			if(abs(self.dToGo) <= ACCEPTABLE_DISTANCE):
				self.navState = 'None'
			else:
				action = 'Forward'
				leftVel = NAV_FWD_VEL
				rightVel = NAV_FWD_VEL

		if(self.navState == 'None'):
			action = 'Stop'
			leftVel = 0
			rightVel = 0

		return (leftVel, rightVel, action)
		

	def navigateToWayPoint(self, robotState, goalPoint):
		"""
			This function is to obtain the proper control command (leftVel, rightVel) for 		                navigating the robot from robotState(x, y, th) to goalPoint(x, y)
		"""
		# calculate distance to goal point
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
	
		prefer_th = atan2(dy, dx)
		d_th = toPIPI(prefer_th - robotState[2])
	
		# check if angle error is within acceptable region
		if(abs(d_th) >= ACCEPTABLE_ANGLE):
			if(d_th > 0):
				action = ACTION_ROTATE_CCW
				leftVel, rightVel = -NAV_ROT_VEL, NAV_ROT_VEL
			else:
				action = ACTION_ROTATE_CW
				leftVel, rightVel = NAV_ROT_VEL, -NAV_ROT_VEL
		elif(sqrt(dx*dx + dy*dy) >= ACCEPTABLE_DISTANCE):
			action = ACTION_FORWARD
			leftVel, rightVel = NAV_FWD_VEL, NAV_FWD_VEL
		else:
			action = ACTION_STOP
			leftVel, rightVel = 0, 0

		return (leftVel, rightVel, action)
