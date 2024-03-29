from utilities import *
from math import *
from constants import *

ACCEPTABLE_ANGLE_LARGE = pi/12  # about 5 degress
ACCEPTABLE_ANGLE_SMALL = pi/36  # about 1 degress
ACCEPTABLE_DISTANCE = 3  # cm
NAV_FWD_VEL = 10
NAV_ROT_VEL = 7
NAV_ROT_VEL_LARGE = 4
NAV_ROT_VEL_SMALL = 4

class Navigator:
	def __init__(self):
		self.lastGoalPoint = (0, 0)
		self.navState = 'None'
		self.dToGo = 0
		self.dSignToGo = 0
		self.thToGo = 0
		self.thSignToGo = 0

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
			# print "I AM DESPERATE"
			# for x in xrange(1,20):
			# 	BrickPi.MotorSpeed[LEFT_MOTOR] = FWD_SIGN*int(round(150))
			# 	BrickPi.MotorSpeed[RIGHT_MOTOR] = FWD_SIGN*int(round(150))
			# 	BrickPiUpdateValues()
			# 	time.sleep(0.05)
			self.navState = 'Complete'
			action = 'Complete'
			return (leftVel, rightVel, action)

		# set control command rotate
		if(self.navState == 'Rotate'):
			# check if the robot is at the goal angle
			if(abs(diffTh) <= ACCEPTABLE_ANGLE_SMALL):
				self.navState = 'Translate'
			elif(abs(diffTh) <= ACCEPTABLE_ANGLE_LARGE):
				# set control command
				if(diffTh > 0):
					action = 'Rotate'
					leftVel = -NAV_ROT_VEL_SMALL
					rightVel = NAV_ROT_VEL_SMALL
				else:
					action = 'Rotate'
					leftVel = NAV_ROT_VEL_SMALL
					rightVel = -NAV_ROT_VEL_SMALL
			else:
				# set control command
				if(diffTh > 0):
					action = 'Rotate'
					leftVel = -NAV_ROT_VEL_LARGE
					rightVel = NAV_ROT_VEL_LARGE
				else:
					action = 'Rotate'
					leftVel = NAV_ROT_VEL_LARGE
					rightVel = -NAV_ROT_VEL_LARGE
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

		#print "Diff (R, T) : ", diffTh*180/pi, diffTh
		return (leftVel, rightVel, action)


		

	def navigateToWayPointStateFul2(self, robotState, enc_distL, enc_distR, goalPoint):
		#calculate angle different
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
		prefer_th = atan2(dy, dx)
		dth = toPIPI(prefer_th - robotState[2])
		#if(abs(prefer_th - robotState[2]) >= pi):
		#	dth = -dth

		leftVel = 0
		rightVel = 0

		if(self.lastGoalPoint != goalPoint): # just order to go to this point first time!
			self.lastGoalPoint = goalPoint
			self.navState = 'Rotate' # rotate first
			self.thToGo = dth
			self.thSignToGo = sign(dth)

		# set control command		 
		if(self.navState == 'Rotate'):
			# set new state
			motionTH = (enc_distR - enc_distL)/(2*RW_DIST) #estamate moved angle
			self.thToGo -= motionTH			

			# check if the robot is at the goal angle
			if(self.thToGo*self.thSignToGo <= 0):
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

			if(self.dToGo <= 0):
				self.navState = 'None'
				action = 'Complete'
			else:
				action = 'Forward'
				rightVel = NAV_FWD_VEL

		# if(self.navState == 'None'):
		# 	action = 'Stop'
		# 	leftVel = 0
		# 	rightVel = 0

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
