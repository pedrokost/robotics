import operator
import numpy as np
from signature import Signature
from utilities import *

class SignatureRecognizer:
	"""
	Compares a histogram with a set of stored histogram, and returns the closest.
	histogram should respond to:
		hist (returns the histogram) -- numpy.array
		values (returns raw values)  -- numpy.array
	"""

	def __init__(self, signature_container):
		self.container = signature_container # manages reading/writing signatures to/from files
		self._sigs = None

	def sigs(self):
		"""
		Returns a set of known signatures which are saved to files
		"""
		if self._sigs is None:  # cache
			self._sigs = self.container.readAll()
		return self._sigs

	def closest(self, signature):
		"""
		Given the signature, find the most similar signature
		Returns:
			index of most similar signature
			distance to most similar signature
			most similar signature
		"""
		dists = [self.distance(signature, s) for s in self.sigs()]
		min_index, min_value = min(enumerate(dists), key=operator.itemgetter(1))
		return min_index, min_value, self.sigs()[min_index]

	def distance(self, signature1, signature2):
		"""
		Returns the square of the distance between the signatures.
		"""
		return square_euclidean_distance(signature1.sig, signature2.sig)

	def shift(self, signature1, signature2):
		return self.__shift(signature1.values, signature2.values)

	def __shift(self, vector1, vector2):
		"""
		Returns the absolute shift between two enumerables.
		vector1 is the reference vector, vector2 is the one we want to compare against the reference 
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
			cycled_values = np.roll(vector2, i)
			d = square_euclidean_distance(cycled_values, vector1)
			if d < bestDist:
				bestDist = d
				shift = i

		return shift, bestDist
