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
import sys
import zmq


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
            self.frontendSocket.connect(f"tcp://{self.ip_to_connect}:{frontend_port}")
            self.backendSocket.bind(f"tcp://*:{backend_port}")
            # proxy the information from the publisher to the subscriber
            zmq.proxy(self.frontendSocket, self.backendSocket)


# Creation of broker
if __name__ == "__main__":
    ip_address = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    socket_to_pub = sys.argv[2] if len(sys.argv) > 2 else "6663"
    socket_to_sub = sys.argv[3] if len(sys.argv) > 3 else "5556"
    broker = Broker(socket_to_pub, socket_to_sub, ip_address)
