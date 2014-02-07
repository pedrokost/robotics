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

	def follow_wall(self, prefer_wall_distance):
		"""
		Follow wall within 'distance' cm
		"""
		print "Follow wall within ", prefer_wall_distance, " cm."
		
		acc_err = 0
		last_err = 0
		#loop for moving
		while(True):
			acc_err, last_err = self._follow_wall_step(prefer_wall_distance, acc_err, last_err)
		
	def _follow_wall_step(self, prefer_wall_distance, acc_err=0, last_err=0):
		diff_weight = 20
		# read sonar
		z = self.sonar.getSmoothSonarDistance(0.05)

		print "Distance from the wall ", z
		
		err = (prefer_wall_distance - z)
		err = limitTo(err, -10, 10)
		derror = err - last_err
		acc_err += err
		acc_err = limitTo(acc_err, -10, 10)  # HACK: shouldn't need to do this
		diff_vel = FOLLOW_WALL_KP*err + FOLLOW_WALL_KI*acc_err + FOLLOW_WALL_KD * derror

		# set moving speed
		new_left_speed  = FWD_VEL + FWD_SIGN*int(round(diff_vel*diff_weight))
		new_right_speed = FWD_VEL - FWD_SIGN*int(round(diff_vel*diff_weight))
		self.motors.setLeftSpeed(new_left_speed)
		self.motors.setRightSpeed(new_right_speed)
		time.sleep(0.01)

		return (acc_err, err) 
		

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
			print err, acc_err
			speed = KEEP_DISTANCE_FRONT_KP * err + KEEP_DISTANCE_FRONT_KI * acc_err + KEEP_DISTANCE_FRONT_KD * derror

			# print "speed : ", speed
			self.motors.setSpeed(speed)
			last_err = err
			time.sleep(0.01)


