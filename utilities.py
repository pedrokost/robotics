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

def median(array):
	"""
	Returns the median of an array
	"""
	medIndex = int(len(array) / 2)
	return sorted(array)[medIndex];