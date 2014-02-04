from BrickPi import *
import math
from constants import *
from utilities import toPIPI

class Encoder:
	prev_radianL = 0
	prev_radianR = 0

	def __init__(self):
		pass

	def getAngle(self, motor_port):
		"""
		Function to get encoder angle (in radian)
		"""
		BrickPiUpdateValues()
		degree = ( BrickPi.Encoder[motor_port] % 720 ) * 0.5
		radian = ( degree * math.pi / 180 )
		return radian


	def getMovingDistance(self, motor_port):
		"""
		Function to change encoder steps into distance(in cm)Current distance 36.0759556387
		"""
		current_radian = self.getAngle(motor_port)
		if(motor_port == LEFT_MOTOR):	
			distance = toPIPI(current_radian - self.prev_radianL) * W_RADIUS
			self.prev_radianL = current_radian  # ???
		else:	
			distance = toPIPI(current_radian - self.prev_radianR) * W_RADIUS
			self.prev_radianR = current_radian  # ???
		return FWD_SIGN*distance

	def reset(self):
		"""
		Reset the encoder
		"""
		# ???? How does getting the angle reset the encoder?
		self.prev_radianL = self.getAngle(LEFT_MOTOR)
		self.prev_radianR = self.getAngle(RIGHT_MOTOR)
