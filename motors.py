from constants import *
from BrickPi import *
from encoder import Encoder


class Motors:
	def __init__(self, leftMotor, rightMotor):
		self.leftMotorPort = leftMotor
		self.rightMotorPort = rightMotor
		BrickPi.MotorEnable[leftMotor]  = 1  # Enable the Motor A
		BrickPi.MotorEnable[rightMotor] = 1 # Enable the Motor B
		
		#set up encoder
		self.encoder = Encoder()

	def stop(self):
		"""
		Stop Motors
		"""
		self._setMotorSpeed(self.leftMotorPort, 0)
		self._setMotorSpeed(self.rightMotorPort, 0)

	def forward(self, distance, speed):
		"""
		Makes the robot move forward 'distance' cm
		"""
		print "Move forward ", distance, " cm."
		self.encoder.reset()
		current_dist = 0
		current_left = 0
		current_right = 0
		dummy_vel = 0
		dummy_weight = 20
		
		main_vel = FWD_VEL0
		
		#get direction sign	
		dir_sign = 1
		if(distance < 0):
			dir_sign = -1

		#loop for moving
		while(abs(current_dist) < abs(distance)):
			new_left_speed  = dir_sign*(main_vel) + dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
			new_right_speed = dir_sign*(main_vel) - dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
			self._setMotorSpeed(self.leftMotorPort, new_left_speed)
			self._setMotorSpeed(self.rightMotorPort, new_right_speed)
			time.sleep(.05)
			left_move = self.encoder.getMovingDistance(self.leftMotorPort)
			right_move = self.encoder.getMovingDistance(self.rightMotorPort)
			current_left  += left_move
			current_right += right_move
			current_dist = (current_left + current_right)/2
			dummy_vel = (abs(current_right) - abs(current_left))/2
			
			#change main speed
			main_vel += int(round((speed - main_vel) * EASING_C))
		self.stop()

	def turn(self, angle):
		"""
		Makes the robot turn in place by an angle
		"""
		self.encoder.reset()
		print "Turn ", angle, " radian."
		current_angle = 0
		current_left = 0
		current_right = 0
		dummy_vel = 0
		dummy_weight = 40

		#get direction sign	
		dir_sign = 1
		if(angle < 0):
			dir_sign = -1

		while(abs(current_angle) < abs(angle)):
			new_left_speed = -(dir_sign*ROT_VEL + dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight)))
			new_right_speed = dir_sign*ROT_VEL - dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
			self._setMotorSpeed(self.leftMotorPort, new_left_speed)
			self._setMotorSpeed(self.rightMotorPort, new_right_speed)
			time.sleep(.05)
			left_move = self.encoder.getMovingDistance(self.leftMotorPort)
			right_move = self.encoder.getMovingDistance(self.rightMotorPort)
			current_left  += left_move
			current_right += right_move
			current_angle = (current_right - current_left)/(2*RW_DIST) #can change this
			dummy_vel = (abs(current_right) - abs(current_left))/2
			print "L : ", current_left
			print "R : ", current_right
			print "Current angle : ", current_angle
		self.stop()

	def left90deg(self):
		"""
		Function to turn left 90 degrees
		"""
		self.turn(M_PI/2) #  - 0*M_PI/180
		
	def right90deg(self):
		"""
		Function to turn right 90 degrees
		"""
		self.turn(-M_PI/2)

	def setLeftSpeed(self, speed):
		BrickPi.MotorSpeed[self.leftMotorPort] = speed
		BrickPiUpdateValues()

	def setRightSpeed(self, speed):
		BrickPi.MotorSpeed[self.rightMotorPort] = speed
		BrickPiUpdateValues()

	def _setMotorSpeed(self, motor_port, speed):
		BrickPi.MotorSpeed[motor_port] = speed
		BrickPiUpdateValues()