import signal 
import sys
import zmq
import json

def signal_handler(*args): 
    print(socket) 
    socked.close() 
    print('You pressed Ctrl+C!') 
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

context = zmq.Context()
producer = context.socket(zmq.PUSH)
producer.connect("tcp://192.168.53.11:5555")

topic = "0"
message = "{\"mac_dl_cqi\": 10}"

producer.send_string(f"{topic};{message}")

                                                                                                                        

