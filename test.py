from sonar import *
from encoder import *
from math import *
from motorScanner import *
from utilities import *
from Canvas import *
from BrickPi import *
import time
s = Sonar(PORT_4)

BrickPiSetup()
BrickPiSetupSensors()

for x in xrange(1,100000):
	z = s._getSonarDistance()
	print z
	time.sleep(0.5)
	