from .managers.XappManager import XappManager
from .helpers.Validator import Validator
from .RegisterXapp import RegisterXapp
from .parse_config import parse_config
from .xapp_setup import check_entropy
from .managers.CommandManager import *
from .enums import *
import zmq
import sys
import json
import threading
import time

class XappController:

    def __init__(self):
        self.xApps = []
        self.topics = []
        self.read_topic = -1
        self.message = {}
        self.message_queue = {}
        # validate the xApps
        for xApp in XappManager.xApps.values():
            Validator.validate_xApp(xApp)

        register_xapp_inst = RegisterXapp()
        for xApp in XappManager.xApps.values():
            register_xapp_inst.register_xapp(xApp)

        # read configuration file
        self.config = parse_config('./xApp.conf')
        self.sub_socket = "tcp://" + register_xapp_inst.databus_ip + ":" + register_xapp_inst.rcv_port
        self.pub_socket = "tcp://" + register_xapp_inst.databus_ip + ":" + register_xapp_inst.send_port
        # self.sub_socket = "tcp://" + self.config["ip_address"] + ":" + self.config["recv_measurements"]
        # self.pub_socket = "tcp://" + self.config["ip_address"] + ":" + self.config["pub_commands"]

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
        self.consumer.setsockopt(zmq.SUBSCRIBE,b"%d" % 0)
        self.consumer.setsockopt(zmq.CONFLATE, 1)

        self.producer = self.context.socket(zmq.PUSH)
        self.producer.connect(self.pub_socket)

    def read_message(self):
        while True:
            # print("***************FIRST READING******************")
            message = self.consumer.recv().decode("utf-8")
            # print("**********************READING MESSAGE************************")
            # print(message)
            topic, payload = message.split(";")
            # print("**********************topic************************")
            # print(topic)
            # print("**********************payload ************************")
            # print(payload)
            self.read_topic = int(topic)
            self.message = json.loads(payload)
            # self.message = payload
            if self.read_topic in self.message_queue.keys():
                for xApp_i in self.message_queue[self.read_topic].keys():
                    self.message_queue[self.read_topic][xApp_i].append(self.message)
            # return 0
            # return json.loads(self.consumer.recv().decode("utf-8"))
            # return int(topic), json.loads(payload)

    def send_command(self, command):
        self.producer.send_string(command)
        print("Command sent")

    def __xApp_setup(self):
        for name, xApp in XappManager.xApps.items():
            print("Setting up %s xApp." % name)
            temp_xApp = xApp()
            self.xApps.append(temp_xApp)
            for topic in temp_xApp.cell_ids:
                self.topics.append(topic)
        self.topics = set(self.topics)

    def __set_topics(self):
        for topic in self.topics:
            self.consumer.setsockopt(zmq.SUBSCRIBE,b"%d" % topic)
            self.message_queue[topic] = {}
            for xApp in self.xApps:
                if topic in xApp.cell_ids:
                    self.message_queue[topic][xApp.u_name] = []

    def __execute(self, xApp):
        while True:
            # filter here based on the xApp interset
            measurements = []
            if xApp.read_measurements:
                for topic in xApp.cell_ids:
                #for _ in range(len(self.message_queue[topic][xApp.u_name])):
                    for _ in range(len(self.message_queue[topic][xApp.u_name])):
                        msg = self.message_queue[topic][xApp.u_name].pop(0)
                    # for msg in self.message_queue[topic][xApp.u_name]:
                        if MeasurementsHandler.ALL_MEASUREMENTS in xApp.read_measurements:
                            measurements.append(dict(msg.items()))
                        else:
                            measurements.append(dict(filter(lambda elem: elem[0] in xApp.read_measurements, msg.items())))
            xApp.process(measurements)
            # for _ in range(len(xApp.send_commands)):
            #     command = xApp.send_commands.pop(0)
            #     self.send_command(command_dict.get(command[0], default_cmd)(command[1]))
            time.sleep(xApp.time_interval)

    def run(self):
        self.__xApp_setup()
        self.__set_topics()
        # while True:
        threading.Thread(target=self.read_message).start()
        # topic, self.message = self.read_message()
        # print(topic)
        for xApp in self.xApps:
            try:
                threading.Thread(target=self.__execute, args=[xApp]).start()
            except:
                raise RuntimeError("Unable to start thread.")
