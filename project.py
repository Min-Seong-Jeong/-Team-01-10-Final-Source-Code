import botbook_mcp3002 as mcp # for botbook_mcp3002 module import
							  # read gas sence
import time	# for using time.sleep()

import RPi.GPIO as GPIO # for using GPIO port
from sys import exit 	# for exception processing
import pygame.mixer     # for warning sound

GPIO.setmode(GPIO.BCM)  # set GPIO port as GPIO.BCM
GPIO.setup(17,GPIO.OUT) # moving motor
GPIO.setup(21,GPIO.IN)  # button input

# motor initialize
motor = GPIO.PWM(17,50) 
motor.start(7.5) 

# sound initialize
pygame.mixer.init(48000,-16,1,1024) 
warningSound = pygame.mixer.Sound("/home/pi/warning.wav") 
soundChannelA = pygame.mixer.Channel(1) 

tickSound = pygame.mixer.Sound("/home/pi/tick.wav")
soundChannelB = pygame.mixer.Channel(2)

# read Gas Function
def readPotent():

	global gasValue 
	gasValue = mcp.readAnalog() # read gas information from mcp-3002 

#m main Function
def main(): 

	isGas = 0
	count = 0
	flag = 0
	tickCount = 0

	print(" start program ")

	try:
		while True: # while Loop
			readPotent() # read Gas Funtion Call
			isButton = GPIO.input(21) # read button
			
			# burning the gas
			# for 10, call tickSound
			if (tickCount < 10): 
				tickCount = tickCount + 1
				soundChannelB.play(tickSound)

			if (gasValue > 600):	# gas on
				isGas = 1
				print(" Gas !!! ")
				print("The current potentiometer value is %i " % gasValue) # 
			
			if (isGas == 1): # gas count time per 0.5 sec
				count = count + 1
				soundChannelA.play(warningSound) # warning sound call
			
			time.sleep(0.5) # program timer per 0.5 sec
		
			if( count == 10 ): # time 0.5 * 10 = 5sec , motor on.
				motor.ChangeDutyCycle(12.5) 

			if( isButton == 1 ): # button on
				isGas = 0
				count = 0
				tickCount = 0
				motor.ChangeDutyCycle(7.5) # motor off.

	except KeyboardInterrupt:
		GPIO.cleanup()
if (__name__ == "__main__"): #main Function Start
	main()
