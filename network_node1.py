# network_node1.py
import zmq
import time
import random

NODE_ID = "N001"

# Randomly generated initial metrics
METRICS = {
    "SINR": f"{random.uniform(10, 30):.2f} dB",
    "Throughput": f"{random.randint(100, 300)} Mbps",
    "Delay": f"{random.uniform(5, 20):.2f} ms"
}

def register_to_register():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5558")

    print("[Node] Registering with register1.py...")
    socket.send_json({
        "node_id": NODE_ID,
        "metrics": METRICS
    })

    try:
        reply = socket.recv_json()
        if reply.get("status") == "REGISTRATION_SUCCESS":
            print("[Node] Successfully registered.")
        else:
            print("[Node] Registration failed.")
    except zmq.ZMQError as e:
        print(f"[Node] Registration error: {e}")

def listen_for_ai_commands():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5560")

    print("[Node] Ready to receive commands from AI engine...")

    while True:
        command = socket.recv_string()
        print(f"[Node] Received command: {command}")

        if command == "APP1":
            print(f"[APP1 Execution] SINR: {METRICS['SINR']}, Throughput: {METRICS['Throughput']}")
            socket.send_string("APP1 task completed")
        elif command == "APP2":
            print(f"[APP2 Execution] Delay: {METRICS['Delay']}")
            socket.send_string("APP2 task completed")
        else:
            print("[Node] Unknown command received.")
            socket.send_string("Unknown command")

if __name__ == "__main__":
    register_to_register()
    listen_for_ai_commands()
