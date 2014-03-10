import os
from utilities import rotate

POI_dict = {\
	1 : (84, 30),\
	2 : (180, 30),\
	4 : (126, 54),\
	5 : (126, 168),\
	7 : (30, 54),\
	}

def getById(wayPointIndex):
	global POI_dict
	if wayPointIndex not in POI_dict:
		print "Waypoint index does not exist."
		os._exit(0)
	return POI_dict[wayPointIndex]

def pathFromIndexes(indexList):
	return map(lambda index : POI_dict[index], indexList)

def makeCircular(indexList):
	return indexList + [indexList[0]]

def performRotation(indexList, first):
	while indexList[0] != first:
		indexList = rotate(indexList, 1)
	return indexList

# wayPointIndex is the first waypoint
def buildPath(wayPointIndex):
	basePathIndexes = [7, 1, 2, 4, 5, 4]
	print "Base: {0}".format(str(basePathIndexes))
	rotatedPath = performRotation(basePathIndexes, wayPointIndex)
	print "Rotated: {0}".format(str(rotatedPath))
	circularPath = makeCircular(rotatedPath)
	print "Circular: {0}".format(str(circularPath))
	finalPath = pathFromIndexes(circularPath)
	print "Final: {0}".format(str(finalPath))
	return finalPath
