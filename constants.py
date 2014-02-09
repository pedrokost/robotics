import math
from BrickPi import *

M_PI = math.pi   # for backwards compatibility

W_RADIUS = 3 # wheel radius in cm
RW_DIST = 5.65 # distance from center of the robot to center of the wheel

EASING_C = 0.05  # determines acceleration strenght
FWD_SIGN = 1     # 1 means forward, -1 means backwards??

KEEP_DISTANCE_FRONT_KP = 30  # easing factor for maintaining equal distance from wall
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

LEFT_MOTOR = PORT_B     # Motor port left
RIGHT_MOTOR = PORT_A    # Motor port right

LEFT_TOUCH = PORT_2
RIGHT_TOUCH = PORT_1

SONAR_SENSOR = PORT_4   # sonar sensor port

# The array size of previous sonar meausurments
DISTANCE_HISTORY_SIZE = 5   # make it odd. 
