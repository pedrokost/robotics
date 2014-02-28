from sonarScanner import *
from BrickPi import *
from utilities import *
from math import *



BrickPiSetup()
scanner = SonarScanner(PORT_4, PORT_C)
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

data = scanner.scan()
#data = [21, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 20, 21, 21, 23, 23, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 57, 57, 56, 55, 55, 55, 55, 55, 54, 54, 54, 54, 54, 54, 54, 54, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 54, 54, 54, 54, 54, 54, 55, 54, 55, 55, 55, 55, 56, 56, 56, 57, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 91, 91, 91, 91, 91, 92, 92, 92, 92, 92, 91, 92, 91, 92, 91, 91, 73, 72, 71, 71, 71, 71, 70, 70, 70, 70, 70, 70, 70, 70, 70, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 70, 70, 69, 69, 70, 69, 70, 70, 70, 70, 70, 70, 70, 71, 71, 71, 71, 71, 72, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 27, 25, 158, 157, 25, 26, 157, 29, 27, 157, 30, 26, 24, 27, 28, 157, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 139, 139, 138, 21]
scanner.drawScanData(data)