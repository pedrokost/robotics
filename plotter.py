from Canvas import *
from math import pi, cos, sin
from constants import *
from utilities import degToRad
from Map import *

SCANNER_DRAW_X0 = 0
SCANNER_DRAW_Y0 = 0
SCANNER_DRAW_SCALE = 1.2

SCANNER_START_ANGLE = -pi
SCANNER_SCAN_STEP = pi/180 # 1 degree
SCANNER_END_ANGLE = pi

def drawScanData(data, point):
	canvas = Canvas()
	for i in range(0, len(data)):
		if i%2 == 0:
			continue
		r = data[i]*SCANNER_DRAW_SCALE
		SCANNER_SCAN_STEP = 2*pi / len(data)
		th = SCANNER_START_ANGLE + SCANNER_SCAN_STEP*i

		x0 = int(SCANNER_DRAW_X0) + point[0]
		y0 = int(SCANNER_DRAW_Y0) + point[1]
		x1 = int(x0 + r*cos(th))
		y1 = int(y0 + r*sin(th))

		# print radToDeg(th), r
		# print (x0, y0, x1, y1)

		canvas.drawLine((x0, y0, x1, y1))

def drawMap():
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
	mymap.draw();
