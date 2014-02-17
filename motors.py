from constants import *
from BrickPi import *

MOTOR_VEL_KP = 6
MOTOR_VEL_KI = 0
MOTOR_VEL_KD = 0

class Motors:
	# The index indicates the element of the vector that belongs to each motor
	LEFT_MOTOR_INDEX  = 0
	RIGHT_MOTOR_INDEX = 1
	# set up parameter for velocity control with PID
	accError = [0, 0]
	prevError = [0, 0]
	power = [0, 0]

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

	def reset(self):
		"""
		Resets the power, but does immediately apply it to the motors
		"""
		self.power = [0, 0]
		self.accError = [0, 0]
		self.prevError = [0, 0]

	def _setVel(self, motor_port, prefer_vel, current_vel):
		"""
			Set Velocity in cm/s
		"""
		motor_index = self.LEFT_MOTOR_INDEX if motor_port == self.leftMotorPort else self.RIGHT_MOTOR_INDEX

		error = prefer_vel - current_vel
		d_error = error - self.prevError[motor_index]
		acc_error = self.accError[motor_index] + error

		# update static params
		self.accError[motor_index] = acc_error
		self.prevError[motor_index] = error

		# update power
		self.power[motor_index] += MOTOR_VEL_KP*error + MOTOR_VEL_KI*acc_error + MOTOR_VEL_KD*d_error
		self._setMotorPower(motor_port, self.power[motor_index])

	def _setMotorPower(self, motor_port, power):
		BrickPi.MotorSpeed[motor_port] = FWD_SIGN*int(round(power))
		BrickPiUpdateValues()


# Old Version of motors.py

#	def stop(self):
#		"""
#		Stop Motors
#		"""
#		self.setSpeed(0, 0)
#
#	def forward(self, distance, speed=FWD_VEL):
#		"""
#		Makes the robot move forward 'distance' cm
#		"""
#		print "Move forward ", distance, " cm."
#		self.encoder.reset()
#		current_dist = 0
#		current_left = 0
#		current_right = 0
#		dummy_vel = 0
#		dummy_weight = 20
#		
#		main_vel = FWD_VEL0
#		
#		#get direction sign	
#		dir_sign = 1
#		if(distance < 0):
#			dir_sign = -1
#
#		#loop for moving
#		while(abs(current_dist) < abs(distance)):
#			new_left_speed  = dir_sign*(main_vel) + dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
#			new_right_speed = dir_sign*(main_vel) - dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
#			self._setMotorSpeed(self.leftMotorPort, new_left_speed)
#			self._setMotorSpeed(self.rightMotorPort, new_right_speed)
#			time.sleep(.05)
#			left_move = self.encoder.getMovingDistance(self.leftMotorPort)
#			right_move = self.encoder.getMovingDistance(self.rightMotorPort)
#			current_left  += left_move
#			current_right += right_move
#			current_dist = (current_left + current_right)/2
#			dummy_vel = (abs(current_right) - abs(current_left))/2
#			
#			#change main speed
#			main_vel += int(round((speed - main_vel) * EASING_C))
#		self.stop()
#
#	def turn(self, angle):
#		"""
#		Makes the robot turn in place by an angle
#		"""
#		self.encoder.reset()
#		print "Turn ", angle, " radian."
#		current_angle = 0
#		current_left = 0
#		current_right = 0
#		dummy_vel = 0
#		dummy_weight = 40
#
#		#get direction sign	
#		dir_sign = 1
#		if(angle < 0):
#			dir_sign = -1
#
#		while(abs(current_angle) < abs(angle)):
#			new_left_speed = -(dir_sign*ROT_VEL + dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight)))
#			new_right_speed = dir_sign*ROT_VEL - dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
#			self._setMotorSpeed(self.leftMotorPort, new_left_speed)
#			self._setMotorSpeed(self.rightMotorPort, new_right_speed)
#			time.sleep(.05)
#			left_move = self.encoder.getMovingDistance(self.leftMotorPort)
#			right_move = self.encoder.getMovingDistance(self.rightMotorPort)
#			current_left  += left_move
#			current_right += right_move
#			current_angle = (current_right - current_left)/(2*RW_DIST) #can change this
#			dummy_vel = (abs(current_right) - abs(current_left))/2
#			print "L : ", current_left
#			print "R : ", current_right
#			print "Current angle : ", current_angle
#		self.stop()
#
#	def setLeftSpeed(self, speed):
#		self._setMotorSpeed(self.leftMotorPort, speed)
#
#	def setRightSpeed(self, speed):
#		self._setMotorSpeed(self.rightMotorPort, speed)
#
#	def left90deg(self):
#		"""
#		Function to turn left 90 degrees
#		"""
#		self.turn(M_PI/2) #  - 0*M_PI/180
#		
#	def right90deg(self):
#		"""
#		Function to turn right 90 degrees
#		"""
#		self.turn(-M_PI/2)
#
#	def setSpeed(self, speed_left, speed_right=None):
#		if speed_right is None: speed_right = speed_left
#		BrickPi.MotorSpeed[self.leftMotorPort] = int(round(speed_left))
#		BrickPi.MotorSpeed[self.rightMotorPort] = int(round(speed_right))
#		BrickPiUpdateValues()
#
#	def _setMotorSpeed(self, motor_port, speed):
#		BrickPi.MotorSpeed[motor_port] = int(round(speed))
#		BrickPiUpdateValues()

