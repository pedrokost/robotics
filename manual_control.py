from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
import tty, sys, select, termios, time

robot = Robot(LEFT_MOTOR, RIGHT_MOTOR)

# Main Program
def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

settings = termios.tcgetattr(sys.stdin)
key = ''

FWD_VEL = 500
ROT_VEL = 300

while key != 'q':
    key = getKey()
    if key == 'q': 
        print "pressed: q"
    if key == 'u':
        print "pressed: top"
        robot.motors._setMotorPower(LEFT_MOTOR, FWD_VEL)
        robot.motors._setMotorPower(RIGHT_MOTOR, FWD_VEL)
    if key == 'e':
        print "pressed: bottom"
        robot.motors._setMotorPower(LEFT_MOTOR, -FWD_VEL)
        robot.motors._setMotorPower(RIGHT_MOTOR, -FWD_VEL)
    if key == 'i':
        print "pressed: right"
        robot.motors._setMotorPower(LEFT_MOTOR, 0)
        robot.motors._setMotorPower(RIGHT_MOTOR, ROT_VEL)
    if key == 'n':
        print "pressed: left"
        robot.motors._setMotorPower(LEFT_MOTOR, ROT_VEL)
        robot.motors._setMotorPower(RIGHT_MOTOR, 0)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
