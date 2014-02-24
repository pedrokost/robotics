from utilities import *
from math import *
from constants import *

ACCEPTABLE_ANGLE_LARGE = degToRad(20)  # about 5 degress
ACCEPTABLE_ANGLE_SMALL = degToRad(10)  # about 1 degress
ACCEPTABLE_DISTANCE = 3  # cm
NAV_FWD_VEL = 8
NAV_ROT_VEL_LARGE = 6
NAV_ROT_VEL_SMALL = 3

class Navigator:
	def __init__(self):
		self.lastGoalPoint = (0, 0)
		self.navState = 'None'
		self.dToGo = 0
		self.thToGo = 0

		# substate for rotate and translate exactly
		self.dAbsToGo = 0
		self.dSign = 0
		self.thAbsToGo = 0
		self.thSign = 0
		self.navSubState = 'None'


	def rotateX(self, x, enc_distL, enc_distR):	
		if(self.navSubState != 'RotateX'):
			self.navSubState = 'RotateX'
			self.thAbsToGo = abs(x)
			self.thSign = sign(x)
			return (0, 0, 'RotateX')  			
		
		if(self.thAbsToGo < 0):
			self.navSubState = 'Complete'
			return (0, 0, 'Complete')  			

		motionTH = (enc_distR - enc_distL)/(2*RW_DIST)
		self.thAbsToGo -= abs(motionTH)

		return (-self.thSign*NAV_ROT_VEL_SMALL, self.thSign*NAV_ROT_VEL_SMALL, 'RotateX')

	def translateX(self, x, enc_distL, enc_distR):	
		if(self.navSubState != 'translateX'):
			self.navSubState = 'translateX'
			self.dAbsToGo = abs(x)
			self.dSign = sign(x)
			return (0, 0, 'translateX')  			
		
		if(self.dAbsToGo < 0):
			self.navSubState = 'Complete'
			return (0, 0, 'Complete')  			

		motionD = (enc_distR + enc_distL)/2
		self.dAbsToGo -= abs(motionD)

		return (self.dSign*NAV_FWD_VEL, self.dSign*NAV_FWD_VEL, 'RotateX')

	def navigateToWayPoint(self, robotState, goalPoint):
		#calculate angle different
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
		prefer_th = atan2(dy, dx)
		diffTh = toPIPI(prefer_th - robotState[2])
		diffD = diffDist(robotState, goalPoint)
		
		if(abs(diffD) <= ACCEPTABLE_DISTANCE):
			return (0, 0, 'Complete')

		KmeanV = (1.0/50)
		KrotV = 180/pi	

		meanV = limitTo(diffD*KmeanV, 6, 8)
		rotV = limitTo(diffTh*KrotV, -20, 20)

		print "V : ", meanV, rotV

		leftVel = meanV - rotV
		rightVel = meanV + rotV

		return (leftVel, rightVel, 'Not Complete')
		


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
				if abs(diffTh) <= ACCEPTABLE_ANGLE_LARGE:
					vel = NAV_ROT_VEL_SMALL
				else:
					vel = NAV_ROT_VEL_LARGE
				# set control command
				if(diffTh > 0):
					action = 'Rotate'
					leftVel = -vel
					rightVel = vel
				else:
					action = 'Rotate'
					leftVel = vel
					rightVel = -vel
		elif(self.navState == 'Translate'):
			if(abs(diffTh) > ACCEPTABLE_ANGLE_LARGE):
				self.navState = 'Rotate'
			else:
				action = 'Forward'
				leftVel = NAV_FWD_VEL
				rightVel = NAV_FWD_VEL

		#print "Diff (R, T) : ", diffTh*180/pi, diffTh
		return (leftVel, rightVel, action)


		

	def navigateToWayPointStateFul2(self, robotState, enc_distL, enc_distR, goalPoint):
		#calculate angle different
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
		prefer_th = atan2(dy, dx)
		dth = toPIPI(prefer_th - robotState[2])	

		if(self.lastGoalPoint != goalPoint): # just order to go to this point first time!
			self.lastGoalPoint = goalPoint
			self.navState = 'Rotate' # rotate first
			self.thToGo = dth

		# set control command		 
		if(self.navState == 'Rotate'):
			# set new state
			motionTH = (enc_distR - enc_distL)/(2*RW_DIST) #estamate moved angle
			self.thToGo -= motionTH			

			# check if the robot is at the goal angle
			if(abs(self.thToGo) <= ACCEPTABLE_ANGLE_SMALL):
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
#		
#
#	def navigateToWayPoint(self, robotState, robotVelocity, goalPoint):
#		"""
#			This function is to obtain the proper control command (leftVel, rightVel) for navigating the robot from robotState(x, y, th) to goalPoint(x, y)
#			robotStates = [x, y, theta]
#			robotVelocity = [velL, velR]
#			goalPoint = (x, y)
#
#		"""
#		velL, velR = robotVelocity  # current
#		# calculate distance to goal point
#		dx = goalPoint[0] - robotState[0]
#		dy = goalPoint[1] - robotState[1]
#		
#		absolute_th = atan2(dy, dx)
#		d_th = toPIPI(absolute_th - robotState[2])
#		
#		if(abs(d_th) >= ACCEPTABLE_ANGLE):
#			if(d_th > 0):
#				prefer_velL, prefer_velR = -NAV_ROT_VEL, NAV_ROT_VEL
#			else:
#				prefer_velL, prefer_velR = NAV_ROT_VEL, -NAV_ROT_VEL
#		elif(sqrt(dx*dx + dy*dy) >= ACCEPTABLE_DISTANCE):
#			prefer_velL, prefer_velR = NAV_FWD_VEL, NAV_FWD_VEL
#		else:
#			prefer_velL, prefer_velR = 0, 0
#
#		print "prefer : ", prefer_velL, prefer_velR
#		d_velL = (prefer_velL - velL) * GOAL_GREADYNESS
#		d_velR = (prefer_velR - velR) * GOAL_GREADYNESS
#
#		velL += d_velL
#		velR += d_velR
#
#		return velL, velR
