import numpy as np

class Signature:
	"""
	Represents a signature of a set of measurements in place (360 deg)
	"""
	def __init__(self, vector, nBins = 20):
		"""
		The vector contains reliable scalar values (in case of distance measurments, only those where the distance is below 100cm, and angle to wall < 40 deg)
		"""
		self.values = np.array(vector)
		self.hist = self.hist(vector, nBins)

	def hist(self, vector, nBins):
		h, _ = np.histogram(vector, nBins)
		return h
