# ------------------------------
# File: network_node1.py
# ------------------------------
import zmq
import time
import random

NODE_ID = "N001"
METRICS = {
    "SINR": f"{random.uniform(10, 30):.2f} dB",
    "Throughput": f"{random.randint(50, 150)} Mbps",
    "Delay": f"{random.uniform(1, 10):.2f} ms"
}

# Step 1: Register to Register service
def register_with_register():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5558")
    
    print("[Node] Connecting to Register...")
    socket.send_json({
        "node_id": NODE_ID,
        "metrics": METRICS
    })

    try:
        reply = socket.recv_json()
        if reply.get("status") == "REGISTRATION_SUCCESS":
            print(f"[Node] Registration successful with metrics: {METRICS}")
        else:
            print("[Node] Registration failed.")
    except zmq.ZMQError as e:
        print(f"[Node] ERROR: {e}")

# Step 2: Wait for instructions on a separate socket
def listen_for_commands():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5560")
    
    while True:
        command = socket.recv_string()
        print(f"[Node] Received command: {command}")
        if command == "APP1":
            print(f"SINR: {METRICS['SINR']}, Throughput: {METRICS['Throughput']}")
            socket.send_string("APP1 task done")
        elif command == "APP2":
            print(f"Delay: {METRICS['Delay']}")
            socket.send_string("APP2 task done")
        else:
            socket.send_string("Unknown command")

if __name__ == "__main__":
    register_with_register()
    listen_for_commands()
