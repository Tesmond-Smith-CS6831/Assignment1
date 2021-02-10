# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale
#
# Code taken from ZeroMQ examples with additional
# comments or extra statements added to make the code
# more self-explanatory  or tweak it for our purposes
#
# We are executing these samples on a Mininet-emulated environment
#
#


#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq
import random

# Updated subscriber for assignment1
class Subscriber:

    def __init__(self, address, port, topic, timeToListen):
        self.address = address
        self.port = port
        self.totalTemp = 0
        self.zipCode = topic
        self.totalTimesToListen = timeToListen
        self.listenCounter = 0
        self.createContext(topic)

    def createContext(self, topic):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{self.address}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    def getMessage(self):
        self.message = self.socket.recv_string()
        zipcode, temperature, relhumidity = self.message.split()
        self.totalTemp += int(temperature)
        self.listenCounter += 1
        print("Relative humidity was: %d" % relhumidity)
        if self.listenCounter.__eq__(self.totalTimesToListen):
            self.printMessage(zipcode, temperature)
            self.context.term()

    def printMessage(self, zipcode, temperature):
        print("Average temperature for zipcode %s is %dF" % self.zipCode, temperature / self.totalTimesToListen + 1)


"""
#  Socket to talk to server
context = zmq.Context()

# Since we are the subscriber, we use the SUB type of the socket
socket = context.socket(zmq.SUB)

# Here we assume publisher runs locally unless we
# send a command line arg like 10.0.0.1
srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connect_str = "tcp://" + srv_addr + ":5556"

print("Collecting updates from weather server...")
socket.connect(connect_str)

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"

# Python 2 - ascii bytes to unicode str
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')

# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
# system what it is interested in
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# Process 10 updates
total_temp = 0
for update_nbr in range(10):
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)

print("Average temperature for zipcode '%s' was %dF" % (
      zip_filter, total_temp / (update_nbr+1))
)
"""

#create the subscriber
rN = random.randint(1,10)
if rN > 5:
    addressType = "localhost"
else:
    addressType = "10.0.0.1"
#Idk why its > 1 or 2 so ima just do 1, set default to NYC again
topic = sys.argv[1] if (sys.argv) > 1 else "10001"
sub = Subscriber(addressType, "6663, topic, 10")
sub.getMessage()