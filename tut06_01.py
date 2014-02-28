from sonarScanner import *
from BrickPi import *
from utilities import *
from math import *



BrickPiSetup()
scanner = SonarScanner(PORT_4, PORT_C)
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

scanner.scan()