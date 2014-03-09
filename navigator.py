from utilities import *
from math import *
from constants import *

ACCEPTABLE_ANGLE = degToRad(5)
ACCEPTABLE_ANGLE_LARGE = pi/12  # about 15 degress
ACCEPTABLE_ANGLE_SMALL = pi/36  # about 10 degress
ACCEPTABLE_DISTANCE = 3  # cm
NAV_FWD_VEL = 8
NAV_ROT_VEL = 6
NAV_ROT_VEL_LARGE = 6
NAV_ROT_VEL_SMALL = 6
BREAK_VEL = -0.1

class Navigator:
	def __init__(self):
		self.lastGoalPoint = (0, 0)
		self.navState = 'None'
		self.dToGo = 0
		self.dSignToGo = 0
		self.thToGo = 0
		self.thSignToGo = 0

	# def navigateToWayPoint(self, robotState, goalPoint):
	# 	#calculate angle different
	# 	dx = goalPoint[0] - robotState[0]
	# 	dy = goalPoint[1] - robotState[1]
	# 	prefer_th = atan2(dy, dx)
	# 	diffTh = toPIPI(prefer_th - robotState[2])
	# 	diffD = diffDist(robotState, goalPoint)
		
	# 	if(abs(diffD) <= ACCEPTABLE_DISTANCE):
	# 		return (0, 0, 'Complete')

	# 	KmeanV = (1.0/50)
	# 	KrotV = 180/pi	

	# 	meanV = limitTo(diffD*KmeanV, 6, 8)
	# 	rotV = limitTo(diffTh*KrotV, -20, 20)

	# 	print "V : ", meanV, rotV

	# 	leftVel = meanV - rotV
	# 	rightVel = meanV + rotV

	# 	return (leftVel, rightVel, 'Not Complete')
		


	# def navigateToWayPointStateFul(self, robotState, goalPoint):
	# 	if(self.lastGoalPoint != goalPoint): # just order to go to this point first time!
	# 		self.lastGoalPoint = goalPoint
	# 		self.navState = 'Rotate' # rotate first

	# 	#calculate angle different
	# 	dx = goalPoint[0] - robotState[0]
	# 	dy = goalPoint[1] - robotState[1]
	# 	prefer_th = atan2(dy, dx)
	# 	diffTh = toPIPI(prefer_th - robotState[2])
	# 	diffD = diffDist(robotState, goalPoint)


	# 	leftVel = 0
	# 	rightVel = 0
	# 	action = 'Stop'

	# 	if(abs(diffD) <= ACCEPTABLE_DISTANCE):
	# 		self.navState = 'Complete'
	# 		action = 'Complete'
	# 		return (leftVel, rightVel, action)

	# 	# set control command rotate
	# 	if(self.navState == 'Rotate'):
	# 		# check if the robot is at the goal angle
	# 		if(abs(diffTh) <= ACCEPTABLE_ANGLE_SMALL):
	# 			self.navState = 'Translate'
	# 		elif(abs(diffTh) <= ACCEPTABLE_ANGLE_LARGE):
	# 			# set control command
	# 			if(diffTh > 0):
	# 				action = 'Rotate'
	# 				leftVel = -NAV_ROT_VEL_SMALL
	# 				rightVel = NAV_ROT_VEL_SMALL
	# 			else:
	# 				action = 'Rotate'
	# 				leftVel = NAV_ROT_VEL_SMALL
	# 				rightVel = -NAV_ROT_VEL_SMALL
	# 		else:
	# 			# set control command
	# 			if(diffTh > 0):
	# 				action = 'Rotate'
	# 				leftVel = -NAV_ROT_VEL_LARGE
	# 				rightVel = NAV_ROT_VEL_LARGE
	# 			else:
	# 				action = 'Rotate'
	# 				leftVel = NAV_ROT_VEL_LARGE
	# 				rightVel = -NAV_ROT_VEL_LARGE
	# 	elif(self.navState == 'Translate'):
	# 		if(abs(diffTh) > ACCEPTABLE_ANGLE_LARGE):
	# 			self.navState = 'Rotate'
	# 		elif(abs(diffD) <= ACCEPTABLE_DISTANCE):
	# 			self.navState = 'Complete'
	# 			action = 'Complete'
	# 		else:
	# 			action = 'Forward'
	# 			leftVel = NAV_FWD_VEL
	# 			rightVel = NAV_FWD_VEL

	# 	#print "Diff (R, T) : ", diffTh*180/pi, diffTh
	# 	return (leftVel, rightVel, action)


		

	# def navigateToWayPointStateFul2(self, robotState, enc_distL, enc_distR, goalPoint):
	# 	#calculate angle different
	# 	dx = goalPoint[0] - robotState[0]
	# 	dy = goalPoint[1] - robotState[1]
	# 	prefer_th = atan2(dy, dx)
	# 	dth = toPIPI(prefer_th - robotState[2])

	# 	if(self.lastGoalPoint != goalPoint): # just order to go to this point first time!
	# 		self.lastGoalPoint = goalPoint
	# 		self.navState = 'Rotate' # rotate first
	# 		self.thToGo = dth
	# 		self.thSignToGo = sign(dth)

	# 	# set control command		 
	# 	if(self.navState == 'Rotate'):
	# 		# set new state
	# 		motionTH = (enc_distR - enc_distL)/(2*RW_DIST) #estamate moved angle
	# 		self.thToGo -= motionTH			

	# 		# check if the robot is at the goal angle
	# 		if(self.thToGo*self.thSignToGo <= ACCEPTABLE_ANGLE):
	# 			self.navState = 'Translate'
	# 			action = 'ToTranslate'
	# 			self.dToGo = diffDist(robotState, goalPoint)

	# 			# just break
	# 			if(self.thSignToGo > 0):
	# 				leftVel = -BREAK_VEL
	# 				rightVel = BREAK_VEL
	# 			else:
	# 				leftVel = BREAK_VEL
	# 				rightVel = -BREAK_VEL

	# 		else:
	# 			# set control command
	# 			if(self.thToGo > 0):
	# 				action = 'RotateCCW'
	# 				leftVel = -NAV_ROT_VEL
	# 				rightVel = NAV_ROT_VEL
	# 			else:
	# 				action = 'RotateCW'
	# 				leftVel = NAV_ROT_VEL
	# 				rightVel = -NAV_ROT_VEL
	# 	elif(self.navState == 'Translate'):
	# 		motionD  = (enc_distR + enc_distL)/2
	# 		self.dToGo -= motionD

	# 		if(self.dToGo <= 0):
	# 			self.navState = 'None'
	# 			action = 'Complete'

	# 			# just break
	# 			leftVel = BREAK_VEL
	# 			rightVel = BREAK_VEL
	# 		else:
	# 			action = 'Forward'
	# 			leftVel = NAV_FWD_VEL
	# 			rightVel = NAV_FWD_VEL
	# 	elif(self.navState == 'None'):
	# 			action = 'Complete'
	# 			leftVel = 0
	# 			rightVel = 0



	# 	print "What : ", action

	# 	# print "thToGo : ", self.thToGo
	# 	# if(self.navState == 'None'):
	# 	# 	action = 'Stop'
	# 	# 	leftVel = 0
	# 	# 	rightVel = 0

	# 	return (leftVel, rightVel, action)



	def navigateToWayPointStateFulPow(self, robotState, enc_distL, enc_distR, goalPoint):
		print "Power"
		#calculate angle different
		dx = goalPoint[0] - robotState[0]
		dy = goalPoint[1] - robotState[1]
		prefer_th = atan2(dy, dx)
		dth = toPIPI(prefer_th - robotState[2])

		# if change goal point
		if(self.lastGoalPoint != goalPoint):
			self.lastGoalPoint = goalPoint
			self.prepareRotate(dth)
			self.navState = 'Rotate' # rotate first
			leftPow = 0
			rightPow = 0
			action = 'Rotate'
		# rotate
		elif(self.navState == 'Rotate'):
			action = 'Rotate'
			leftPow, rightPow, complete = self.motorRotate(enc_distL, enc_distR)

			if(complete): # change to translate state
				dist = diffDist(robotState, goalPoint)
				self.prepareForward(dist)
				self.navState = 'Translate'
				action = 'Translate'
		# translate
		elif(self.navState == 'Translate'):
			action = 'Translate'
			leftPow, rightPow, complete = self.motorForward(enc_distL, enc_distR)

			if(complete): # change to complete state
				self.navState = 'None'
				action = 'Complete'
		else: #self.navState == 'None'
				action = 'Complete'
				leftPow = 0
				rightPow = 0

		print "Pow : ", leftPow, rightPow, action

		return (leftPow, rightPow, action)

