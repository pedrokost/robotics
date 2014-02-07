from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
import tty

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



stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

key = ''
while key != ord('q'):
    key = getKey()
    print key

    # if key == curses.KEY_UP: 
    #     # stdscr.addstr(2, 20, "Up")
    #     robot.forward(30)
    # elif key == curses.KEY_DOWN: 
    #     # stdscr.addstr(3, 20, "Down")
    #     robot.forward(-30)
    # if key == curses.KEY_LEFT:
    # 	# stdscr.addstr(4, 20, "Left")
    # 	robot.motors.turn(1)
    # elif key == curses.KEY_RIGHT:
    # 	# stdscr.addstr(5, 20, "Right")
    # 	robot.motors.turn(-1)

