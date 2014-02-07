from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from robot import Robot
from constants import *
from random import uniform
import curses

robot = Robot(LEFT_MOTOR, RIGHT_MOTOR, None, None, None)

# Main Program

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

key = ''
while key != ord('q'):
    key = stdscr.getch()
    # stdscr.addch(20,25,key)
    # stdscr.refresh()
    if key == curses.KEY_UP: 
        # stdscr.addstr(2, 20, "Up")
        robot.forward(30)
    elif key == curses.KEY_DOWN: 
        # stdscr.addstr(3, 20, "Down")
        robot.forward(-30)
    if key == curses.KEY_LEFT:
    	# stdscr.addstr(4, 20, "Left")
    	robot.motors.turn(1)
    elif key == curses.KEY_RIGHT:
    	# stdscr.addstr(5, 20, "Right")
    	robot.motors.turn(-1)

curses.endwin()
