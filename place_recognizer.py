from signature import Signature
from constants import NUMBER_OF_SIGNATURE_BINS
from utilities import degToRad, radToDeg

class PlaceRecognizer:

	ALLOWED_DISTANCE = 0.3

	"""Handles waypoint recognition"""
	def __init__(self, args):

		# Degree to rotate before each scan
		HIGH_ACCURACY = degToRad(3)
		LOW_ACCURACY = degToRad(10)
		
		self.sonarScanner = args['sonarScanner']
		self.recognizer = args['signatureRecognizer']
		self.scannerAccuracy = HIGH_ACCURACY if args['accurateScan'] is True else LOW_ACCURACY
		self.thetaAccuracy = args['accurateRecognition']

	def whereAmI(self):
		"""
		Returns the waypoint number and orientation of the robot
		"""
		print "Available sigs", map(lambda x: x.name, self.recognizer.sigs())

		# Perform a scan
		data = self.sonarScanner.scan(self.scannerAccuracy)
		s = Signature(data, NUMBER_OF_SIGNATURE_BINS)

		# Try to recognize the signature
		_, dist, closest = self.recognizer.closest(s)
		theta = self.recognizer.theta(closest, s, exhaustive=self.thetaAccuracy, debug=True)

		print dist
		# return the waypoint number and theta
		if dist > self.ALLOWED_DISTANCE:
			print "Place not recognized"
			return None, None
		
		print "Recognized place:", closest.name, "at rotation:", radToDeg(theta), "dist:", dist
		return closest.name, theta

