#!/usr/bin/env python

from subprocess import * 
from lcdDisplay import lcdDisplay
from subprocess import * 
from twython import Twython
from time import sleep
from twitter_keys import *
lcd = lcdDisplay() #Object named lcd for using all the functions of lcdDisplay.py
#Contents of twitter_keys.py 
#CONSUMER_KEY='############YOUR APP##################################'
#CONSUMER_SECRET = '##########KEYS####################################'
#ACCESS_KEY = '###############FROM##http://dev.twitter.com##############'
#ACCESS_SECRET = '#########################################'

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 
lcd.begin(20,3)
hashtagvalue='DCPrimeRPi' # Search Query 
i=0

while 1:

	lcd.clear()
	i=0
	tweettag=api.search(q=hashtagvalue, lang='en')
	tweetcount=len(tweettag['statuses'])
	while i < (tweetcount):
		tweetdata=tweettag['statuses'][i]['text']
		tweetuser=tweettag['statuses'][i]['user']['screen_name']
		lcd.longmessage('@'+tweetuser+': '+tweetdata)
		i+=1
		sleep(4)
