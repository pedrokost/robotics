from constants import *
from math import *
from utilities import *
import random

class ParticleFilter:
	particleSet = []
	particleDraw = []

	def initialize(self):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet.append((0, 0, 0))  # (x, y, th(radian))
			self.particleDraw.append((0, 0, 0)) # (x, y, th(degree))

	def motionUpdate(self, distL, distR):
		# calculate estimated motion
		motionD  = (distR + distL)/2            # average moved direction of both wheels
		motionTH = (distR - distL)/(2*RW_DIST)  # rotation (voluntary or not) 

		# update particle
		for i in range(0, NUMBER_OF_PARTICLES):
			going_straight = distR*distL > 0 # if both motors moved to same direction, it goes forward
			if going_straight:
				e = random.gauss(0, SIGMA_E)
				f = random.gauss(0, SIGMA_F)
				if(i == 0): # use first particle as mean
					e = 0
					f = 0
				self.particleSet[i] = self._updateParticleTranslate(self.particleSet[i], motionD, e, f)
			else:  # rotating
				g = random.gauss(0, SIGMA_G)
				if(i == 0): # use first particle as mean
					g = 0
				self.particleSet[i] = self._updateParticleRotate(self.particleSet[i], motionTH, g)

	def measurementUpdate(self):
		pass

	def getPredictState(self):
		return self.particleSet[0] # use first particle as mean

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
		for i in range(0, NUMBER_OF_PARTICLES):
			draw_x = int(self.particleSet[i][0]*DISPLAY_SCALE_X + DISPLAY_OFFSET_X)
			draw_y = int(self.particleSet[i][1]*DISPLAY_SCALE_Y + DISPLAY_OFFSET_Y)
			draw_th = int((self.particleSet[i][2] + pi)/pi*180) # change radian to degree
			self.particleDraw[i] = (draw_x, draw_y, draw_th)
  		print "drawParticles:" + str(self.particleDraw)

	def _updateParticleTranslate(self, particleState, motionD, e, f):
		newX = particleState[0] + (motionD + e)*cos(particleState[2])
		newY = particleState[1] + (motionD + e)*sin(particleState[2])
		newTH = toPIPI(particleState[2] + f)
		return (newX, newY, newTH)

	def _updateParticleRotate(self, particleState, motionTH, g):
		newX = particleState[0]
		newY = particleState[1]
		newTH = toPIPI(particleState[2] + motionTH + g)
		return (newX, newY, newTH)
