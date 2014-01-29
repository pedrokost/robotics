from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import math
# Define parameters
M_PI = math.pi
W_RADIUS = 3 # wheel radius in cm
RW_DIST = 5.65 # distance from center of the robot to center of the wheel

EASING_C = 0.05
FWD_SIGN = 1
FWD_VEL0 = FWD_SIGN*80
FWD_VEL = FWD_SIGN*200

ROT_VEL = FWD_SIGN*100

LEFT_MOTOR = PORT_B
RIGHT_MOTOR = PORT_A

BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

# Function to stop the robot
def motorStop():
	print "Stop"
	BrickPi.MotorSpeed[LEFT_MOTOR] = 0
	BrickPi.MotorSpeed[RIGHT_MOTOR] = 0

# Function to move forward for a specified distance(in cm)
def motorForward(prefer_dist):
	resetEncoder()
	print "Move forward ", prefer_dist, " cm."
	current_dist = 0
	current_left = 0
	current_right = 0
	dummy_vel = 0
	dummy_weight = 20
	
	main_vel = FWD_VEL0
	
	#get direction sign	
	dir_sign = 1
	if(prefer_dist < 0):
		dir_sign = -1

	#loop for moving
	while(abs(current_dist) < abs(prefer_dist)):
		BrickPi.MotorSpeed[LEFT_MOTOR] = dir_sign*(main_vel) + dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
		BrickPi.MotorSpeed[RIGHT_MOTOR] = dir_sign*(main_vel) - dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
		time.sleep(.05)
		left_move = getEncoderMovingDistance(LEFT_MOTOR)
		right_move = getEncoderMovingDistance(RIGHT_MOTOR)
		current_left += left_move
		current_right += right_move
		current_dist = (current_left + current_right)/2
		dummy_vel = (abs(current_right) - abs(current_left))/2
		print "L : ", current_left
		print "R : ", current_right
		print "Current distance", current_dist
		
		#change main speed
		main_vel += int(round((FWD_VEL - main_vel)*EASING_C))
	motorStop()

# Function to turn for a specified angle(in radian)
def motorTurn(prefer_angle):
	resetEncoder()
	print "Turn ", prefer_angle, " radian."
	current_angle = 0
	current_left = 0
	current_right = 0
	dummy_vel = 0
	dummy_weight = 40

	#get direction sign	
	dir_sign = 1
	if(prefer_angle < 0):
		dir_sign = -1

	while(abs(current_angle) < abs(prefer_angle)):
		BrickPi.MotorSpeed[LEFT_MOTOR] = -(dir_sign*ROT_VEL + dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight)))
		BrickPi.MotorSpeed[RIGHT_MOTOR] = dir_sign*ROT_VEL - dir_sign*FWD_SIGN*int(round(dummy_vel*dummy_weight))
		time.sleep(.05)
		left_move = getEncoderMovingDistance(LEFT_MOTOR)
		right_move = getEncoderMovingDistance(RIGHT_MOTOR)
		current_left += left_move
		current_right += right_move
		current_angle = (current_right - current_left)/(2*RW_DIST) #can change this
		dummy_vel = (abs(current_right) - abs(current_left))/2
		print "L : ", current_left
		print "R : ", current_right
		print "Current angle : ", current_angle
	motorStop()

# Function to get encoder angle (in radian)
def getEncoderAngle(motor_port):
	BrickPiUpdateValues()
	degree = ( BrickPi.Encoder[motor_port] %720 ) /2
	radian = (degree*M_PI/180)
	return radian

# Function to change encoder steps into distance(in cm)Current distance 36.0759556387

def getEncoderMovingDistance(motor_port):
	current_radian = getEncoderAngle(motor_port)
	if(motor_port == LEFT_MOTOR):	
		distance = toPIPI(current_radian - getEncoderMovingDistance.prev_radianL)*W_RADIUS
		getEncoderMovingDistance.prev_radianL = current_radian
	else:	
		distance = toPIPI(current_radian - getEncoderMovingDistance.prev_radianR)*W_RADIUS
		getEncoderMovingDistance.prev_radianR = current_radian
	return FWD_SIGN*distance

def resetEncoder():
	getEncoderMovingDistance.prev_radianL = getEncoderAngle(LEFT_MOTOR)
	getEncoderMovingDistance.prev_radianR = getEncoderAngle(RIGHT_MOTOR)


# Function to limit the value of angle (radian) into [-PI, PI)
def toPIPI(angle):
	while(angle < -M_PI):
		angle += 2*M_PI
	while(angle >= M_PI):
		angle -= 2*M_PI
	return angle
      
# Function to turn left 90 degrees
def Left90deg():
	motorTurn(M_PI/2 - 0*M_PI/180)
	
# Function to turn right 90 degrees
def Right90deg():
	motorTurn(-M_PI/2)

# Main Program
# Left90deg()
for i in range(0, 4):
	motorForward(42)
	time.sleep(1)
	Left90deg()
	time.sleep(1)

#motorForward(40)