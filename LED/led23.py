from time import sleep
import sys

argmnt=sys.argv
def main():
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23,GPIO.OUT)
	if argmnt == 'ON':
		GPIO.output(23,True)
	elif argmnt == 'OFF':
		GPIO.output(23,False)
	else:
		for i in range(0,10):	
			GPIO.output(23,True)
			sleep(1)
			GPIO.output(23,False)
			sleep(1)


if __name__== '__main__':
	main()


