import math
import numpy as np
from constants import *

def toPIPI(angle):
	"""
	Function to limit the value of angle (radian) into [-PI, PI)
	"""
	while(angle < -math.pi):
		angle += 2*math.pi
	while(angle >= math.pi):
		angle -= 2*math.pi
	return angle

def median(list):
	"""
	Returns the median of an list
	"""
	medIndex = int(len(list) / 2)
	return sorted(list)[medIndex]

def mean(list):
	"""
	Returns the mean of an list
	"""
	sum(list) / float(len(list))


def limitTo(value, min_v, max_v):
	"""
	Bounds a value to certain limit by chopping it
	"""
	return min(max(value, min_v), max_v)

def diffDist(point0, point1):
	dx = point0[0] - point1[0]
	dy = point0[1] - point1[1]
	return math.sqrt(dx*dx + dy*dy)

def squareEuclideanDistance(vector1, vector2):
	"""
	Returns the square euclidean distance between 2 numpy vectors
	"""
	return np.sum(np.square(np.subtract(vector1, vector2)))

def cumsum(list):
    total = 0
    for x in list:
        total += x
        yield total

def sign(x):
	if(x > 0):
		return 1
	elif(x < 0):
		return -1
	return 0

def limitTo(x, min_val, max_val):
	if(x < min_val):
		x = min_val
	if(x > max_val):
		x = max_val
	return x

def degToRad(deg):
	return deg * math.pi / 180

def radToDeg(rad):
	return rad / math.pi * 180

def getAngularDifferent(a1, a0):
	a0 = toPIPI(a0)
	a1 = toPIPI(a1)

	return toPIPI(a1 - a0)

def unitSum(vector):
	"""
	Normalizes the vector so sum up to 1
	"""
	vec = map(float, vector)
	s = sum(vec)
	vec = [v / s for v in vec]
	return vec

def predictState(state, distL, distR):
	motionD  = (distR + distL)/2            # average moved direction of both wheels
	motionTH = (distR - distL)/(2*RW_DIST)  # rotation (voluntary or not) 

	newX = state[0] + (motionD)*cos(state[2])
	newY = state[1] + (motionD)*sin(state[2])
	newTH = toPIPI(state[2] + motionTH)
	return (newX, newY, newTH)

def medianFilter(array, halfsize=4):
	"""
	Performs a median filtering on the array
	"""
	newArray = array[0:halfsize]
	eachside = halfsize
	right = len(array) - halfsize - 1
	for x in xrange(halfsize, right):
		window = array[x-eachside:x+eachside+1]
		newArray.append(median(window))

	newArray += (array[right:])

	return newArray