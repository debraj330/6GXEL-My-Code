# register2.py
import zmq
import threading

registered_nodes = {}
valid_node_id = "N002"

def handle_node_registration():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5565")
    print("[Register2] Waiting for node registration...")

    while True:
        message = socket.recv_json()
        node_id = message.get("node_id")
        if node_id == valid_node_id:
            registered_nodes[node_id] = message.get("metrics")
            print(f"[Register2] Registered node: {node_id} with metrics {registered_nodes[node_id]}")
            socket.send_json({"status": "REGISTRATION_SUCCESS"})
            break
        else:
            socket.send_json({"status": "REGISTRATION_FAILED"})

def handle_ai_registration():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5566")
    print("[Register2] Waiting for AI engine registration...")

    while True:
        msg = socket.recv_json()
        if msg.get("ai_id") == "AI002":
            print(f"[Register2] AI Engine {msg['ai_id']} registered.")
            socket.send_json({"status": "AI_REGISTERED"})
            break
        else:
            socket.send_json({"status": "AI_REGISTRATION_FAILED"})

if __name__ == "__main__":
    threading.Thread(target=handle_node_registration).start()
    threading.Thread(target=handle_ai_registration).start()
