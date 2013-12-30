#!/usr/bin/python

#
# based on code from lrvick and LiquidCrystal
# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp
#

from time import sleep

class lcdDisplay:

    # commands
    LCD_CLEARDISPLAY 		= 0x01
    LCD_RETURNHOME 		= 0x02
    LCD_ENTRYMODESET 		= 0x04
    LCD_DISPLAYCONTROL 		= 0x08
    LCD_CURSORSHIFT 		= 0x10
    LCD_FUNCTIONSET 		= 0x20
    LCD_SETCGRAMADDR 		= 0x40
    LCD_SETDDRAMADDR 		= 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT 		= 0x00
    LCD_ENTRYLEFT 		= 0x02
    LCD_ENTRYSHIFTINCREMENT 	= 0x01
    LCD_ENTRYSHIFTDECREMENT 	= 0x00

    # flags for display on/off control
    LCD_DISPLAYON 		= 0x04
    LCD_DISPLAYOFF 		= 0x00
    LCD_CURSORON 		= 0x02
    LCD_CURSOROFF 		= 0x00
    LCD_BLINKON 		= 0x01
    LCD_BLINKOFF 		= 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE 		= 0x08
    LCD_CURSORMOVE 		= 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE 		= 0x08
    LCD_CURSORMOVE 		= 0x00
    LCD_MOVERIGHT 		= 0x04
    LCD_MOVELEFT 		= 0x00

    # flags for function set
    LCD_8BITMODE 		= 0x10
    LCD_4BITMODE 		= 0x00
    LCD_2LINE 			= 0x08
    LCD_1LINE 			= 0x00
    LCD_5x10DOTS 		= 0x04
    LCD_5x8DOTS 		= 0x00
    # line addresses	
    LCD_LINE1			= 0x80	
    LCD_LINE2                   = 0xC0
    LCD_LINE3                   = 0x94
    LCD_LINE4                   = 0xD4


    def __init__(self, pin_rs=25, pin_e=24, pins_db=[23, 17, 27, 22], GPIO = None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin_e, GPIO.OUT)
        self.GPIO.setup(self.pin_rs, GPIO.OUT)

        for pin in self.pins_db:
            self.GPIO.setup(pin, GPIO.OUT)

        self.write4bits(0x33) # initialization
        self.write4bits(0x32) # initialization
        self.write4bits(0x28) # 2 line 5x7 matrix
        self.write4bits(0x0C) # turn cursor off 0x0E to enable cursor
        self.write4bits(0x06) # shift cursor right

        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        """ Initialize to default text direction (for romance languages) """
        self.displaymode =  self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode) #  set the entry mode

        self.clear()


    def begin(self, cols, lines):

        if (lines > 1):
                self.numlines = lines
                self.displayfunction |= self.LCD_2LINE
                self.currline = 0


    def home(self):

        self.write4bits(self.LCD_RETURNHOME) # set cursor position to zero
        self.delayMicroseconds(3000) # this command takes a long time!
        

    def clear(self):

        self.write4bits(self.LCD_CLEARDISPLAY) # command to clear display
        self.delayMicroseconds(3000)	# 3000 microsecond sleep, clearing the display takes a long time


    def setCursor(self, col, row):

        self.row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]

        if ( row > self.numlines ): 
                row = self.numlines - 1 # we count rows starting w/0

        self.write4bits(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))


    def noDisplay(self): 
        """ Turn the display off (quickly) """

        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)


    def display(self):
        """ Turn the display on (quickly) """

        self.displaycontrol |= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)


    def noCursor(self):
        """ Turns the underline cursor on/off """

        self.displaycontrol &= ~self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)


    def cursor(self):
        """ Cursor On """

        self.displaycontrol |= self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)


    def noBlink(self):
        """ Turn on and off the blinking cursor """

        self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)


    def noBlink(self):
        """ Turn on and off the blinking cursor """

        self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)


    def DisplayLeft(self):
        """ These commands scroll the display without changing the RAM """

        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)


    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """

        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT);


    def leftToRight(self):
        """ This is for text that flows Left to Right """

        self.displaymode |= self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode);


    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)


    def autoscroll(self):
        """ This will 'right justify' text from the cursor """

        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)


    def noAutoscroll(self): 
        """ This will 'left justify' text from the cursor """

        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)


    def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """

        self.delayMicroseconds(1000) # 1000 microsecond sleep

        bits=bin(bits)[2:].zfill(8)

        self.GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            self.GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i], True)

        self.pulseEnable()

        for pin in self.pins_db:
            self.GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i-4], True)

        self.pulseEnable()


    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)	# divide microseconds by 1 million for seconds
        sleep(seconds)


    def pulseEnable(self):
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)		# 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, True)
        self.delayMicroseconds(1)		# 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)		# commands need > 37us to settle


    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
                if char == '\2':
                        self.write4bits(self.LCD_LINE2) # 2nd line
                elif char == '\3':
                        self.write4bits(self.LCD_LINE3) # 3rd line
                elif char == '\4':
                        self.write4bits(self.LCD_LINE4) # 4th line
                else:
                        self.write4bits(ord(char),True)

    def splitnum(self, num,text):
            text1=[]
	    i=0
            while i<len(text):
	            text1.append(text[i:i+num])
        	    i+=num
            return text1

    def splitnumv2(self, num,text):
            text1=[]
            i=0
            while i<len(text):
                    text1.append(text[i:i+num])
                    i+=1
            return text1
    
                                    
    def longmessage(self, text):
#	    text=str(text)
	    if len(text)<80:
		    text=text+' '*(80-len(text))
	    li=0
	    for char in text:
		    if char=='\n':
			    text = text[:li] + ' ' + text[li+1:]
		    li+=1	
            text1=self.splitnumv2(4, self.splitnum(20,text))
	    print text1	    	
	    text1=text1[:len(text1)-3]
            """ Send string to LCD. Newline wraps to second line"""
            for screen in text1:
		    self.home()
                    l=0
#		    self.clear()		    
                    for line in screen:
			    line=line+' '*(20-len(line))
			    for char in line:
				    l+=1				    
                                    self.write4bits(ord(char),True)
 
				    if l==20:
					    self.write4bits(self.LCD_LINE2) # 2nd line
                                    elif l==40:
                                             
					    self.write4bits(self.LCD_LINE3) # 3rd line # changed
                                    elif l==60:
                                            
                                            self.write4bits(self.LCD_LINE4) # 4th line #changed
                 		    
		    sleep(4)
		
if __name__ == '__main__':

    lcd = lcdDisplay()
    lcd.home()
    lcd.clear()
    lcd.longmessage("1a2a3a4a5a6a7a8a9a0a1b2b3b4b5b6b7b8b9b0b1c2c3c4c5c6c7c8c9c0c1d2d3d4d5d6d7d8d9d0d1e2e3e4e5e6e7e8e9e0e1f2f3f4f5f6f7f8f9f0f")

