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
        self.frontend_socket = None
        self.backend_socket = None
        self.context = None
        self.establish_broker(self.front, self.back, self.ip_to_connect)

    def establish_broker(self, frontend_port, backend_port, host):
        while True:
            self.context = zmq.Context()
            self.frontend_socket = self.context.socket(zmq.XSUB)
            self.backend_socket = self.context.socket(zmq.XPUB)
            self.frontend_socket.connect(f"tcp://{host}:{frontend_port}")
            self.backend_socket.bind(f"tcp://*:{backend_port}")
            zmq.proxy(self.frontend_socket, self.backend_socket)


if __name__ == "__main__":
    ip_address = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    broker = Broker("6663", "5556", ip_address)
