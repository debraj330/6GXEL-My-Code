import zmq

def start_broker():
    context = zmq.Context()
    receiver = context.socket(zmq.SUB)
    receiver.connect("tcp://192.168.0.178:5563")  # Register1's PUB socket
    receiver.setsockopt_string(zmq.SUBSCRIBE, "")

    sender = context.socket(zmq.PUB)
    sender.bind("tcp://192.168.0.178:5573")  # Broadcast to AI2
    print("[InterBroker] Listening for APP messages from register1.py...")

    while True:
        app_msg = receiver.recv_string()
        print(f"[InterBroker] Forwarding: {app_msg}")
        sender.send_string(app_msg)

if __name__ == "__main__":
    start_broker()
