from constants import *
from math import *
import random
# for display
DISPLAY_SCALE_X = 5
DISPLAY_SCALE_Y = 5
DISPLAY_OFFSET_X = 40
DISPLAY_OFFSET_Y = 40

# for particle filter
NUMBER_OF_PARTICLES = 100
sigmaE = 0.5
sigmaF = pi/720
sigmaG = pi/180



class ParticleFilter:
	def __init__(self):
		self.particleSet = []
		pass

	def initialize(self):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet.append((0, 0, 0)) # (x, y, th)
		pass

	def motionUpdate(self, distL, distR):
		print len(self.particleSet)
		# calculate estimated motion
		motionD = (distR + distL)/2
		motionTH = (distR - distL)/(2*RW_DIST)

		# update particle
		for i in range(0, NUMBER_OF_PARTICLES):
			if(distR*distL > 0):
				e = random.gauss(0, sigmaE)
				f = random.gauss(0, sigmaF)
				self.particleSet[i] = self._updateParticleTranslate(self.particleSet[i], motionD, e, f)
			else:
				g = random.gauss(0, sigmaG)
				self.particleSet[i] = self._updateParticleRotate(self.particleSet[i], motionTH, g)

	def measurementUpdate(self):
		pass

	def getPredictState(self):
		best_x = 0
		best_y = 0
		best_th = 0
		for i in range(0, NUMBER_OF_PARTICLES):
			best_x += self.particleSet[i][0]
			best_y += self.particleSet[i][1]
			best_th += self.particleSet[i][2]
		
		best_x /= NUMBER_OF_PARTICLES
		best_y /= NUMBER_OF_PARTICLES
		best_th /= NUMBER_OF_PARTICLES

		return (best_x, best_y, best_th)


	def drawParticles(self):
		displayParticleSet = []
		for i in range(0, NUMBER_OF_PARTICLES):
			disp_x = self.particleSet[i][0]*DISPLAY_SCALE_X + DISPLAY_OFFSET_X
			disp_y = self.particleSet[i][1]*DISPLAY_SCALE_Y + DISPLAY_OFFSET_Y
			disp_th = self.particleSet[i][2]
			displayParticleSet.append((disp_x, disp_y, disp_th))
  		print "drawParticles:" + str(displayParticleSet)

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
