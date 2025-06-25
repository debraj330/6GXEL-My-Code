import zmq
import time
import json

NODE_ID = "node-001"
METRICS = {
    "bandwidth": "100Mbps",
    "memory": "4GB",
    "energy": "80%",
    "cpu_cycles": "2GHz"
}

def register_with_server():
    context = zmq.Context()
    register_socket = context.socket(zmq.REQ)
    register_socket.connect("tcp://192.168.0.178:5558")
    register_socket.RCVTIMEO = 5000  # timeout in ms
    print("[Network Node] Connecting to Register service...")

    print(f"[Network Node] Registering with node ID: {NODE_ID}")
    message = {
        "node_id": NODE_ID,
        "metrics": METRICS
    }
    try:
        register_socket.send_json(message)
        print("[Network Node] Sent registration message. Waiting for reply...")
        response = register_socket.recv_json()
        print(f"[Network Node] Received from register: {response}")
    except zmq.Again:
        print("[Network Node] ERROR: No response from register.py (timeout)")
    except Exception as e:
        print(f"[Network Node] ERROR: {e}")

if __name__ == "__main__":
    register_with_server()
