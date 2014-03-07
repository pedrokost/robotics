import numpy as np
from utilities import unitSum, medianFilter
from constants import NUMBER_OF_SIGNATURE_BINS

class Signature:
	"""
	Represents a signature of a set of measurements in place (360 deg)
	"""
	def __init__(self, vector, nBins = NUMBER_OF_SIGNATURE_BINS, name=""):
		"""
		The vector contains reliable scalar values (in case of distance measurments, only those where the distance is below 100cm, and angle to wall < 40 deg)
		"""
		cleanedVector = medianFilter(vector, 4)
		self.values = np.array(cleanedVector)
		self.sig = self.sig(vector, nBins)  # histogram
		self.name = name

	def sig(self, vector, nBins):
		h, _ = np.histogram(vector, nBins)
		# Normalize histogram to make it work with different number of measurments
		h = unitSum(h)
		return h

	def __str__(self):
		return self.name
