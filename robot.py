from constants import *
from BrickPi import *
from utilities import *
from motors import Motors
from sonar import Sonar
from touch import Touch

class Robot:

	def __init__(self, leftMotorPort=None, rightMotorPort=None, leftTouchPort=None, rightTouchPort=None, sonarPort=None):
		BrickPiSetup()  # setup the serial port for communication

		if(sonarPort is not None): self.sonar = Sonar(sonarPort)
		if(leftTouchPort is not None): self.leftTouch = Touch(leftTouchPort)
		if(rightTouchPort is not None): self.rightTouch = Touch(rightTouchPort)
		if(leftMotorPort is not None and rightMotorPort is not None): 
			self.motors = Motors(leftMotorPort, rightMotorPort)

		BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

	def followWall(self, prefer_wall_distance):
		"""
		Follow wall within 'distance' cm
		"""
		print "Follow wall within ", prefer_wall_distance, " cm."

		acc_err = 0
		last_err = 0
		last_dist = 0
		while(True):
			acc_err, last_err, last_diff_vel = self.followWallStep(prefer_wall_distance, acc_err, last_err, last_dist)
		
	def followWallStep(self, prefer_wall_distance, acc_err=0, last_err=0, last_z = 0):
		# read sonar
		z = self.sonar.getSmoothSonarDistance(0.05)

		print "Distance from the wall ", z
				
		err = (prefer_wall_distance - z)
		err = limitTo(err, -10, 10)
		derror = err - last_err
		acc_err += err
		#acc_err = limitTo(acc_err, -10, 10)  # HACK: shouldn't need to do this

		if(err < 0):
			kp = FOLLOW_WALL_KP_FAR
		else:
			kp = FOLLOW_WALL_KP_NEAR
		
		I_adjust = limitTo(FOLLOW_WALL_KI*acc_err, -5, 5)

		diff_vel = kp*err + I_adjust + FOLLOW_WALL_KD * derror
		
		print "err : ", err, acc_err

		if(err*last_err <= 0):
			acc_err = 0
		print kp*err, I_adjust, FOLLOW_WALL_KD * derror
		
		print "RERR : ", abs(err) - abs(last_err)

		ERR_T = 3
		#if(abs(last_err) - abs(err) > ERR_T):
		#	diff_vel = 0

		# set moving speed
		new_left_speed  = FWD_VEL + FWD_SIGN*int(round(diff_vel))
		new_right_speed = FWD_VEL - FWD_SIGN*int(round(diff_vel))
		self.motors.setSpeed(new_left_speed, new_right_speed)
		time.sleep(0.01)

		last_z = z
		return (acc_err, err, last_z)

	def keepDistanceFront(self, distance):
		"""
		Keeps the robot at some distance from the wall
		"""
		print "Keep distance : ", distance

		acc_err = 0
		last_err = 0

		while True:
			# get sonar measurement for 0.05 seconds
			z = self.sonar.getSmoothSonarDistance(0.05)

			# set the speed of the robot
			err = z - distance
			acc_err += err
			derror = err - last_err
			print "Current distance : ", z
			speed = KEEP_DISTANCE_FRONT_KP * err + KEEP_DISTANCE_FRONT_KI * acc_err + KEEP_DISTANCE_FRONT_KD * derror
			print speed, err, acc_err, derror
			#if(abs(err) > 3 and speed != 0 and abs(speed) < LOWEST_VEL):
			#	direction = speed/abs(speed)
			#	speed = direction*LOWEST_VEL
			if(err*last_err < 0):
				acc_err = 0
			print "mul", err*last_err
			self.motors.setSpeed(speed)
			last_err = err
			time.sleep(0.01)

	# def stop(self):
	# 	self.motors.stop()

	# def forward(self, *args, **kwargs):
	# 	self.motors.forward(*args, **kwargs)

	# def turn(self, *args, **kwargs):
	# 	self.motors.turn(*args, **kwargs)

	# def left90deg(self):
	# 	self.motors.left90deg()
		
	# def right90deg(self):
	# 	self.motors.right90deg()

	# def setSpeed(self, *args, **kwargs):
	# 	self.motors.setSpeed(*args, **kwargs)

	def __getattr__(self, name):
		"""
		If a method like stop does not exist, try it on the motors
		"""
		def _missing(*args, **kwargs):
			if self.motors is not None:
				func = getattr(self.motors, name)
				func(*args, **kwargs)

		return _missing
