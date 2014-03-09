import os

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
	return indexList.append(indexList[0])

def rotate(l, n):
	return l[n:] + l[:n]

def performRotation(indexList, first):
	while indexList[0] != first:
		indexList = rotate(indexList, 1)

# wayPointIndex is the first waypoint
def buildPath(wayPointIndex):
	basePathIndexes = [7, 1, 2, 4, 5, 4]
	rotatedPath = performRotation(basePathIndexes, wayPointIndex)
	circularPath = makeCircular(rotatedPath)
	return pathFromIndexes(circularPath)
