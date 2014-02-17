import time, sys, random

# Each call to this method will draw a single line without clearing the
# canvas (multiple calls will result in multiple lines on the screen).
# A line should be presented as a tuple (x0, y0, x1, y1).
# Example: drawLine((0, 0, 10, 10))
def drawLineTuple(line):
  print "drawLine:" + str(line)

# Each call to this method will draw a single line without clearing the
# canvas (multiple calls will result in multiple lines on the screen).
# Example: drawLine(0, 0, 10, 10)
def drawLine(x0, y0, x1, y1):
  drawLineTuple((x0, y0, x1, y1))

# Each call to this method will clear the previous particles (but wil not
# affect any lines that have been drawn) and then will draw the particles
# given by its argument. The particles argument is a list of individual
# particles for instance [p1, p2, p3, p4], where pi = (x_i, y_i, theta_i).
# Example: drawParticles([(0, 0, 2), (5, 4, 5)])
def drawParticles(particles):
  print "drawParticles:" + str(particles)

if __name__ == "__main__":
  c = 0;
  def getRandomX():
    return random.randint((c % 10) * 50, (c % 10 + 1) * 50)

  def getRandomY():
    return random.randint((c % 10) * 50, (c % 10 + 1) * 50)

  def getRandomTheta():
    return random.randint(0, 360)

  numberOfParticles = 100

  drawLine(10, 10, 10, 500) # (x0, y0, x1, y1)
  drawLine(20, 20, 500, 200)  # (x0, y0, x1, y1)

  while True:
    # Create a list of particles to draw. This list should be filled by tuples (x, y, theta).
    particles = [(getRandomX(), getRandomY(), getRandomTheta()) for i in range(numberOfParticles)]
    drawParticles(particles)
    c += 1;
    time.sleep(0.05)
