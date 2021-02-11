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

# Updated subscriber for assignment1
class Subscriber:

    def __init__(self, address, port, topic, time_to_listen):
        self.address = address
        self.port = port
        self.totalTemp = 0
        self.zipCode = topic
        self.total_times_to_listen = time_to_listen
        self.listenCounter = 0
        self.message = None
        self.context = None
        self.socket = None
        self.create_context(topic)

    def create_context(self, topic):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{self.address}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    def get_message(self):
        for x in range(self.total_times_to_listen):
            print("Looking for message")
            self.message = self.socket.recv_string()
            print("Received message")
            zipcode, temperature, relhumidity = self.message.split()
            self.totalTemp += int(temperature)
            self.listenCounter += 1
            print("Relative humidity was: {}".format(relhumidity))
            if self.listenCounter == self.total_times_to_listen:
                print(self.print_message(zipcode, temperature))
                self.context.term()

    def print_message(self, zipcode, temperature):
        return "Average temperature for zipcode {} is {}".format(zipcode, temperature)


if __name__ == "__main__":
    #create the subscriber
    # rN = random.randint(1, 10)
    # if rN > 5:
    #     addressType = "localhost"
    # else:
    #     addressType = "10.0.0.1"
    #Idk why its > 1 or 2 so ima just do 1, set default to NYC again
    print("we're here")
    # address_type = '10.0.0.1'
    address_type = "localhost"
    topic = sys.argv[1] if len(sys.argv) > 1 else "10001"
    print(topic)
    sub = Subscriber(address_type, "5556", topic, 10)
    sub.get_message()
