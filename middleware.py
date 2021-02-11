"""
Initial thoughts from Rick T:
    - creating anonymity is the goal
    - middleware could act as a hashtable with initialized buckets 'n' for number of zips
        - key: zipcode
        - value: weather stats
    - Publisher script calls into middleware hashtable to update value using ziptable[zip] = collected_weather
    - Subscriber script polls value from middleware using ziptable[zip] or ziptable.get(zip)

    - this allows for neither the client/server knowing the pub/sub servers
"""


from random import randrange
from xxlimited import Null

import sys
import zmq

# Socket to talk to server
from keyring.backends import null

class Broker:

    def __init__(self, frontend_port, backend_port, connect_ip_address):
        self.front = frontend_port
        self.back = backend_port
        self.ip_to_connect = connect_ip_address
        self.frontendSocket = None
        self.backendSocket = None
        self.context = None
        self.establish_broker(self.front, self.back)

    def establish_broker(self, frontend_port, backend_port):
        # Needed for zmq
        while True:
            self.context = zmq.Context()
            # Creation of the socket using XSUB & XPUB because of the potential n number of pubs and subs
            self.frontendSocket = self.context.socket(zmq.XSUB)
            self.backendSocket = self.context.socket(zmq.XPUB)
            # Bind the sockets to the appropriate address
            # self.frontendSocket.bind(f"tcp://*:{frontend_port}")
            self.frontendSocket.connect(f"tcp://{self.ip_to_connect}:{frontend_port}")
            self.backendSocket.bind(f"tcp://*:{backend_port}")
            # proxy the information from the publisher to the subscriber
            zmq.proxy(self.frontendSocket, self.backendSocket)


"""
context = zmq.Context();
# Since we are the middleware we need a pub and sub socket
# The thought of not have semicolons is insane
pubSocket = context.socket(zmq.PUB)
subSocket = context.socket(zmq.SUB)
# Setting the server address for the publisher
pubAddress = sys.argv[1] if len(sys.argv) > 1 else "localhost"
pubConnectionPoint = "tcp://" + pubAddress + ":6663"
# Create Publisher bit to push to subscribers
pubSocket.bind("tcp://*:6663")
# Taken from Dr. Gokhale's code
# publish forever ie publish function
def middlewarepublish(zipcode, temperature, relhumidity):
    pubSocket.send_string("%i" "%i" "%i" % (zipcode, temperature, relhumidity))
def middlewaresubscribe(zipcode, temperature, relhumidity):
    middlewarepublish(zipcode, temperature, relhumidity)
"""

# Creation of broker
if __name__ == "__main__":
    # address_type = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    ip_address = "localhost"
    broker = Broker("6663", "5556", ip_address)
