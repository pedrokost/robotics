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
		self.sig = self.sig(vector, nBins)  # histogram

	def sig(self, vector, nBins):
		h, _ = np.histogram(vector, nBins)
		# Normalize histogram to make it work with different number of measurments
		h = map(float, h) / sum(h)
		return h

	def __str__(self):
		return str(self.sig)
