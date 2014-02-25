from BrickPi import *
from Encoder import *
from math import *
from utilities import *

SCANNER_ACCEPTABLE_ANGLE = pi/360 # 0.5 degree

class MotorScanner:
	def __init__(self, motorPort):
		self.motorPort = motorPort
		self.encoder = Encoder()
		BrickPi.MotorEnable[motorPort]  = 1

	def gotoAngle(self, prefer_angle):
	"""
		Function to rotate motor to the specific angle(Radian)
	"""
		# get the starting angle
		current_angle = self.encoder.getAngle(motorPort)

		# if it is still in the specified angle -> do nothing
		if(abs(toPIPI(prefer_angle - current_angle)) < SCANNER_ACCEPTABLE_ANGLE):
			return

		# calculate moving direction
		#
		moving_dir = sign(diff_angle) # if 
		

		# 

		while(True):




