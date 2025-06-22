from .parse_config import parse_config
from .xapp_setup import check_entropy
import zmq
import json

class xAppInterface:
    def __init__(self):
        # read configuration file
        self.config = parse_config('./xApp.conf')
        self.sub_socket = "tcp://" + self.config["ip_address"] + ":" + self.config["recv_measurements"]
        self.pub_socket = "tcp://" + self.config["ip_address"] + ":" + self.config["pub_commands"]

        # check entropy before establishing the connection with the databus
        check_entropy()

        print("Connecting to the databus****************")
        # connect to the databus pub and sub sockets
        self.connect()

    def connect(self):
        self.context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to the databus")
        self.consumer = self.context.socket(zmq.SUB)
        self.consumer.connect(self.sub_socket)
        self.consumer.setsockopt(zmq.LINGER, 0)
        self.consumer.setsockopt(zmq.SUBSCRIBE,b"")
        self.consumer.setsockopt(zmq.CONFLATE, 1)

        self.producer = self.context.socket(zmq.REQ)
        self.producer.connect(self.pub_socket)

    def read_message(self):
        return self.producer.recv().decode("utf-8")

    def send_command(self, command):
        # self.producer.send(command)
        # self.producer.send_string(command)
        self.producer.send_json(command)
        print("Command sent")

    # def __del__(self):
    #     self.producer.close()
    #     self.consumer.close()
    #     self.contex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t.term()
