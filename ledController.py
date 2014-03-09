import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

# Turn the LEDs off initially
GPIO.output(12, False)
GPIO.output(13, False)

class LEDController:

	def __init__(self):
		pass

	@staticmethod
	def blink():
		for i in range(0, 5):
			GPIO.output(12, True)
			GPIO.output(13, True)
			time.sleep(0.1)
			GPIO.output(12, False)
			GPIO.output(13, False)
			time.sleep(0.1)

