from BrickPi import *
from math import *
from utilities import *

SCANNER_ACCEPTABLE_ANGLE = pi/180*5 # 1 degree
SCANNER_POWER = 200
SCANNER_ENCODER_RATIO = 8.0/40.0
SCANNER_FWD_SIGN = -1


class MotorScanner:
    #
    # Function to reset the motor
	def reset(self):
		self._prev_encoder_angle = self._getEncoderAngle()
		self._sonar_angle = 0

	#
	# Constructor
	def __init__(self, motorPort):
		self.motorPort = motorPort
		BrickPi.MotorEnable[motorPort]  = 1
		self.reset()

    #
    #	Function to rotate motor to a specific angle in specific direction (cw or ccw)
	def gotoAngle(self, prefer_angle, dir):
    	# check direction
		if(not (dir == 'cw') and not (dir == 'ccw')):
			print "dir must be either 'cw' or 'ccw'"

		# calculate moving direction
		if(dir == 'cw'):
			moving_dir = -1;
		else:
			moving_dir = 1;

		while(True):
	        # get the starting angle
			current_angle = self.getSonarAngle()

			# get angular distance to target
			diff_angle = getAngularDifferent(prefer_angle, current_angle)

			print "1 : ", radToDeg(current_angle), radToDeg(diff_angle)
			
			# check if it is at the goal state
			if((abs(diff_angle) < SCANNER_ACCEPTABLE_ANGLE) and (moving_dir*diff_angle < 0)):
				self._setMotorPower(-20*moving_dir) # break
				time.sleep(0.04)
				self._setMotorPower(0)
				break

			# # drive motor
			self._setMotorPower(SCANNER_POWER*moving_dir)

    #
    #    Function to set motor power
	def _setMotorPower(self, power):
		BrickPi.MotorSpeed[self.motorPort] = SCANNER_FWD_SIGN*int(round(power))
		BrickPiUpdateValues()
	
	#
	# Function to get current sonar angle
	def getSonarAngle(self):
		# get how far encoder is rotate
		current_encoder_angle = self._getEncoderAngle()
		diff = -getAngularDifferent(current_encoder_angle, self._prev_encoder_angle)
		self._prev_encoder_angle = current_encoder_angle

		# set to sonar angle
		self._sonar_angle = toPIPI(diff*SCANNER_ENCODER_RATIO + self._sonar_angle)

		return self._sonar_angle
	#
	# Function to get current encoder angle
	def _getEncoderAngle(self):
		BrickPiUpdateValues()
		degree = ( BrickPi.Encoder[self.motorPort] % 720 ) * 0.5
		radian = degree * math.pi / 180
		return radian


    # def motorRotateDegree(self,power,deg,port,sampling_time=.1):
    #     """Rotate the selected motors by specified degre

    #     Args:
    #       power    : an array of the power values at which to rotate the motors (0-255)
    #       deg    : an array of the angle's (in degrees) by which to rotate each of the motor
    #       port    : an array of the port's on which the motor is connected
    #       sampling_time  : (optional) the rate(in seconds) at which to read the data in the encoders

    #     Returns:
    #       0 on success

    #     Usage:
    #       Pass the arguments in a list. if a single motor has to be controlled then the arguments should be
    #       passed like elements of an array,e.g, motorRotateDegree([255],[360],[PORT_A]) or 
    #       motorRotateDegree([255,255],[360,360],[PORT_A,PORT_B])
    #     """

    #     num_motor=len(power)    #Number of motors being used
    #     init_val=[0]*num_motor
    #     final_val=[0]*num_motor
    #     BrickPiUpdateValues()  
    #     for i in range(num_motor):
    #         BrickPi.MotorEnable[port[i]] = 1        #Enable the Motors
    #         power[i]=abs(power[i])
    #         BrickPi.MotorSpeed[port[i]] = power[i] if deg[i]>0 else -power[i]  #For running clockwise and anticlockwise
    #         init_val[i]=BrickPi.Encoder[port[i]]        #Initial reading of the encoder  
    #         final_val[i]=init_val[i]+(deg[i]*2)        #Final value when the motor has to be stopped;One encoder value counts for 0.5 degrees
    #     run_stat=[0]*num_motor
    #     while True:
    #         result = BrickPiUpdateValues()          #Ask BrickPi to update values for sensors/motors
    #         if not result : 
    #             for i in range(num_motor):        #Do for each of the motors
    #                 if run_stat[i]==1:
    #                     continue
    #                 # Check if final value reached for each of the motors
    #                 if(deg[i]>0 and final_val[i]>init_val[i]) or (deg[i]<0 and final_val[i]<init_val[i]) :
    #                     # Read the encoder degrees
    #                     init_val[i]=BrickPi.Encoder[port[i]]
    #                 else:
    #                     run_stat[i]=1
    #                     BrickPi.MotorSpeed[port[i]]=-power[i] if deg[i]>0 else power[i]  #Run the motors in reverse direction to stop instantly
    #                     print "MB : ", BrickPi.MotorSpeed
    #                     BrickPiUpdateValues()
    #                     time.sleep(.04)
    #                     BrickPi.MotorEnable[port[i]] = 0
    #                     BrickPiUpdateValues()
    #         time.sleep(sampling_time)          #sleep for the sampling time given (default:100 ms)
    #         if(all(e==1 for e in run_stat)):        #If all the motors have already completed their rotation, then stop
    #           break
    #     return 0