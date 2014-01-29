from BrickPi import *   #import BrickPi.py file to use BrickPi operations

# Define parameters
M_PI = 3.14159265359
W_RADIUS = 2.2 # wheel radius in cm
RW_DIST = 6.3 # distance from center of the robot to center of the wheel

FWD_SIGN = -1
FWD_VEL = FWD_SIGN*200

ROT_VEL = FWD_SIGN*200

LEFT_MOTOR = PORT_A
RIGHT_MOTOR = PORT_B

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
	print "Move forward ", prefer_dist, " cm."
	current_dist = 0
	current_left = 0
	current_right = 0
	while(current_dist < prefer_dist):
		BrickPi.MotorSpeed[LEFT_MOTOR] = FWD_VEL
		BrickPi.MotorSpeed[RIGHT_MOTOR] = FWD_VEL
		time.sleep(.05)
		left_move = getEncoderMovingDistance(LEFT_MOTOR)
		right_move = getEncoderMovingDistance(RIGHT_MOTOR)
		current_left += left_move
		current_right += right_move
		current_dist = (current_left + current_right)/2 #can change this

		print "C : ", current_dist
		print "L : ", current_left
		print "R : ", current_right
	motorStop()

# Function to turn for a specified angle(in radian)
def turn(prefer_angle):
	print "Turn ", prefer_angle, " radian."
	current_angle = 0
	while(current_angle < prefer_angle):
		BrickPi.MotorSpeed[LEFT_MOTOR] = -ROT_VEL
		BrickPi.MotorSpeed[RIGHT_MOTOR] = ROT_VEL
		time.sleep(.05)
		current_angle += (getEncoderMovingDistance(RIGHT_MOTOR) - getEncoderMovingDistance(LEFT_MOTOR))/RW_DIST #can change this
		print current_angle
	motorStop()

# Function to get encoder angle (in radian)
def getEncoderAngle(motor_port):
	BrickPiUpdateValues()
	degree = ( BrickPi.Encoder[motor_port] %720 ) /2
	radian = (degree*M_PI/180)
	return radian

# Function to change encoder steps into distance(in cm)
def getEncoderMovingDistance(motor_port):
	current_radian = getEncoderAngle(motor_port)
	if(motor_port == LEFT_MOTOR):	
		distance = toPIPI(current_radian - getEncoderMovingDistance.prev_radianL)*W_RADIUS
		getEncoderMovingDistance.prev_radianL = current_radian
	else:	
		distance = toPIPI(current_radian - getEncoderMovingDistance.prev_radianR)*W_RADIUS
		getEncoderMovingDistance.prev_radianR = current_radian
	return FWD_SIGN*distance

getEncoderMovingDistance.prev_radianL = getEncoderAngle(LEFT_MOTOR)
getEncoderMovingDistance.prev_radianR = getEncoderAngle(RIGHT_MOTOR)

# Function to limit the value of angle (radian) into [-PI, PI)
def toPIPI(angle):
	while(angle < -M_PI):
		angle += 2*M_PI
	while(angle >= M_PI):
		angle -= 2*M_PI
	return angle
# Main Program

motorForward(10)
#turn(M_PI/2)

