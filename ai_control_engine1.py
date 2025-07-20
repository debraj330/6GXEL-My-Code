# ai_control_engine1.py
import zmq
import time

AI_ID = "AI001"

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
        if app in ["APP1", "APP2"]:
            socket.send_string(app)
            reply = socket.recv_string()
            print(f"[AI] Node replied: {reply}")
        else:
            print("[AI] Invalid APP name. Try again.")

if __name__ == "__main__":
    if register_to_register():
        send_command_to_node()
