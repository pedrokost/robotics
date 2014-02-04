from BrickPi import *

class Touch:
	def __init__(self, touch):
		self.touch = touch
		BrickPi.SensorType[touch] = TYPE_SENSOR_TOUCH

	def isTouch(self):
		BrickPiUpdateValues()
		return BrickPi.Sensor[self.touch]

