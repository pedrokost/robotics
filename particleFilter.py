from constants import *
from math import *
from utilities import *
from random import uniform, gauss
from bisect import bisect
from Map import *
from Canvas import *

SIGMA_S = 3
LIK_K = 0.01

class ParticleFilter:
	particleSet = []
	particleDraw = []

	def __init__(self, Map, canvas):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet.append((0, 0, 0, 1/NUMBER_OF_PARTICLES))  # (x, y, th(radian), w)
			self.particleDraw.append((0, 0, 0)) # (x, y, th(degree))
		self.Map = Map
		self.canvas = canvas

	def motionUpdate(self, distL, distR):
		# calculate estimated motion
		motionD  = (distR + distL)/2            # average moved direction of both wheels
		motionTH = (distR - distL)/(2*RW_DIST)  # rotation (voluntary or not) 

		# update particle
		for i in range(0, NUMBER_OF_PARTICLES):
			going_straight = distR*distL > 0 # if both motors moved to same direction, it goes forward
			if going_straight:
				e = gauss(0, SIGMA_E)
				f = gauss(0, SIGMA_F)
				if(i == 0): # use first particle as mean
					e = 0
					f = 0
				self.particleSet[i] = self._updateParticleTranslate(self.particleSet[i], motionD, e, f)
			else:  # rotating
				g = gauss(0, SIGMA_G)
				if(i == 0): # use first particle as mean
					g = 0
				self.particleSet[i] = self._updateParticleRotate(self.particleSet[i], motionTH, g)

	def measurementUpdate(self, z):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet[i] *= _calculate_likelihood(self.particleSet[i][0], self.particleSet[i][1], self.particleSet[i][2], z)
		pass

	def compute_m(self, Ax, Ay, Bx, By, x, y, theta):
		return ((By - Ay)*(Ax - x) - (Bx - Ax)*(Ay - y)) / ((By - Ay)*cos(theta) - (Bx - Ax)*sin(theta))

	def wall_intersection(self, x, m, theta):
		Cx = x + m*cos(theta)			
		Cy = y + m*sin(theta)
		return Cx, Cy

	def is_wall_boundary(self, Ax, Ay, Bx, By, Cx, Cy):
		AB = (Bx - Ax, By - Ay)
		lenAB = sqrt(AB[0]*AB[0], AB[1]*AB[1])
		AC = (Cx - Ax, Cy - Ay)
		lenAC = sqrt(AC[0]*AC[0], AC[1]*AC[1])
		return ((AB[0]*AC[0] + AB[1]*AC[1] > 0) and (lenAC < lenAB))

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
			predictM = self.compute_m(Ax, Ay, Bx, By, x, y, theta)

			# calculate crashing point
			Cx, Cy = self.wall_intersection(x, m, theta)

			# check if the point is in the wall boundary
			if not self.is_wall_boundary(Ax, Ay, Bx, By, Cx, Cy):
				continue

			# check if predict distance is minimum
			if(best_m < 0):
				best_m = predictM
			elif(best_m > predictM):
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

	def normalizeWeights(self):
		"""
		Normalizes the weight of the particles so that they all sum to 1
		"""
		s = sum([p[3] for p in self.particleSet])
		self.particleSet = [(x, y, t, w/s) for (x, y, t, w) in self.particleSet]

	def resample(self):
		"""
		Weight-proportionally resamples particles so that those with higher weight are more
		likely to reproduce. The new particles have all uniform weights
		"""
		weights = [p[3] for p in self.particleSet]
		cumWeights = list(cumsum(weights))
		newParticleSet = []
		for i in xrange(0, NUMBER_OF_PARTICLES):
			index = bisect(cumWeights, uniform(0, 1))  # O(logn)
			(x, y, t, _) = self.particleSet[index]
			newParticleSet.append( (x, y, t, 1./NUMBER_OF_PARTICLES) )
		self.particleSet = newParticleSet

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
