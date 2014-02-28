from BrickPi import *
from math import *
from utilities import *

SCANNER_ACCEPTABLE_ANGLE = pi/180*5 # 1 degree
SCANNER_POWER = 200
SCANNER_ENCODER_RATIO = 8.0/40.0
SCANNER_FWD_SIGN = -1


class MotorScanner:
    #
    # Function to reset the motor
	def reset(self):
		self._prev_encoder_angle = self._getEncoderAngle()
		self._sonar_angle = 0

	#
	# Constructor
	def __init__(self, motorPort):
		self.motorPort = motorPort
		BrickPi.MotorEnable[motorPort]  = 1
		self.reset()

    #
    #	Function to rotate motor to a specific angle in specific direction (cw or ccw)
	def gotoAngle(self, prefer_angle, dir):
    	# check direction
		if(not (dir == 'cw') and not (dir == 'ccw')):
			print "dir must be either 'cw' or 'ccw'"

		# calculate moving direction
		if(dir == 'cw'):
			moving_dir = -1;
		else:
			moving_dir = 1;

		while(True):
	        # get the starting angle
			current_angle = self.getSonarAngle()

			# get angular distance to target
			diff_angle = getAngularDifferent(prefer_angle, current_angle)
			
			# check if it is at the goal state
			if((abs(diff_angle) < SCANNER_ACCEPTABLE_ANGLE) and (moving_dir*diff_angle < 0)):
				self._setMotorPower(-10*moving_dir) # break
				time.sleep(0.04)
				self._setMotorPower(0)
				break

			# # drive motor
			self._setMotorPower(SCANNER_POWER*moving_dir)

    #
    #    Function to set motor power
	def _setMotorPower(self, power):
		BrickPi.MotorSpeed[self.motorPort] = SCANNER_FWD_SIGN*int(round(power))
		BrickPiUpdateValues()
	
	#
	# Function to get current sonar angle
	def getSonarAngle(self):
		# get how far encoder is rotate
		current_encoder_angle = self._getEncoderAngle()
		diff = -getAngularDifferent(current_encoder_angle, self._prev_encoder_angle)
		self._prev_encoder_angle = current_encoder_angle

		# set to sonar angle
		self._sonar_angle = toPIPI(diff*SCANNER_ENCODER_RATIO + self._sonar_angle)

		return self._sonar_angle
	#
	# Function to get current encoder angle
	def _getEncoderAngle(self):
		BrickPiUpdateValues()
		degree = ( BrickPi.Encoder[self.motorPort] % 720 ) * 0.5
		radian = degree * math.pi / 180
		return radian