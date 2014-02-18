import math

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

def mean_(tupl_list):
	pass


def limitTo(value, min_v, max_v):
	"""
	Bounds a value to certain limit by chopping it
	"""
	return min(max(value, min_v), max_v)

def diffDist(point0, point1):
	dx = point0[0] - point1[0]
	dy = point0[1] - point1[1]
	return math.sqrt(dx*dx + dy*dy)

def cumsum(list):
    total = 0
    for x in list:
        total += x
        yield total