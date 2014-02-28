from signature import Signature
from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer
from sonarScanner import *

BrickPiSetup()
scanner = SonarScanner(PORT_4, PORT_C)
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

nScans = 5
nBins = 10
container = SignatureContainer(nScans)
container.delete_loc_files()

# read + save signatures
for i in range(0, nScans):
	data = scanner.scan()
	s = Signature(data, nBins)
	container.save(s)