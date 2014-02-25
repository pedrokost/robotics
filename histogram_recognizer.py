import operator

class HistogramRecognizer():
	"""
	Compares a histogram with a set of stored histogram, and returns the closest.
	histogram should respond to: hist (returns the histogram) -- numpy.array
	          					 values (returns raw values)  -- numpy.array
	"""
	def __init__(self, hist):
		self.hist = hist
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

	def distance(hist1, hist2):
		"""
		Returns the euclidean distance between the histograms
		"""
		dist = 0


	def shift(hist1, hist2):
		"""
		Returns the shift between two histograms
		"""
		# min_hist1_index = min(enumerate(hist1.values), key=operator.itemgetter(1))
		# min_hist2_index = min(enumerate(hist1.values), key=operator.itemgetter(1))

		# find the minimum index in hist1.values
		# find the minimum index in hist2.values
		# return the difference between the values?

		# This below is the stupid way, that should work
		

	def getHists(self):
		"""
		Returns a set of known histograms which are saved to files
		"""
		if not self.hists:
			# self.hists = readHists from file 
			pass

		return self.hists


