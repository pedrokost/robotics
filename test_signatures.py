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
	'accurateScan': False,
	'accurateRecognition': True,
})

# while True:

print placeRecognizer.whereAmI()
	
	# break
	# time.sleep(20)

