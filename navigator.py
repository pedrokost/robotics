from utilities import *
from math import *
from constants import *

ACCEPTABLE_ANGLE_LARGE = pi/12  # about 15 degress
ACCEPTABLE_ANGLE_SMALL = pi/36  # about 5 degress
ACCEPTABLE_DISTANCE = 1  # cm

NAV_FWD_VEL = 10
NAV_ROT_VEL = 3

class Navigator:
	def __init__(self):
		self.lastGoalPoint = (0, 0)
		self.navState = 'None'
		self.dToGo = 0
		self.thToGo = 0


	def navigateToWayPointStateFul(self, robotState, goalPoint):
		if(self.lastGoalPoint != goalPoint): # just order to go to this point first time!
			self.lastGoalPoint = goalPoint
			self.navState = 'Rotate' # rotate first

		#calculate angle different
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
		prefer_th = atan2(dy, dx)
		diffTh = toPIPI(prefer_th - robotState[2])
		diffD = diffDist(robotState, goalPoint)


		leftVel = 0
		rightVel = 0
		action = 'Stop'

		if(abs(diffD) <= ACCEPTABLE_DISTANCE):
			self.navState = 'Complete'
			action = 'Complete'
			return (leftVel, rightVel, action)

		# set control command rotate
		if(self.navState == 'Rotate'):
			# check if the robot is at the goal angle
			if(abs(diffTh) <= ACCEPTABLE_ANGLE_SMALL):
				self.navState = 'Translate'
			else:
				# set control command
				if(diffTh > 0):
					action = 'RotateCCW'
					leftVel = -NAV_ROT_VEL
					rightVel = NAV_ROT_VEL
				else:
					action = 'RotateCW'
					leftVel = NAV_ROT_VEL
					rightVel = -NAV_ROT_VEL
		elif(self.navState == 'Translate'):
			if(abs(diffTh) > ACCEPTABLE_ANGLE_LARGE):
				self.navState = 'Rotate'
			elif(abs(diffD) <= ACCEPTABLE_DISTANCE):
				self.navState = 'Complete'
				action = 'Complete'
			else:
				action = 'Forward'
				leftVel = NAV_FWD_VEL
				rightVel = NAV_FWD_VEL

		print "Diff (R, T) : ", diffTh*180/pi, diffTh
		return (leftVel, rightVel, action)


		

#	def navigateToWayPointStateFul(self, robotState, enc_distL, enc_distR, goalPoint):
#		#calculate angle different
#		dx = goalPoint[0] - robotState[0]
#		dy = goalPoint[1] - robotState[1]
#		prefer_th = atan2(dy, dx)
#		dth = toPIPI(prefer_th - robotState[2])	
#
#		if(self.lastGoalPoint != goalPoint): # just order to go to this point first time!
#			self.lastGoalPoint = goalPoint
#			self.navState = 'Rotate' # rotate first
#			self.thToGo = dth
#
#		# set control command		 
#		if(self.navState == 'Rotate'):
#			# set new state
#			motionTH = (enc_distR - enc_distL)/(2*RW_DIST) #estamate moved angle
#			self.thToGo -= motionTH			
#
#			# check if the robot is at the goal angle
#			if(abs(self.thToGo) <= ACCEPTABLE_ANGLE_SMALL):
#				self.navState = 'Translate'
#				self.dToGo = diffDist(robotState, goalPoint)
#			else:
#				# set control command
#				if(self.thToGo > 0):
#					action = 'RotateCCW'
#					leftVel = -NAV_ROT_VEL
#					rightVel = NAV_ROT_VEL
#				else:
#					action = 'RotateCW'
#					leftVel = NAV_ROT_VEL
#					rightVel = -NAV_ROT_VEL
#
#		
#		if(self.navState == 'Translate'):
#			motionD  = (enc_distR + enc_distL)/2
#			self.dToGo -= motionD
#
#			if(abs(self.dToGo) <= ACCEPTABLE_DISTANCE):
#				self.navState = 'None'
#			else:
#				action = 'Forward'
#				leftVel = NAV_FWD_VEL
#				rightVel = NAV_FWD_VEL
#
#		if(self.navState == 'None'):
#			action = 'Stop'
#			leftVel = 0
#			rightVel = 0
#
#		return (leftVel, rightVel, action)
#		

	def navigateToWayPoint(self, robotState, robotVelocity, goalPoint):
		"""
			This function is to obtain the proper control command (leftVel, rightVel) for navigating the robot from robotState(x, y, th) to goalPoint(x, y)
			robotStates = [x, y, theta]
			robotVelocity = [velL, velR]
			goalPoint = (x, y)

		"""
		velL, velR = robotVelocity  # current
		# calculate distance to goal point
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
		
		absolute_th = atan2(dy, dx)
		d_th = toPIPI(absolute_th - robotState[2])
		
		if(abs(d_th) >= ACCEPTABLE_ANGLE):
			if(d_th > 0):
				prefer_velL, prefer_velR = -NAV_ROT_VEL, NAV_ROT_VEL
			else:
				prefer_velL, prefer_velR = NAV_ROT_VEL, -NAV_ROT_VEL
		elif(sqrt(dx*dx + dy*dy) >= ACCEPTABLE_DISTANCE):
			prefer_velL, prefer_velR = NAV_FWD_VEL, NAV_FWD_VEL
		else:
			prefer_velL, prefer_velR = 0, 0

		print "prefer : ", prefer_velL, prefer_velR
		d_velL = (prefer_velL - velL) * GOAL_GREADYNESS
		d_velR = (prefer_velR - velR) * GOAL_GREADYNESS

		velL += d_velL
		velR += d_velR

		return velL, velR
