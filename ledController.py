from BrickPi import *
from constants import *

class LEDController:

	def __init__(self):
		pass

	@staticmethod
	def ledOn():
		BrickPi.SensorType[LIGHT_SENSOR] = TYPE_SENSOR_LIGHT_ON
		BrickPiSetupSensors()

	@staticmethod
	def ledOff():
		BrickPi.SensorType[LIGHT_SENSOR] = TYPE_SENSOR_LIGHT_OFF
		BrickPiSetupSensors()

	@staticmethod
	def blink():
		LEDController.ledOn()
		time.sleep(1.0)
		LEDController.ledOff()

