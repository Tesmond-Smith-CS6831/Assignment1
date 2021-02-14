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
#   Weather update server
#   Binds PUB socket to tcp://*:6663 or whatever system input socket is
#   Publishes random weather updates
#
import sys
import zmq
from random import randrange

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)


class Publisher:
    def __init__(self, port_to_bind):
        self.context = None
        self.socket = None
        self.port = port_to_bind
        self.initialize_context(port_to_bind)
        self.publish()

    def initialize_context(self, port_to_bind):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{self.port}")

    def publish(self):
        while True:
            zipcode = randrange(1, 100000)
            temperature = randrange(-80, 135)
            relhumidity = randrange(10, 60)

            self.socket.send_string("{} {} {}".format(zipcode, temperature, relhumidity))


if __name__ == "__main__":
    port_to_bind = sys.argv[1] if len(sys.argv) > 1 else "6663"
    publisher = Publisher(port_to_bind)
    publisher.publish()
