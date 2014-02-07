from constants import *
from BrickPi import *
from utilities import *
from motors import Motors
from sonar import Sonar
from touch import Touch

class Robot:
	# TODO: pass dict with sensor mappings
	def __init__(self, leftMotorPort, rightMotorPort, leftTouchPort, rightTouchPort, sonarPort):
		BrickPiSetup()  # setup the serial port for communication

		self.motors = Motors(leftMotorPort, rightMotorPort)
		
		if(sonarPort != None):
			self.sonar = Sonar(sonarPort)

		if(leftTouchPort != None):
			self.leftTouch = Touch(leftTouchPort)
		
		if(rightTouchPort != None):
			self.rightTouch = Touch(rightTouchPort)

		BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

	def follow_wall(self, prefer_wall_distance):
		"""
		Follow wall within 'distance' cm
		"""
		print "Follow wall within ", prefer_wall_distance, " cm."
		
		acc_err = 0
		#loop for moving
		while(True):
			acc_err = self._follow_wall_step(prefer_wall_distance, acc_err)
		
	def _follow_wall_step(self, prefer_wall_distance, acc_err=0):
		diff_weight = 20
		# read sonar
		z = self.sonar.getSmoothSonarDistance(0.05)

		print "Distance from the wall ", z
		
		err = (prefer_wall_distance - z)
		err = limitTo(err, -10, 10)
		print err
		acc_err += err
		diff_vel = FOLLOW_WALL_KERR*err + 2*acc_err

		# set moving speed
		new_left_speed  = FWD_VEL + FWD_SIGN*int(round(diff_vel*diff_weight))
		new_right_speed = FWD_VEL - FWD_SIGN*int(round(diff_vel*diff_weight))
		self.motors.setLeftSpeed(new_left_speed)
		self.motors.setRightSpeed(new_right_speed)

		return acc_err
		

	def keepDistance(self, distance):
		"""
		Keeps the robot at some distance from the wall
		"""
		print "Keep distance : ", distance

		acc_err = 0

		while True:
			# get sonar measurement for 0.05 seconds
			z = self.sonar.getSmoothSonarDistance(0.05)

			# set the speed of the robot
			err = z - distance
			acc_err += err
			print err, acc_err
			speed = PID_KP_CONSTANT * err + PID_KI_CONSTANT * acc_err

			# print "speed : ", speed
			self.motors.setLeftSpeed(speed)
			self.motors.setRightSpeed(speed)
