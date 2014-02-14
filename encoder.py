from BrickPi import *
import math
from constants import *
from utilities import toPIPI

class Encoder:
	prev_radianL = 0
	prev_radianR = 0

	def __init__(self):
		self.reset();
		pass

	def getAngle(self, motor_port):
		"""
		Function to get encoder angle (in radian)
		"""
		BrickPiUpdateValues()
		degree = ( BrickPi.Encoder[motor_port] % 720 ) * 0.5
		radian = toPIPI( degree * math.pi / 180 )
		return radian

	def getMovingDistance(self, motor_port):
		"""
		Function to change encoder steps into distance(in cm)Current distance 36.0759556387
		"""
		current_radian = self.getAngle(motor_port)
		current_time = time.time()
		if(motor_port == LEFT_MOTOR):
			dt = current_time - self.prev_timeL
			dth = toPIPI(current_radian - self.prev_radianL)
			distance = dth * W_RADIUS
			#print "*********************************************"
			#print current_radian*180/math.pi
			#print self.prev_radianL*180/math.pi
			#print (current_radian - self.prev_radianL)*180/math.pi
			#print dth*180/math.pi
			if(dth > 3): print "Shoot!"
			self.prev_radianL = current_radian
			self.prev_timeL = current_time
		else:	
			dt = current_time - self.prev_timeR
			dth = toPIPI(current_radian - self.prev_radianR)
			distance = dth * W_RADIUS
			#print "R : ", current_radian - self.prev_radianR
			self.prev_radianR = current_radian
			self.prev_timeR = current_time
		return (FWD_SIGN*distance, dt)

	def reset(self):
		"""
		Reset the encoder. By storing the current values, we can get following measurments relative to this one.
		"""
		self.prev_radianL = self.getAngle(LEFT_MOTOR)
		self.prev_radianR = self.getAngle(RIGHT_MOTOR)
		current_time = time.time()
		self.prev_timeL = current_time
		self.prev_timeR = current_time
