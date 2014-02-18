from constants import *
from random import uniform, gauss
from math import pi
from time import sleep
from utilities import cumsum
from bisect import bisect

def drawParticles(particles):
    particleDraw = []
    for i in range(0, NUMBER_OF_PARTICLES):
        draw_x = int(particles[i][0]*DISPLAY_SCALE_X + DISPLAY_OFFSET_X)
        draw_y = int(particles[i][1]*DISPLAY_SCALE_Y + DISPLAY_OFFSET_Y)
        draw_th = int((particles[i][2] + pi)/pi*180) # change radian to degree
        particleDraw.append( (draw_x, draw_y, draw_th) )
    print "drawParticles:" + str(particleDraw)


def normalizeWeights(particles):
    """
    Normalizes the weight of the particles so that they all sum to 1
    """
    s = sum([p[3] for p in particles])
    return [(x, y, t, w/s) for (x, y, t, w) in particles]


def resample(particles):
    """
    Weight-proportionally resamples particles so that those with higher weight are more
    likely to reproduce
    """
    weights = [p[3] for p in particles]
    cumWeights = list(cumsum(weights))
    # print cumWeights
    new_particles = []
    for i in xrange(0, NUMBER_OF_PARTICLES):
        rnd = uniform(0, 1)
        index = bisect(cumWeights, rnd)  # O(logn)
        (x, y, t, _) = particles[index]
        new_particles.append( (x, y, t, 1./NUMBER_OF_PARTICLES) )
    return new_particles


particles = []
for i in xrange(0, NUMBER_OF_PARTICLES):
    particles.append((uniform(1,10), uniform(1,10), uniform(0,2*pi), gauss(5, 2)))
particles = normalizeWeights(particles)


old_particles = particles
while True:
    particles = old_particles
    drawParticles(particles)
    particles_enum = resample(particles)
    particles = normalizeWeights(particles_enum)
    sleep(2)
    drawParticles(particles)
    sleep(2)
    break
