from constants import *
from BrickPi import *
from encoder import Encoder
from utilities import toPIPI, median

class Robot:
	# TODO: pass dict with sensor mappings
	def __init__(self, leftMotor, rightMotor, leftTouch, rightTouch, sonar):
		BrickPiSetup()  # setup the serial port for communication

		self.leftMotor = leftMotor
		self.rightMotor = rightMotor
		self.leftTouch = leftTouch
		self.rightTouch = rightTouch
		self.sonar = sonar

		BrickPi.MotorEnable[leftMotor]  = 1  # Enable the Motor A
		BrickPi.MotorEnable[rightMotor] = 1 # Enable the Motor B

		BrickPi.SensorType[leftTouch] = TYPE_SENSOR_TOUCH
		BrickPi.SensorType[rightTouch] = TYPE_SENSOR_TOUCH
		BrickPi.SensorType[sonar] = TYPE_SENSOR_ULTRASONIC_CONT

		BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

		self.encoder = Encoder()

	def stop(self):
		"""
		Makes the robot stop
		"""
		print "Stop"
		self._setMotorSpeed(self.leftMotor, 0)
		self._setMotorSpeed(self.rightMotor, 0)

	def forward(self, distance):
		"""
		Makes the robot move forward 'distance' cm
		"""
		print "Move forward ", distance, " cm."
		self.encoder.reset()  # What does it do?
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
			self._setMotorSpeed(self.leftMotor, new_left_speed)
			self._setMotorSpeed(self.rightMotor, new_right_speed)
			time.sleep(.05)
			left_move = self.encoder.getMovingDistance(self.leftMotor)
			right_move = self.encoder.getMovingDistance(self.rightMotor)
			current_left  += left_move
			current_right += right_move
			current_dist = (current_left + current_right)/2
			dummy_vel = (abs(current_right) - abs(current_left))/2
			print "L : ", current_left
			print "R : ", current_right
			print "Current distance", current_dist
			
			#change main speed
			main_vel += int(round((FWD_VEL - main_vel) * EASING_C))
		
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
			self._setMotorSpeed(self.leftMotor, new_left_speed)
			self._setMotorSpeed(self.rightMotor, new_right_speed)
			time.sleep(.05)
			left_move = self.encoder.getMovingDistance(self.leftMotor)
			right_move = self.encoder.getMovingDistance(self.rightMotor)
			current_left  += left_move
			current_right += right_move
			current_angle = (current_right - current_left)/(2*RW_DIST) #can change this
			dummy_vel = (abs(current_right) - abs(current_left))/2
			print "L : ", current_left
			print "R : ", current_right
			print "Current angle : ", current_angle
		self.stop()

	def keepDistance(self, distance):
		"""
		Keeps the robot at some distance from the wall
		"""
		print "Keep distance : ", distance
		self.encoder.reset()

		acc_err = 0

		while True:
			# get sonar measurement for 0.05 seconds
			z = self.getSmoothSonarDistance(0.05)

			# set the speed of the robot
			err = z - distance
			acc_err += err
			print err, acc_err
			speed = PID_KP_CONSTANT * err + PID_KI_CONSTANT * acc_err

			# print "speed : ", speed
			self._setMotorSpeed(self.leftMotor, speed)
			self._setMotorSpeed(self.rightMotor, speed)

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

	def isLeftTouch(self):
		BrickPiUpdateValues()
		return BrickPi.Sensor[self.leftTouch]

	def isRightTouch(self):
		BrickPiUpdateValues()
		return BrickPi.Sensor[self.rightTouch]

	def getSmoothSonarDistance(self, duration):
		"""
		Returns a cleaned value for the distance, by sampling continuosly for duration seconds
		"""
		values = []
		start = time.time()
		while time.time() - start < duration:
			values.append(self._getSonarDistance())
			time.sleep(0.001)
		return median(values)

	# This function is to get sonar distance. (in cm)
	def _getSonarDistance(self):
		BrickPiUpdateValues()
		return BrickPi.Sensor[self.sonar]

	def setFwdSpeed(self, speed):
		self._setMotorSpeed(self.leftMotor, speed)
		self._setMotorSpeed(self.rightMotor, speed)
		
	def _setMotorSpeed(self, motor_port, speed):
		BrickPi.MotorSpeed[motor_port] = speed

