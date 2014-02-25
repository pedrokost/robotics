import numpy

class Histogram:
	"""
	Represents a histogram of datapoint
	"""
	def __init__(self, vector, nBins = 20):
		"""
		The vector contains reliable scalar values (in case of distance measurments, only those where the distance is below 100cm, and angle to wall < 40 deg)
		"""
		self.vector = numpy.array(vector)
		# self.hist = self.hist(vector, nBins)

	def hist(self, vector, nBins):
		return numpy.histogram(vector, nBins)