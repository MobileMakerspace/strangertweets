import time
import re
import os
import threading
import logging
import Queue
import opc
from dotenv import load_dotenv, find_dotenv
from twython import TwythonStreamer

#import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

load_dotenv(find_dotenv())

# Search terms
TERMS = '#KenBoneFacts'


# number of LEDS
numLEDS = 26

client = opc.Client('localhost:7890')
alpha = [(0,0,0)] * numLEDS

# Twitter application authentication
APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']



q = Queue.Queue(20)



# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        item = data['text'].encode('utf-8')
                        q.put(item)
                        logging.debug('Putting ' + str(item)
                              + ' : ' + str(q.qsize()) + ' items in queue')

        def on_error(self, status_code, data):
                print status_code, data



class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run2(self):
        while True:
            if not q.full():
                item = random.randint(1,10)
                q.put(item)
                logging.debug('Putting ' + str(item)  
                              + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(random.random())
        return


    def run(self):
        try:
            stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
            stream.statuses.filter(track=TERMS)
        except KeyboardInterrupt:
            quit()

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def cleanString(self, item):
        # make all lowercase
        item = item.lower()

        # check for obscenity

        # replace non-alpha
        item = re.sub('[^a-z]+', '', item)
        return item

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                logging.debug('Getting ' + str(item) 
                              + ' : ' + str(q.qsize()) + ' items in queue')
                # loop thru the string in item putting the pixels
                clean = self.cleanString(item)
                for c in clean:
                    pixel = ord(c) - ord('a')
                    print pixel
                    alpha[pixel] = (255,255,255)
                    client.put_pixels(alpha)
                    time.sleep(0.05)
                    alpha[pixel] = (0,0,0)
                    client.put_pixels(alpha)
                         
        return

if __name__ == '__main__':
    
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
