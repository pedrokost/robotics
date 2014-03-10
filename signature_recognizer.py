import operator
import numpy as np
from signature import Signature
from utilities import *
from math import pi
import os


MINIMUM_THRESHOLD = 0.1  # vectors are normalized to 1, so this is used to find the indices of the minimums with a *about* 10% soft boundary (to account for noise)


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
		dists_print = [(s.name, self.distance(signature, s)) for s in self.sigs()]
		print dists_print
		if self.tie(dists):
			return self.solveTie(signature, dists)
		else:
			min_index, min_value = min(enumerate(dists), key=operator.itemgetter(1))
			return min_index, min_value, self.sigs()[min_index]

	def tie(self, dists):
		dists = sorted(dists)
		# TODO(asfrent) make this a constant
		return dists[1] - dists[0] < 750

	def solveTie(self, signature, dists):
		METRIC_FUN = variance
		sortedIndices = [i[0] for i in sorted(enumerate(dists), key=lambda x:x[1])]
		first, second = sortedIndices[0], sortedIndices[1]
		metricFirst = METRIC_FUN(self.sigs()[first].values)
		metricSecond = METRIC_FUN(self.sigs()[second].values)
		metricReal = METRIC_FUN(signature.values)
		print "Metrics: real = {0}, first[{1}] = {2}, second[{3}] = {4}".format(metricReal, first, metricFirst, second, metricSecond)
		distToFirst = abs(metricReal - metricFirst)
		distToSecond = abs(metricReal - metricSecond)
		if distToFirst < distToSecond:
			return first, dists[first], self.sigs()[first]
		else:
			return second, dists[second], self.sigs()[second]

	def distance(self, signature1, signature2):
		"""
		Returns the square of the distance between the signatures.
		"""
		vals1 = list(signature1.values)
		vals2 = list(signature2.values)
		if len(vals1) != len(vals2):
			vals2 = interpolate(vals2, len(vals1))
		rotations = self.genAllRotations(vals2)
		distances = map(lambda r : squareEuclideanDistance(r, vals1), rotations)
		return float(min(distances)) / float(len(vals1))

	def genAllRotations(self, values):
		rotations = []
		currentRot = values
		for i in range(0, len(values)):
			rotations.append(currentRot)
			currentRot = rotate(currentRot, 1)
		return rotations

	def theta(self, signature1, signature2, **kwargs):
		"""
		Compute the orientation difference between 2 signatures (assumes signatures are same, but cycled) in radians
		"""
		shift = self.shift(signature1, signature2, **kwargs)
		radiansPerShift = self.__radiansPerShift(shift, len(signature1.values))
		return toPIPI(shift * radiansPerShift)


	def shift(self, signature1, signature2, **kwargs):
		"""
		Returns the absolute shift between two signatures
		"""
		s1_values = unitSum(signature1.values)
		s2_values = unitSum(signature2.values)

		return self.__shift(s1_values, s2_values, **kwargs)

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
		if len(vector1) is not len(vector2):
			vector2 = interpolate(vector2, len(vector1))

		if exhaustive:
			return self.__shift_exhaustive(vector1, vector2, **kwargs)
		else:
			return self.__shift_fast(vector1, vector2, **kwargs)

	def __shift_exhaustive(self, vector1, vector2, debug = False):
		"""
		Returns how much a vector was shifted

		The method is exhaustive: optimal but slow
		"""
		shift = -1
		bestDist = float("inf")
		for i in xrange(0, len(vector1)):
			cycled_values = np.roll(vector2, i)
			d = squareEuclideanDistance(cycled_values, vector1)
			if d < bestDist:
				bestDist = d
				shift = i

		if debug:
			print "Best distance", bestDist
			print "Total comparisons:", len(vector1)

		return shift

	def __shift_fast(self, vector1, vector2, debug=False):
		"""
		Returns how much a vector was shifted

		The method is almost always optimal but at least an order of
		magnitude faster than the exhaustive shift
		"""
		min_v1_index, _ = min(enumerate(vector1), key=operator.itemgetter(1))
		_, min_v2_value = min(enumerate(vector2), key=operator.itemgetter(1))

		val = min_v2_value + float(MINIMUM_THRESHOLD) / len(vector1)
		min_v2_indices = [i for i, x in enumerate(vector2) if x <= val]

		bestShift = -1
		bestDist = float("inf")
		for v2_index in min_v2_indices:
			shift = min_v1_index - v2_index
			cycled_values = np.roll(vector2, shift)
			d = squareEuclideanDistance(cycled_values, vector1)
			if d < bestDist:
				bestDist = d
				bestShift = shift

		if debug:
			v2 = np.roll(vector2, bestShift)
			print "Best distance:", bestDist
			print "Total comparisons:", len(min_v2_indices)

		return bestShift