# Function to move forward for a specified distance(in cm)
	def prepareForward(self, prefer_dist):
		print "Moving forward : ", prefer_dist, " cm"
		self.fpCurrentLeft = 0
		self.fpCurrentRight = 0
		self.fpCurrentDist = 0
		self.fpPreferDist = prefer_dist
		self.fpDummyPow = 0
		self.fpDummyWeight = 20
		self.fpDirSign = sign(prefer_dist)
		self.fpMainPow = 90

	def motorForward(self, enc_distL, enc_distR):
		# read data from encoder
 		self.fpCurrentLeft += enc_distL
 		self.fpCurrentRight += enc_distR
 		self.fpCurrentDist = (self.fpCurrentLeft + self.fpCurrentRight)/2

 		# set Dummy Power
 		self.fpDummyPow = (abs(self.fpCurrentRight) - abs(self.fpCurrentLeft))/2

	 	# check if it reaches the goal
	 	if(abs(self.fpCurrentDist) < abs(self.fpPreferDist)):
	 		# set the power
	 		leftPow = self.fpMainPow + self.fpDummyPow*self.fpDummyWeight
	 		rightPow = self.fpMainPow - self.fpDummyPow*self.fpDummyWeight

	 		# set to correct direction
	 		leftPow *= self.fpDirSign
	 		rightPow *= self.fpDirSign

	 		complete = False
	 	else: # brake
	 		leftPow = -5*self.fpDirSign
	 		rightPow = -5*self.fpDirSign
	 		complete = True

	 	return leftPow, rightPow, complete

	# Function to rotate for a specified angle (in radian)
	def prepareRotate(self, prefer_angle):
		self.rpCurrentLeft = 0
		self.rpCurrentRight = 0
		self.rpCurrentAngle = 0
		self.rpPreferAngle = prefer_angle
		self.rpDummyPow = 0
		self.rpDummyWeight = 40
		self.rpMainPow = 100
		self.rpDirSign = sign(prefer_angle)

	def motorRotate(self, enc_distL, enc_distR):
		# read data from encoder
		self.rpCurrentLeft += enc_distL
		self.rpCurrentRight += enc_distR
		self.rpCurrentAngle = (self.rpCurrentRight - self.rpCurrentLeft)/(2*RW_DIST)

		# set Dummy Power
		self.rpDummyPow = (abs(self.rpCurrentRight) - abs(self.rpCurrentLeft))/2

		if(abs(self.rpCurrentAngle) < abs(self.rpPreferAngle)):
			leftPow = -(self.rpMainPow + self.rpDummyPow*self.rpDummyWeight)
			rightPow = self.rpMainPow - self.rpDummyPow*self.rpDummyWeight

			# set to correct direction
		 	leftPow *= self.rpDirSign
		 	rightPow *= self.rpDirSign

		 	complete = False
		else:
			leftPow = 5*self.rpDirSign
			rightPow = -5*self.rpDirSign

			complete = True
		return leftPow, rightPow, complete

