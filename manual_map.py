from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from particleFilter import *
from encoder import *
from random import uniform
from navigator import Navigator
import tty, sys, select, termios, time
import Tkinter
from utilities import mean
from random import randrange
# from Tkinter import Tk, Canvas, Frame, BOTH


def drawTrajectory(points):
	n = len(points)
	for i in range(0, n):
		x0 = DISPLAY_OFFSET_X + DISPLAY_SCALE_X*points[i][0]
		y0 = DISPLAY_OFFSET_Y + DISPLAY_SCALE_Y*points[i][1]
		x1 = DISPLAY_OFFSET_X + DISPLAY_SCALE_X*points[(i + 1)%n][0]
		y1 = DISPLAY_OFFSET_Y + DISPLAY_SCALE_Y*points[(i + 1)%n][1]
		print "drawLine:" + str((x0, y0, x1, y1))

GUI_SCALE = 10
WAYPOINT_RADIUS = 5
PARTICLE_RADIUS = 1


class App:
	wayPoints = [(0,0), (0,10)]

	def __init__(self, root):
		f = Tkinter.Frame(width=500, height=500, background="bisque")
		f.pack(padx=100, pady=100)
		# f.bind("<1>", self.OnMouseDown)
		f.pack(fill=Tkinter.BOTH, expand=1)
		self.canvas = Tkinter.Canvas(f)
		self.canvas.configure(background='black')
		self.canvas.bind("<1>", self.OnMouseDown)
		self.canvas.pack(fill=Tkinter.BOTH, expand=1)

		drawTrajectory(self.wayPoints)

		particles = []
		for x in xrange(1,100):
			particle = (randrange(-10, 10), randrange(-5, 5), randrange(-10, 10))
			particles.append(particle)
		self.redrawCanvas(particles)

		return

		leftMotorPort=LEFT_MOTOR
		rightMotorPort=RIGHT_MOTOR

		robot = Robot(leftMotorPort,
				rightMotorPort,
				leftTouchPort=LEFT_TOUCH,
				rightTouchPort=RIGHT_TOUCH,
				sonarPort=SONAR_SENSOR)

		encoder = Encoder()
		navigator = Navigator()

		# initialize particle filter
		particleFilter = ParticleFilter()
		particleFilter.initialize()


		#wayPoints = [(40, 0)]
		drawTrajectory(self.wayPoints)
		currentPointIndex = 0

		leftVel = 0
		rightVel = 0

		lastAction = 'forward'

		while True:
			time.sleep(0.05)

			# get encoder data (for actual run)
			enc_distL, enc_dtL = encoder.getMovingDistance(leftMotorPort);
			enc_distR, enc_dtR = encoder.getMovingDistance(rightMotorPort);

			enc_velL = enc_distL/enc_dtL;
			enc_velR = enc_distR/enc_dtL;

			#print enc_distL
			# temp encoder data (for simulation only)
			temp_dt = 0.05;
			enc_velL = leftVel;
			enc_velR = rightVel;
			enc_distL = leftVel*temp_dt;
			enc_distR = rightVel*temp_dt;


			# motion update
			particleFilter.motionUpdate(enc_distL, enc_distR)

			# measurement update
			particleFilter.measurementUpdate()

			# get predict state
			robotState = particleFilter.getPredictState()

			#print "From : ", int(robotState[0]), int(robotState[1]), int(robotState[2]*180/pi)
			#print "To : ", currentPointIndex, int(self.wayPoints[currentPointIndex][0]), int(self.wayPoints[currentPointIndex][1])

			# set control signal
			leftVel, rightVel, action = navigator.navigateToWaypoint(robotState, self.wayPoints[currentPointIndex])
			if action is not lastAction:
				robot.motors.reset()
			lastAction = action

			robot.motors.setVel(leftVel, rightVel, enc_velL, enc_velR)

			# set waypoint index
			if(abs(leftVel) < NEAR_ZERO and abs(rightVel) < NEAR_ZERO):
				currentPointIndex += 1

				while(currentPointIndex >= len(self.wayPoints)):
					robot.motors.reset()
					time.sleep(0.5)

			self.redrawCanvas(particleFilter.particleSet)
			# draw particle
			particleFilter.drawParticles()


	def redrawCanvas(self, particles=None):
		self.canvas.delete(Tkinter.ALL)
		lastPoint = None
		for point in self.wayPoints:
			x = point[0] * GUI_SCALE
			y = point[1] * GUI_SCALE

			self.canvas.create_oval(x-WAYPOINT_RADIUS, y-WAYPOINT_RADIUS, x+WAYPOINT_RADIUS, y+WAYPOINT_RADIUS, outline="red", fill="white", width=0)

			if lastPoint:
				x_old = lastPoint[0] * GUI_SCALE
				y_old = lastPoint[1] * GUI_SCALE
				self.canvas.create_line(x, y, x_old, y_old, arrow=Tkinter.FIRST, fill="grey" )
			lastPoint = point

		if particles:
			# robot_x = mean(particles[:][0])
			# robot_y = mean(particles[:][1])
			for particle in particles:
				x = int(particle[0]*GUI_SCALE)
				y = int(particle[1]*GUI_SCALE)
				self.canvas.create_oval(x-PARTICLE_RADIUS, y-PARTICLE_RADIUS, x+PARTICLE_RADIUS, y+PARTICLE_RADIUS, outline="blue", fill="yellow", width=0)

	def OnMouseDown(self, event):
		print "frame coordinates: %s/%s" % (event.x, event.y)
		# print "root coordinates: %s/%s" % (event.x_root, event.y_root)
		self.wayPoints.append((event.x/GUI_SCALE, event.y/GUI_SCALE))
		drawTrajectory(self.wayPoints)
		self.redrawCanvas()

root = Tkinter.Tk()
app  = App(root)
root.mainloop()
