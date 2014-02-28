from motorScanner import *
from BrickPi import *
from utilities import *
from math import *

BrickPiSetup()
scanner = MotorScanner(PORT_C)
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

scanner.gotoAngle(pi/2, 'cw')
	#print "Angle : ", radToDeg()
#scanner.gotoAngle(0)

#BrickPi.MotorSpeed[PORT_C] = int(0)
#BrickPi.MotorEnable[PORT_C] = 0
#BrickPiUpdateValues()
#print "A"
#scanner.motorRotateDegree([140], [180], [PORT_C], 0.0001)
#print "A2"
#print "End"
#while(True):
#BrickPi.MotorSpeed[self.motorPort] = int(0)