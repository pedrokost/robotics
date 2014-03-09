from constants import *
from BrickPi import *
from utilities import *

MOTOR_VEL_KP = 0.1
MOTOR_VEL_KI = 0.0
MOTOR_VEL_KD = 0.0  

VEL_TO_POWER_W1 = 12.6407
VEL_TO_POWER_W0 = 0 #-1.8951

LEFT_BIAS = 11

class Motors:
	# The index indicates the element of the vector that belongs to each motor
	LEFT_MOTOR_INDEX  = 0
	RIGHT_MOTOR_INDEX = 1
	# set up parameter for velocity control with PID
	accError = [0, 0]
	prevError = [0, 0]
	dpower = [0, 0]

	#
	# Function to initialize motor statuts
	def __init__(self, leftMotor, rightMotor):
		self.leftMotorPort = leftMotor
		self.rightMotorPort = rightMotor
		BrickPi.MotorEnable[leftMotor]  = 1 # Enable the Motor A
		BrickPi.MotorEnable[rightMotor] = 1 # Enable the Motor B
		self.reset()

	def setVel(self, prefer_left_vel, prefer_right_vel, current_left_vel, current_right_vel):
		self.setLeftVel(prefer_left_vel, current_left_vel)
		self.setRightVel(prefer_right_vel, current_right_vel)

	def setLeftVel(self, prefer_vel, current_vel):
		self._setVel(self.leftMotorPort, prefer_vel, current_vel)

	def setRightVel(self, prefer_vel, current_vel):
		self._setVel(self.rightMotorPort, prefer_vel, current_vel)

	#
	#	Function to reset motor status
	def reset(self):
		self.dpower = [0, 0]
		self.accError = [0, 0]
		self.prevError = [0, 0]

	#
	#	Function to set motor velocity using PID controller
	def _setVel(self, motor_port, prefer_vel, current_vel):
		# get motor index from motor port
		motor_index = self.LEFT_MOTOR_INDEX if motor_port == self.leftMotorPort else self.RIGHT_MOTOR_INDEX		

		# get PID value
		error = abs(prefer_vel) - abs(current_vel)
		d_error = error - self.prevError[motor_index]
		acc_error = self.accError[motor_index] + error

		#if(motor_index == 0):
		#	print "error : ", error

		# update static params
		self.accError[motor_index] = acc_error
		self.prevError[motor_index] = error

		# update power (Not use pid)
		self.dpower[motor_index] += self._velToPower(MOTOR_VEL_KP*error + MOTOR_VEL_KI*acc_error + MOTOR_VEL_KD*d_error)

		# calculate power
		power_est = self._velToPower(prefer_vel)
		power_sign = sign(power_est)
		power = (self.dpower[motor_index] + abs(self._velToPower(prefer_vel)))*power_sign
		#power = self._velToPower(prefer_vel)
		if(motor_port == self.leftMotorPort):
			power = (LEFT_BIAS + self.dpower[motor_index] + abs(self._velToPower(prefer_vel)))*power_sign
 
		# set power
		self._setMotorPower(motor_port, power)


	#
	#	Function to change prefer velocity to power learning by linear regression
	def _velToPower(self, vel):
		return VEL_TO_POWER_W1*vel + VEL_TO_POWER_W0
	#
	#	Function to set motor power
	def _setMotorPower(self, motor_port, power):
		BrickPi.MotorSpeed[motor_port] = FWD_SIGN*int(round(power))
		BrickPiUpdateValues()

	#
	#	Function to set motor power
	def _setMotorPowerAll(self, powerLeft, powerRight):
		BrickPi.MotorSpeed[self.leftMotorPort] = FWD_SIGN*int(round(powerLeft))
		BrickPi.MotorSpeed[self.rightMotorPort] = FWD_SIGN*int(round(powerRight))
		BrickPiUpdateValues()


