from sonar import *
from encoder import *
from math import *
from motorScanner import *
from utilities import *

SCANNER_START_ANGLE = -pi
SCANNER_SCAN_STEP = pi/180 # 1 degree
SCANNER_END_ANGLE = pi

class SonarScanner:
	def __init__(self, sonarPort, motorPort):
		self.motor = MotorScanner(motorPort)
		self.sonar = Sonar(sonarPort)

	# 
	# Function to scan from 0 to 360. Each step takes SCAN_STEP Radian
	def scan(self):
		# initialize data
		data = []

		# Go to start angle
		self.motor.gotoAngle(SCANNER_START_ANGLE, 'cw')

		nStep = int((SCANNER_END_ANGLE - SCANNER_START_ANGLE)/SCANNER_SCAN_STEP)
		for i in range(0, nStep):
			# go to angle
			angle = SCANNER_START_ANGLE + SCANNER_SCAN_STEP*i
			self.motor.gotoAngle(angle, 'ccw')

			# read sonar data
			z = self.sonar.getSmoothSonarDistance(0.05)
			data.append(z)

		# Back to zero angle
		self.motor.gotoAngle(0, 'cw')

		return data