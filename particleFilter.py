from constants import *
from math import *
from utilities import *
from random import uniform, gauss
from bisect import bisect
from Map import *
from Canvas import *

SIGMA_Z = 3
LIK_K = 0.05

class ParticleFilter:
	particleSet = []
	particleDraw = []

	def __init__(self, Map, canvas, start_pose):
		for i in range(0, NUMBER_OF_PARTICLES):
			self.particleSet.append((start_pose[0], start_pose[1], start_pose[2], 1.0/NUMBER_OF_PARTICLES))  # (x, y, th(radian), w)
			self.particleDraw.append((0, 0, 0, 0)) # (x, y, th(degree), w)
		self.Map = Map
		self.canvas = canvas

		#for x in range(40, 70):
		#	print x, " : ", self._calculate_likelihood(x, start_pose[1], start_pose[2], 25)

	def motionUpdate(self, distL, distR):
		# calculate estimated motion
		motionD  = (distR + distL)/2            # average moved direction of both wheels
		motionTH = (distR - distL)/(2*RW_DIST)  # rotation (voluntary or not) 
		
		# update particle merge rotate and translate
		#for i in range(0, NUMBER_OF_PARTICLES):
		#	e = gauss(0, SIGMA_E)
		#	f = gauss(0, SIGMA_F)
		#	self.particleSet[i] = self._updateParticle(self.particleSet[i], motionD, motionTH, e, f)
			
		# update particle separate rotate and translate
		for i in range(0, NUMBER_OF_PARTICLES):
			going_straight = distR*distL >=0 # if both motors moved to same direction, it goes forward or backward
			if going_straight:
				e = gauss(0, SIGMA_E)
				f = gauss(0, SIGMA_F)
				#if(i == 0): # preserved 0th index
				#	e = 0
				#	f = 0
				self.particleSet[i] = self._updateParticleTranslate(self.particleSet[i], motionD, e, f)
			else:  # rotating
				g = gauss(0, SIGMA_G)
				#if(i == 0): # preserved 0th index
				#	g = 0
				self.particleSet[i] = self._updateParticleRotate(self.particleSet[i], motionTH, g)

	def measurementUpdate(self, z):
		for i in range(0, NUMBER_OF_PARTICLES):
			p = self.particleSet[i]			
			new_w = self._calculate_likelihood(p[0], p[1], p[2], z)*p[3]
			self.particleSet[i] = (p[0], p[1], p[2], new_w)

	def compute_m(self, Ax, Ay, Bx, By, x, y, theta):
		bottom = ((By - Ay)*cos(theta) - (Bx - Ax)*sin(theta))
		if(bottom == 0):
			return 0
		return ((By - Ay)*(Ax - x) - (Bx - Ax)*(Ay - y)) / bottom

	def wall_intersection(self, x, y, theta, m):
		Cx = x + m*cos(theta)			
		Cy = y + m*sin(theta)
		return Cx, Cy

	def is_wall_boundary(self, Ax, Ay, Bx, By, Cx, Cy):
		AB = (Bx - Ax, By - Ay)
		lenAB = sqrt(AB[0]*AB[0] + AB[1]*AB[1])
		AC = (Cx - Ax, Cy - Ay)
		lenAC = sqrt(AC[0]*AC[0] + AC[1]*AC[1])
		return ((AB[0]*AC[0] + AB[1]*AC[1] > 0) and (lenAC < lenAB))

	def getIdealM(self):
		return self._get_predict_m(self.particleSet[0][0], self.particleSet[0][1], self.particleSet[0][2])  # preserved 0th index

	# return -1 if not intersect with any wall
	def _get_predict_m(self, x, y, theta):
		nWalls = len(self.Map.walls)

		best_m = -1
		# estimate sonar measurement from the predict one of each wall
		for i in range(0, nWalls):
			# predict m of this wall
			Ax = self.Map.walls[i][0]
			Ay = self.Map.walls[i][1]
			Bx = self.Map.walls[i][2]
			By = self.Map.walls[i][3]
			predictM = self.compute_m(Ax, Ay, Bx, By, x, y, theta)
			
			if(predictM < 0):
				continue

			# calculate crashing point
			Cx, Cy = self.wall_intersection(x, y, theta, predictM)

			# check if the point is in the wall boundary
			if not self.is_wall_boundary(Ax, Ay, Bx, By, Cx, Cy):
				continue
			
			# check if predict distance is minimum
			if(best_m < 0 or best_m > predictM):  # the first possible or better
				best_m = predictM			

		if(best_m < 0):
			print "Something wrong!"
			print (x, y, theta)
			time.sleep(100)

		return best_m


	# likelihood function for particle at state(x, y, theta) and current sonar measurement is z
	def _calculate_likelihood(self, x, y, theta, z):
		best_m = self._get_predict_m(x, y, theta)
		if(best_m < 0):
			print "Something wrong!"


		# calculate likelihood
		dz = z - best_m;
		lik = exp(-(dz*dz)/(2*SIGMA_Z*SIGMA_Z)) + LIK_K
		# print z, lik, dz, "----------"
		# 	print "Measured ", z, ""


		return lik

	def getPredictState(self):
		# maximum weight
		# bestIndex = 0
		# for i in range(1, NUMBER_OF_PARTICLES):
		# 	if(self.particleSet[bestIndex][3] < self.particleSet[i][3]):
		# 		bestIndex = i
			
		# return (self.particleSet[bestIndex][0], self.particleSet[bestIndex][1], self.particleSet[bestIndex][2])
		#return self.particleSet[0]  # preserved 0th index

		# mean
		
		best_x = 0
		best_y = 0
		best_th = 0
		for i in range(0, NUMBER_OF_PARTICLES):
			best_x += self.particleSet[i][3]*self.particleSet[i][0]
			best_y += self.particleSet[i][3]*self.particleSet[i][1]
			best_th += self.particleSet[i][3]*self.particleSet[i][2]
		
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
			r = uniform(0, 1)
			index = bisect(cumWeights, r) #Hack  # O(logn)
			#print "Chosen Index : ", index, "<", r, ">"
			(x, y, t, _) = self.particleSet[index]
			newParticleSet.append( (x, y, t, 1./NUMBER_OF_PARTICLES) )
		
		
		self.particleSet = newParticleSet

	def drawParticles(self):
		for i in range(0, NUMBER_OF_PARTICLES):
			draw_th = int((self.particleSet[i][2] + pi)/pi*180) # change radian to degree
			self.particleDraw[i] = (self.particleSet[i][0], self.particleSet[i][1], draw_th, self.particleSet[i][3])
		self.canvas.drawParticles(self.particleDraw)

	def _updateParticle(self, particleState, motionD, motionTH, e, f):
		newX = particleState[0] + (motionD + e)*cos(particleState[2])
		newY = particleState[1] + (motionD + e)*sin(particleState[2])
		newTH = toPIPI(particleState[2] + motionTH + f)
		return (newX, newY, newTH, particleState[3])

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
