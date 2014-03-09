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

container = SignatureContainer(8)
p1 = container.read(1).values
p2 = container.read(2).values
p4 = container.read(4).values
p5 = container.read(5).values
p7 = container.read(7).values
vals = [p1, p2, p4, p5, p7]


wayPoints = [(84, 30), (180,30), (126, 54), (126, 168), (30, 54)]

for i in range(len(wayPoints)):
	drawScanData(vals[i], wayPoints[i])

# drawScanData(p5, (100, 50))
# new = medianFilter(list(p5))
# drawScanData(new, (180, 100))

# print p5 - new


# REdo index 1?
# manually fix index 2

# REdo 2 (index 1)
# REdo 4 (index 3)
# REdo 7 (index 6)

# print recognizer.theta(closest, s4, exhaustive=exhaustive, debug=False)

