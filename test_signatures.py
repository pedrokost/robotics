from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer
from place_recognizer import PlaceRecognizer
from sonarScanner import SonarScanner
from BrickPi import BrickPiSetup, PORT_4, PORT_D, BrickPiSetupSensors
# from utilities import *

BrickPiSetup()
container = SignatureContainer()
recognizer = SignatureRecognizer(container)
sonarScanner = SonarScanner(PORT_4, PORT_D)
BrickPiSetupSensors()

placeRecognizer = PlaceRecognizer({
	'sonarScanner': sonarScanner,
	'signatureRecognizer': recognizer,
	'accurateScan': True,
	'accurateRecognition': True,
})

# while True:

print placeRecognizer.whereAmI()

#print container.read(1).sig
#print container.read(2).sig
#print container.read(4).sig
#print container.read(5).sig
#print container.read(7).sig

#indices = [1, 2, 4, 5, 7]

#for a in indices:
#	s1 = container.read(a)
#	for b in indices:
#		s2 = container.read(b)
#		print "a:", a, "b:", b, "distance:", recognizer.distance(s1, s2)

#s1 = container.read(2)
#s2 = container.read(5)
#print recognizer.closest(s1)

	# break
	# time.sleep(20)

