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
producer.connect("tcp://192.168.53.11:5556")

val = 0
while (val!='q'):
    val = input("Choose scheduling policy: ")
    if (str(val) == '0'): 
        producer.send_string("{ \"count\": {0, 0.1523,  0.2344, 0.3770, 0.6016, 0.8770, 1.1758, 1.4766, 1.9141, 1.9141, 1.9141, 1.9141, 1.9141, 1.9141, 1.9141,  1.9141 }") 
    elif (str(val) == '1'):
        producer.send_string("{ \"count\": {0, 0.1523, 0.1523, 0.2344, 0.2344, 0.2344, 0.3770, 0.3770, 0.3770, 0.6016, 0.6016, 0.6016, 0.8770, 0.8770, 1.1758, 1.1758 }") 
    elif (str(val) == '2'):
        producer.send_string("{ \"count\": {0, 0.1523, 0.1523, 0.2344, 0.2344, 0.2344, 0.3770, 0.3770, 0.3770, 0.3770, 0.3770, 0.3770, 0.3770, 0.3770, 0.3770, 0.3770 }") 
    else:
        producer.send_string("{ \"count\": {0, 0.1523, 0.2344, 0.3770, 0.6016, 0.8770, 1.1758, 1.4766, 1.9141, 2.4063, 2.7305, 3.3223, 3.9023, 4.5234, 5.1152, 5.5547 }") 
