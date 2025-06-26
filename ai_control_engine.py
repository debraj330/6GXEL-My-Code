import zmq

# Setup
context = zmq.Context()
register_socket = context.socket(zmq.REQ)
register_socket.connect("tcp://192.168.0.178:5559")

def wait_for_node():
    while True:
        user_input = input("Do you start the network_node and your network_node is successfully registered to the register.py? (Yes/No): ")
        if user_input.lower() == "yes":
            register_socket.send_string("CHECK_NODE")
            reply = register_socket.recv_string()
            if reply == "NODE_PRESENT":
                print("[AI Engine] Network Node is registered. Proceeding with interaction...")
                break
            else:
                print("[AI Engine] No valid network_node present. Waiting again.")
        else:
            print("[AI Engine] Waiting for valid network node...")

def send_messages_to_register():
    while True:
        msg = input("Enter Your Message: ")
        if msg.lower() in ["exit", "quit"]:
            print("[AI Engine] Exiting...")
            break
        register_socket.send_string(msg)
        reply = register_socket.recv_string()
        print(f"[AI Engine] Received from register: {reply}")

if __name__ == "__main__":
    wait_for_node()
    send_messages_to_register()
