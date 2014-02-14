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

