# ai_control_engine2.py
import zmq
import threading
import time

AI_ID = "AI002"

def register_with_register2():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5566")

    print("[AI2] Registering with Register2...")
    socket.send_json({"ai_id": AI_ID})
    reply = socket.recv_json()
    if reply.get("status") == "AI_REGISTERED":
        print("[AI2] Successfully registered.")
    else:
        print("[AI2] Registration failed.")

def listen_to_broker():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.0.178:5568")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        msg = socket.recv_string()
        print(f"[AI2] Received from broker: {msg}")
        if msg == "APP1":
            run_app3_and_app4()
        else:
            run_app5()

def run_app3_and_app4():
    print("[AI2] Running APP3 and APP4...")
    send_command_to_node("APP3")
    send_command_to_node("APP4")

def run_app5():
    print("[AI2] Running APP5...")
    send_command_to_node("APP5")

def send_command_to_node(command):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5567")
    socket.send_string(command)
    reply = socket.recv_string()
    print(f"[AI2] Node replied: {reply}")

if __name__ == "__main__":
    register_with_register2()
    listen_to_broker()
