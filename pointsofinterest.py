import os

POI_dict = {\
	1 : (84, 30),\
	2 : (180, 30),\
	4 : (126, 54),\
	5 : (126, 168),\
	7 : (30, 54),\
	}

def getById(wayPointIndedx):
	global POI_dict
	if wayPointIndedx not in POI_dict:
		print "Waypoint index does not exist."
		os._exit(0)
	return POI_dict[wayPointIndex]

def buildPath(wayPointIndex):
	return [(84, 30), (180,30), (180,54), (126, 54), (126, 168), (126, 126), (30, 54), (84, 54), (84, 30)]
