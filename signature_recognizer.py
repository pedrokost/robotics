import operator
import numpy as np
from signature import Signature
from utilities import *
from math import pi

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

	def theta(self, signature1, signature2, **kwargs):
		"""
		Compute the orientation difference between 2 signatures (assumes signatures are same, but cycled) in radians
		"""
		shift = self.shift(signature1, signature2, **kwargs)
		radiansPerShift = self.__radiansPerShift(shift, len(signature1.values))
		return shift * radiansPerShift


	def shift(self, signature1, signature2, **kwargs):
		"""
		Returns the absolute shift between two signatures
		"""
		return self.__shift(signature1.values, signature2.values, **kwargs)
	
	def __radiansPerShift(self, shift, max_shifts):
		"""
		Returns the number of radians that correspond to a cyclic shift of 1
		"""
		radiansPerShift = 2.0*pi / max_shifts
		return radiansPerShift

	def __shift(self, vector1, vector2, exhaustive = False, **kwargs):
		"""
		Returns the absolute shift between two enumerables.
		vector1 is the reference vector, vector2 is the one we want to compare against the reference 

		If exhaustive flag is set, performs an exhaustive search by attempting all possible shifts, else it tries to normalize the curves by finding the minimum
		"""
		if exhaustive:
			return self.__shift_exhaustive(vector1, vector2, **kwargs)
		else:
			return self.__shift_fast(vector1, vector2, **kwargs)
	
	def __shift_exhaustive(self, vector1, vector2, debug=False):
		"""
		Returns how much a vector was shifted

		The method is exhaustive: optimal but slow
		"""
		shift = -1
		bestDist = float("inf")
		for i in xrange(0, len(vector1)):
			cycled_values = np.roll(vector2, i)
			d = square_euclidean_distance(cycled_values, vector1)
			if d < bestDist:
				bestDist = d
				shift = i
		
		if debug:
			print "Best distance", bestDist

		return shift

	def __shift_fast(self, vector1, vector2, debug=False):
		"""
		Returns how much a vector was shifted

		The method is suboptimal (can give wrong shift) but fast
		"""
		# Finds the minimum value, and rotates the signatures to it
		min_v1_index, _ = min(enumerate(vector1), key=operator.itemgetter(1))
		min_v2_index, _ = min(enumerate(vector2), key=operator.itemgetter(1))
		shift = min_v1_index - min_v2_index

		if debug:
			v2 = np.roll(vector2, shift)
			bestDist = square_euclidean_distance(vector1, v2)
			print "Best distance", bestDist

		return shift
