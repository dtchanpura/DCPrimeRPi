from time import sleep
import sys   		#for using arguments argv
argmnt=str(sys.argv[1]) #for fetching the first argument
def main():
	import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23,GPIO.OUT)
        if argmnt == 'ON':
                GPIO.output(23,True)
        elif argmnt == 'OFF':
                GPIO.output(23,False)
        else:
                GPIO.output(23,True)
                sleep(100)
                GPIO.output(23,False)

if __name__== '__main__':
        main()

