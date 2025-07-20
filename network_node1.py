# network_node1.py
import zmq
import time
import random

NODE_ID = "N001"
METRICS = {
    "SINR": f"{random.uniform(10, 30):.2f} dB",
    "Throughput": f"{random.randint(100, 300)} Mbps",
    "Delay": f"{random.uniform(5, 20):.2f} ms"
}

def register_to_register():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5558")

    print("[Node] Registering to register...")
    socket.send_json({
        "node_id": NODE_ID,
        "metrics": METRICS
    })

    try:
        reply = socket.recv_json()
        if reply.get("status") == "REGISTRATION_SUCCESS":
            print("[Node] Registration successful.")
        else:
            print("[Node] Registration failed.")
    except zmq.ZMQError as e:
        print(f"[Node] Error: {e}")

def listen_for_commands():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5560")

    print("[Node] Listening for commands...")
    while True:
        cmd = socket.recv_string()
        if cmd == "APP1":
            print(f"[Node] APP1 → SINR: {METRICS['SINR']}, Throughput: {METRICS['Throughput']}")
            socket.send_string("APP1 processed")
        elif cmd == "APP2":
            print(f"[Node] APP2 → Delay: {METRICS['Delay']}")
            socket.send_string("APP2 processed")
        else:
            socket.send_string("Unknown command")

if __name__ == "__main__":
    register_to_register()
    listen_for_commands()
