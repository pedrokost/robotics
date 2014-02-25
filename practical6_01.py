from motorScanner import *
from BrickPi import *
from utilities import *

BrickPiSetup()
scanner = MotorScanner(PORT_C)
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

scanner.gotoAngle(0)

#BrickPi.MotorSpeed[PORT_C] = int(0)
#BrickPi.MotorEnable[PORT_C] = 0
#BrickPiUpdateValues()
#print "A"
#scanner.motorRotateDegree([40], [180], [PORT_C], 0.0001)
#print "A2"
#print "End"
#while(True):
#BrickPi.MotorSpeed[self.motorPort] = int(0)