import time
import os
from dotenv import load_dotenv, find_dotenv
from twython import TwythonStreamer

#import RPi.GPIO as GPIO

load_dotenv(find_dotenv())

# Search terms
TERMS = '#KenBoneFacts'

# GPIO pin number of LED
LED = 22

# Twitter application authentication
APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        print
                        #GPIO.output(LED, GPIO.HIGH)
                        #time.sleep(0.5)
                        #GPIO.output(LED, GPIO.LOW)
        def on_error(self, status_code, data):
                print status_code, data


# Setup GPIO as output
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(LED, GPIO.OUT)
#GPIO.output(LED, GPIO.LOW)

# Create streamer
try:
        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
        quit()
