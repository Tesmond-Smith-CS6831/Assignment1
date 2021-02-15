import sys
import zmq


class Subscriber:
    def __init__(self, address, port, topic, time_to_listen):
        self.address = address
        self.port = port
        self.total_temp = 0
        self.zip_code = topic
        self.total_times_to_listen = time_to_listen
        self.listen_counter = 0
        self.message = None
        self.context = None
        self.socket = None


    def create_context(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{self.address}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.zip_code)

    def get_message(self):
        for x in range(self.total_times_to_listen):
            self.message = self.socket.recv_string()
            zipcode, temperature, relhumidity = self.message.split()
            self.total_temp += int(temperature)
            self.listen_counter += 1
            print("Relative humidity was: {}".format(relhumidity))

        if self.listen_counter == self.total_times_to_listen:
            print(self.print_message(self.total_temp / self.total_times_to_listen))
            self.context.term()

    def print_message(self, temperature):
        return "Average temperature for zipcode {} is: {}".format(self.zip_code, temperature)


if __name__ == "__main__":
    address_type = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    topic = sys.argv[2] if len(sys.argv) > 2 else "10001"
    socket_port = sys.argv[3] if len(sys.argv) > 3 else "5556"
    print(topic)
    sub = Subscriber(address_type, socket_port, topic, 10)
    sub.create_context()
    sub.get_message()
