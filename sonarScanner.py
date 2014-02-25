from encoder import *
from math import *
from motorScanner import *

START_ANGLE = 0
SCAN_STEP = pi/180 # 1 degree
END_ANGLE = 2*pi

class SonarScanner:
	def __init__(self, motorPort, sonarPort):
		self.motorScanner = MotorScanner(motorPort)
		self.sonarPort = sonarPort

	# 
	# Function to scan from 0 to 360. Each step takes SCAN_STEP Radian
	def scan():
		current_angle = START_ANGLE

		while(True):
			# read sonar
			# rotate to degree





		return 