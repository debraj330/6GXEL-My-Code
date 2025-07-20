# ai_control_engine1.py
import zmq
import time

AI_ID = "AI001"

# Setup PUB socket to notify broker (inter_ai_broker.py)
context_pub = zmq.Context()
pub_socket = context_pub.socket(zmq.PUB)
pub_socket.bind("tcp://192.168.0.178:5562")  # <-- Added line

def register_to_register():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5559")

    print("[AI] Registering to register...")
    socket.send_json({"ai_id": AI_ID})

    reply = socket.recv_json()
    if reply.get("status") == "AI_REGISTRATION_SUCCESS":
        print("[AI] Registration successful. Node metrics received:")
        print(reply.get("node_metrics"))
        return True
    else:
        print("[AI] Registration failed.")
        return False

def send_command_to_node():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5560")

    while True:
        app = input("Enter APP name to run (APP1/APP2): ").strip()
        if app == "APP1":
            socket.send_string(app)
            reply = socket.recv_string()
            print(f"[AI] Node replied: {reply}")
            pub_socket.send_string("APP1")
        elif app == "APP2":
            socket.send_string(app)
            reply = socket.recv_string()
            print(f"[AI] Node replied: {reply}")
            pub_socket.send_string("APP2")
        else:
            print("[AI] Invalid APP name. Try again.")

if __name__ == "__main__":
    if register_to_register():
        send_command_to_node()
