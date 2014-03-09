from signature import Signature
from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer
from sonarScanner import *
from signature import Signature
from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer
from utilities import *
from Canvas import *
from math import pi, cos, sin
from Map import *

SCANNER_DRAW_X0 = 0
SCANNER_DRAW_Y0 = 0
SCANNER_DRAW_SCALE = 1.2

SCANNER_START_ANGLE = -pi
SCANNER_SCAN_STEP = pi/180 # 1 degree
SCANNER_END_ANGLE = pi


canvas = Canvas();
mymap = Map(canvas);
mymap.add_wall((0,0,0,168));        # a
mymap.add_wall((0,168,84,168));     # b
mymap.add_wall((84,126,84,210));    # c
mymap.add_wall((84,210,168,210));   # d
mymap.add_wall((168,210,168,84));   # e
mymap.add_wall((168,84,210,84));    # f
mymap.add_wall((210,84,210,0));     # g
mymap.add_wall((210,0,0,0));        # h
# mymap.draw();


def drawScanData(data, point):
	canvas = Canvas()
	for i in range(0, len(data)):
		if i%2 == 0:
			continue
		r = data[i]*SCANNER_DRAW_SCALE
		th = SCANNER_START_ANGLE + SCANNER_SCAN_STEP*i

		x0 = int(SCANNER_DRAW_X0) + point[0]
		y0 = int(SCANNER_DRAW_Y0) + point[1]
		x1 = int(x0 + r*cos(th))
		y1 = int(y0 + r*sin(th))

		# print radToDeg(th), r
		# print (x0, y0, x1, y1)

		canvas.drawLine((x0, y0, x1, y1))

BrickPiSetup()
scanner = SonarScanner(PORT_D, PORT_4)
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

nScans = 8
index = 4

# We need to do index 1, 3, 6
container = SignatureContainer(nScans)
# container.delete_loc_files()

# read + save signatures
# for i in range(0, nScans):

data = scanner.scan()

# data = [21, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 20, 21, 21, 23, 23, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 57, 57, 56, 55, 55, 55, 55, 55, 54, 54, 54, 54, 54, 54, 54, 54, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 54, 54, 54, 54, 54, 54, 55, 54, 55, 55, 55, 55, 56, 56, 56, 57, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 91, 91, 91, 91, 91, 92, 92, 92, 92, 92, 91, 92, 91, 92, 91, 91, 73, 72, 71, 71, 71, 71, 70, 70, 70, 70, 70, 70, 70, 70, 70, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 70, 70, 69, 69, 70, 69, 70, 70, 70, 70, 70, 70, 70, 71, 71, 71, 71, 71, 72, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 27, 25, 158, 157, 25, 26, 157, 29, 27, 157, 30, 26, 24, 27, 28, 157, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 139, 139, 138, 21]

s = Signature(data, 50)
container.save(s, index)


drawScanData(s.values, (100,100))