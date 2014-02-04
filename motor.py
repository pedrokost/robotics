class Motors:
	def __init__(self, left_port, right_port):
		pass

	def stop(self):
		"""
		Stop Motors
		"""
		self._setMotorSpeed(self.leftMotor, 0)
		self._setMotorSpeed(self.rightMotor, 0)

	


	def _setMotorSpeed(self, motor_port, speed):
		BrickPi.MotorSpeed[motor_port] = speed
