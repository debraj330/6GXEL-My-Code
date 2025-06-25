import zmq
import time

# Dummy network node details
node_id = "node-001"
performance_metrics = {
    "bandwidth": "100Mbps",
    "memory": "2GB",
    "energy": "90%",
    "cpu": "2.4GHz"
}

# Setup
context = zmq.Context()
register_socket = context.socket(zmq.REQ)
register_socket.connect("tcp://192.168.56.1:5558")

def register_node():
    print("[Network Node] Registering with node ID:", node_id)
    register_socket.send_json({
        "node_id": node_id,
        "metrics": performance_metrics
    })
    reply = register_socket.recv_string()
    if reply == "REGISTRATION_SUCCESS":
        print("[Network Node] Registration successful.")
    else:
        print("[Network Node] Registration failed.")

if __name__ == "__main__":
    register_node()
