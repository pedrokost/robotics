from constants import *
from math import *
from utilities import *
from Map import *
from Canvas import *
import random

SIGMA_S = 3
LIK_K = 0.01

class ParticleFilter:
	particleSet = []
	particleDraw = []

	def initialize(self, Map):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet.append((0, 0, 0, 1/NUMBER_OF_PARTICLES))  # (x, y, th(radian), w)
			self.particleDraw.append((0, 0, 0)) # (x, y, th(degree))
		self.Map = Map

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

	def measurementUpdate(self, z):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet[i] *= _calculate_likelihood(self.particleSet[i][0], self.particleSet[i][1], self.particleSet[i][2], z)
		pass


	# likelihood function for particle at state(x, y, theta) and current sonar measurement is z
	def _calculate_likelihood(self, x, y, theta, z):
		nWalls = len(self.Map)

		best_m = -1
		# estimate sonar measurement from the predict one of each wall
		for i in range(0, nWalls):
			# predict m of this wall
			Ax = self.Map[i][0]
			Ay = self.Map[i][1]
			Bx = self.Map[i][2]
			By = self.Map[i][3]
			predictM = ((By - Ay)*(Ax - x) - (Bx - Ax)*(Ay - y)) / ((By - Ay)*cos(theta) - (Bx - Ax)*sin(theta))

			# calculate crashing point
			Cx = x + predictM*cos(theta)			
			Cy = y + predictM*sin(theta)

			# check if the point is in the wall boundary
			AB = (Bx - Ax, By - Ay)
			lenAB = sqrt(AB[0]*AB[0], AB[1]*AB[1])
			AC = (Cx - Ax, Cy - Ay)
			lenAC = sqrt(AC[0]*AC[0], AC[1]*AC[1])
			if(((AB[0]*AC[0] + AB[1]*AC[1] > 0) and (lenAC < lenAB)) == False):
				continue

			# check if predict distance is minimum
			if(best_m < 0):
				best_m = predictM
			else if(best_m > predictM)
				best_m = predictM

		if(best_m < 0):
			print "Something wrong!"

		# calculate likelihood
		dz = z - best_m;
		lik = exp(-(dz*dz)/(2*SIGMA_S*SIGMA_S)) + LIK_K

		return lik

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
		return (newX, newY, newTH, particleState[3])

	def _updateParticleRotate(self, particleState, motionTH, g):
		newX = particleState[0]
		newY = particleState[1]
		newTH = toPIPI(particleState[2] + motionTH + g)
		return (newX, newY, newTH, particleState[3])
