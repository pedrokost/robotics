from BrickPi import *
from utilities import *

class Sonar:
	def __init__(self, sonar):
		self.sonar = sonar
		BrickPi.SensorType[sonar] = TYPE_SENSOR_ULTRASONIC_CONT


	def getSmoothSonarDistance(self, duration):
		"""
		Returns a cleaned value for the distance, by sampling continuosly for duration seconds
		"""
		values = []
		start = time.time()
		while time.time() - start < duration:
			values.append(self._getSonarDistance())
			time.sleep(0.002)
		return median(values)

	# This function is to get sonar distance. (in cm)
	def _getSonarDistance(self):
		BrickPiUpdateValues()
		return BrickPi.Sensor[self.sonar]
