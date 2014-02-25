import operator
import numpy as np

class HistogramRecognizer():
	"""
	Compares a histogram with a set of stored histogram, and returns the closest.
	histogram should respond to: hist (returns the histogram) -- numpy.array
	          					 values (returns raw values)  -- numpy.array
	"""

	def __init__(self):
		self.hists = self.getHists()

	def closestTo(self, hist):
		"""
		Given the hist, find the most similar histogram
		Returns:
			index of most similar hist
			distance to most similar hist
			most similar hist
		"""
		dists = [self.distance(hist.hist, h.hist) for h in self.hists]
		min_index, min_value = min(enumerate(dists), key=operator.itemgetter(1))
		return min_index, min_value, self.hists[min_index]

	def distance(self, hist1, hist2):
		"""
		Returns the square of the euclidean distance between the histograms.
		hist1 and hist2 are np.ndarray objects (enumerable lists)
		"""
		return np.sum(np.square(hist1 - hist2))


	def shift(self, vector1, vector2):
		"""
		Returns the shift between two vectors.
		vector1 is the reference vectorogram, vector2 is the one we want to compare against the reference 
		vector1 and vector2 are np.ndarray objects (enumerable lists)
		"""
		# min_vector1_index = min(enumerate(vector1.values), key=operator.itemgetter(1))
		# min_vector2_index = min(enumerate(vector1.values), key=operator.itemgetter(1))

		# find the minimum index in vector1.values
		# find the minimum index in vector2.values
		# return the difference between the values?

		# This below is the stupid way, that should work
		shift = -1
		bestDist = float("inf")
		for i in xrange(0, len(vector1)):
			h = np.roll(vector2, i)
			d = self.distance(h, vector1)
			if d < bestDist:
				bestDist = d
				shift = i

		return shift, bestDist
		

	def getHists(self):
		"""
		Returns a set of known histograms which are saved to files
		"""
		return []
		# if not self.hists:
		# 	# self.hists = readHists from file 
		# 	self.hists = []
		# 	pass

		# return self.hists

