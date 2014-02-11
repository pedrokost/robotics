from constants import *
from math import *

NUMBER_OF_PARTICLES = 100

class ParticleFilter:
	def __init__(self):
		self.particleSet = []
		pass

	def initialize(self):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet.append((0, 0, 0)) # (x, y, th)
		pass

	def motionUpdate(self, distL, distR):
		# calculate estimated motion
		motionD = (distR + distL)/2
		motionTH = (distR - distL)/(2*RW_DIST)

		# update particle
		for i in range(0, NUMBER_OF_PARTICLES):
			if(distR*distL > 0):
				e = 0
				f = 0
				self.particleSet[i] = self._updateParticleTranslate(self.particleSet[i], motionD, e, f)
			else:
				g = 0
				self.particleSet[i] = self._updateParticleRotate(self.particleSet[i], motionTH, g)

	def measurementUpdate(self):
		pass

	def getPredictState(self):
		pass

	def drawParticles(self):
  		print "drawParticles:" + str(self.particleSet)
		pass


	def _updateParticleTranslate(self, particleState, motionD, e, f):
		newX = particleState[0] + (motionD + e)*cos(particleState[2])
		newY = particleState[1] + (motionD + e)*sin(particleState[2])
		newTH = particleState[2] + f
		return (newX, newY, newTH)

	def _updateParticleRotate(self, particleState, motionTH, g):
		newX = particleState[0]
		newY = particleState[1]
		newTH = particleState[2] + motionTH + g
		return (newX, newY, newTH)
