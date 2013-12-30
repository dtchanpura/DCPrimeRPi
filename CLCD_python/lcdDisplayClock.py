#!/usr/bin/python

from lcdDisplay import lcdDisplay
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

lcd = lcdDisplay()

cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
rxpack= "ifconfig eth0 | grep 'RX bytes' | cut -d'(' -f2 | cut -d')' -f1"
txpack= "ifconfig eth0 | grep 'TX bytes' | cut -d':' -f3 -d'(' | cut -d')' -f1"
filepath="/var/www/logs.txt"

lcd.begin(20,3)


def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output
lcd.clear()
while 1:
	lcd.home()
	filehandle=open(filepath)
	"""	ipaddr = run_cmd(cmd)"""
	tx1=run_cmd(txpack)
	tx1=tx1+' '*(20-6-len(tx1))
	rx1=run_cmd(rxpack)
	rx1=rx1+' '*(20-6-len(rx1))
	text1=filehandle.read()
	text1=text1+' '*(20-len(text1))	
	lcd.longmessage(datetime.now().strftime('%b %d %Y    %H:%M') + 'Dwnld:%sUpldd:%s%s' % (rx1,tx1, text1 ))
	filehandle.close()
	sleep(3)
