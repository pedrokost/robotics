import math
from BrickPi import PORT_A, PORT_B

M_PI = math.pi   # for backwards compatibility

W_RADIUS = 3 # wheel radius in cm
RW_DIST = 5.65 # distance from center of the robot to center of the wheel

EASING_C = 0.05  # determines acceleration strenght
SMOOTH_DISTANCE = 5  # easing factor for maintaining equal distance from wall
FWD_SIGN = 1     # 1 means forward, -1 means backwards??

# Velocities:
FWD_VEL0 = FWD_SIGN*80  # ???
FWD_VEL  = FWD_SIGN*200  # ???
ROT_VEL  = FWD_SIGN*100  # Velocity of robot rotation

LEFT_MOTOR = PORT_B     # Motor port left
RIGHT_MOTOR = PORT_A    # Motor port right

LEFT_TOUCH = PORT_2
RIGHT_TOUCH = PORT_1

SONAR_SENSOR = PORT_3   # sonar sensor port