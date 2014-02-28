from sonar import *
from encoder import *
from math import *
from motorScanner import *
from utilities import *
from Canvas import *

SCANNER_START_ANGLE = -pi
SCANNER_SCAN_STEP = pi/180 # 1 degree
SCANNER_END_ANGLE = pi


SCANNER_DRAW_X0 = 100
SCANNER_DRAW_Y0 = 100
SCANNER_DRAW_SCALE = 2

class SonarScanner:
	def __init__(self, sonarPort, motorPort):
		self.motor = MotorScanner(motorPort)
		self.sonar = Sonar(sonarPort)
		self.canvas = Canvas()

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

	def drawScanData(self, data):
		for i in range(0, len(data)):
			r = data[i]*SCANNER_DRAW_SCALE
			th = SCANNER_START_ANGLE + SCANNER_SCAN_STEP*i

			if(r > 200):
				continue

			x0 = int(SCANNER_DRAW_X0)
			y0 = int(SCANNER_DRAW_Y0)
			x1 = int(x0 + r*cos(th))
			y1 = int(y0 + r*sin(th))

			print radToDeg(th), r
			print (x0, y0, x1, y1)

			self.canvas.drawLine((x0, y0, x1, y1))