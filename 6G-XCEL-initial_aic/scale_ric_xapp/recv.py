import zmq

import signal
import sys
import json


def signal_handler(*args):
    print(socket)
    socked.close()
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


print("Merim1")
context = zmq.Context()
print("Merim2\n")

#  Socket to talk to server
print("Connecting to hello world server")
socket = context.socket(zmq.SUB)
#socket.connect("tcp://localhost:5555")
socket.connect("tcp://192.168.53.11:5554")
socket.setsockopt(zmq.LINGER, 0)
socket.setsockopt(zmq.SUBSCRIBE,b"")
socket.setsockopt(zmq.CONFLATE, 1)

print("connected")

#  Do 10 requests, waiting each time for a response
while True:
    message = json.loads(socket.recv().decode("utf-8"))
    print(message["timestamp"])
    with open("data.csv", "a") as file:
        file.write(str(message["timestamp"]))
        file.write(",")
        file.write(str(message["rnti"]))
        file.write(",")
        file.write(str(message["rbs_length"]))
        file.write("\n")
