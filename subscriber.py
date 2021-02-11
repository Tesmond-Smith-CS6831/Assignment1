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

        self.create_context(self.zip_code)

    def create_context(self, zip_code):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{self.address}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, zip_code)

    def get_message(self):
        for x in range(self.total_times_to_listen):
            self.message = self.socket.recv_string()
            zipcode, temperature, relhumidity = self.message.split()
            self.total_temp += int(temperature)
            self.listen_counter += 1
            if self.listen_counter == self.total_times_to_listen:
                print(self.print_message(zipcode, temperature))
                self.context.term()

    def print_message(self, zipcode, temperature):
        return "Average temperature for zipcode {} is: {}".format(zipcode, temperature)


if __name__ == "__main__":
    address_type = "localhost"
    topic = sys.argv[1] if len(sys.argv) > 1 else "10001"
    print("Finding average temp for {}...".format(topic))
    sub = Subscriber(address_type, "5556", topic, 10)
    sub.get_message()
