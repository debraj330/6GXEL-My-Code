import zmq
import threading

registered_nodes = {}
valid_node_id = "N002"
registered_ai = {}

def handle_node_registration():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5570")
    print("[Register2] Waiting for Network Node...")

    while True:
        message = socket.recv_json()
        node_id = message.get("node_id")
        metrics = message.get("metrics")
        if node_id == valid_node_id:
            registered_nodes[node_id] = metrics
            print(f"[Register2] Registered node {node_id} with metrics {metrics}")
            socket.send_json({"status": "NODE_REGISTERED"})
            break
        else:
            socket.send_json({"status": "INVALID_NODE"})

def handle_ai_registration():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5571")
    print("[Register2] Waiting for AI engine...")

    while True:
        message = socket.recv_json()
        ai_id = message.get("ai_id")
        if ai_id == "AI002":
            registered_ai[ai_id] = True
            print(f"[Register2] AI Engine {ai_id} registered")
            socket.send_json({"status": "AI_REGISTERED"})
            break
        else:
            socket.send_json({"status": "INVALID_AI"})

if __name__ == "__main__":
    threading.Thread(target=handle_node_registration).start()
    threading.Thread(target=handle_ai_registration).start()
