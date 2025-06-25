import zmq
import threading

registered_nodes = {}
valid_node_id = "node-001"  # Only this node is considered genuine

def handle_node_registration():
    context = zmq.Context()
    node_socket = context.socket(zmq.REP)
    node_socket.bind("tcp://0.0.0.0:5558")
    while True:
        message = node_socket.recv_json()
        node_id = message.get("node_id")
        metrics = message.get("metrics")
        if node_id == valid_node_id:
            registered_nodes[node_id] = metrics
            print(f"[Register] Registered Node: {node_id} with metrics {metrics}")
            node_socket.send_string("REGISTRATION_SUCCESS")
        else:
            print(f"[Register] Invalid node tried to register with ID: {node_id}")
            node_socket.send_string("REGISTRATION_FAILED")

def handle_ai_requests():
    context = zmq.Context()
    ai_socket = context.socket(zmq.REP)
    ai_socket.bind("tcp://0.0.0.0:5559")
    while True:
        message = ai_socket.recv_string()
        if message == "CHECK_NODE":
            if valid_node_id in registered_nodes:
                ai_socket.send_string("NODE_PRESENT")
            else:
                ai_socket.send_string("NO_NODE")

if __name__ == "__main__":
    print("[Register] Register service started...")
    threading.Thread(target=handle_node_registration).start()
    threading.Thread(target=handle_ai_requests).start()
