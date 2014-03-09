from math import *
from BrickPi import *

NEAR_ZERO = 0.0000001
M_PI = pi   # for backwards compatibility

W_RADIUS = 2 # 2.45 # wheel radius in cm # if move too much -> increase
RW_DIST = 5.25 # 6.2 #5.8 # distance from center of the robot to center of the wheel # if rotation is too much -> decrease
ENCODER_RATIO = 24.0/40.0 # Gear Parameter

EASING_C = 0.05  # determines acceleration strenght
FWD_SIGN = -1     # 1 means forward, -1 means backwards??

KEEP_DISTANCE_FRONT_KP = 20  # easing factor for maintaining equal distance from wall
KEEP_DISTANCE_FRONT_KI = 0.5
KEEP_DISTANCE_FRONT_KD = 30

FOLLOW_WALL_KP_NEAR = 10
FOLLOW_WALL_KP_FAR = 2  # affects how much the robot oscillates while following the wall (Proportonal)
FOLLOW_WALL_KI = 0.05  # affects how much the robot oscillates while following the wall (Integral)
FOLLOW_WALL_KD = 30  # affects how much the robot oscillates while following the wall (Integral)

# Velocities:
FWD_VEL  = FWD_SIGN*200  # Wanted max velocity
FWD_VEL0 = FWD_VEL * 0.3  # Velocity before acceleration
ROT_VEL  = FWD_SIGN*100  # Velocity of robot rotation
LOWEST_VEL = 55

LEFT_MOTOR = PORT_A     # Motor port left
RIGHT_MOTOR = PORT_C    # Motor port right

LEFT_TOUCH = PORT_2
RIGHT_TOUCH = PORT_1

SONAR_SENSOR = PORT_4   # sonar sensor port
SONAR_BIAS = 3

LIGHT_SENSOR = PORT_3

# The array size of previous sonar meausurments
DISTANCE_HISTORY_SIZE = 5   # make it odd. 

# for display
DISPLAY_SCALE_X = 10
DISPLAY_SCALE_Y = 10
DISPLAY_OFFSET_X = 200
DISPLAY_OFFSET_Y = 200


# Porticle filter constants
NUMBER_OF_PARTICLES = 100 #100
SIGMA_E = 0.1          # error noise when driving straight
SIGMA_F = 0.2*(pi/180)      	# angular error noise when driving straight
SIGMA_G = 0.7*(pi/180)   # angular error noise when rotating

# How aggresively should it turn towards the goal
# (determines the smoothness of the movement)
GOAL_GREADYNESS = 1  # if close to goal can be more aggressive ... higher


RESAMPLING_PERIOD = 5
DRAWING_PERIOD = 1

NUMBER_OF_SIGNATURE_BINS = 20
