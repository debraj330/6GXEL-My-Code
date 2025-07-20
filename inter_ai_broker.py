# inter_ai_broker.py
import zmq

context = zmq.Context()

# SUB socket to listen to register1.py
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://192.168.0.178:5562")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# PUB socket to forward to ai_control_engine2.py
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://192.168.0.178:5568")

print("[Broker] Forwarding messages from register1 to AI2...")

while True:
    msg = sub_socket.recv_string()
    print(f"[Broker] Received: {msg}")
    pub_socket.send_string(msg)
