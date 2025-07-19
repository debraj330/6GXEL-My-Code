import zmq
import threading

registered_nodes = {}
registered_ai_engines = {}

valid_node_id = "N001"
valid_ai_id = "AI001"

# Handle node registration
def handle_node_registration():
    context = zmq.Context()
    node_socket = context.socket(zmq.REP)
    node_socket.bind("tcp://192.168.0.178:5558")
    print("[Register] Waiting for node registration on port 5558...")

    while True:
        message = node_socket.recv_json()
        node_id = message.get("node_id")
        if node_id == valid_node_id:
            registered_nodes[node_id] = message.get("metrics")
            print(f"[Register] Registered node: {node_id} with metrics: {registered_nodes[node_id]}")
            node_socket.send_json({"status": "REGISTRATION_SUCCESS"})
        else:
            node_socket.send_json({"status": "REGISTRATION_FAILED"})

# Handle AI registration and command routing
def handle_ai_engine():
    context = zmq.Context()
    ai_socket = context.socket(zmq.REP)
    ai_socket.bind("tcp://192.168.0.178:5559")
    print("[Register] Waiting for AI engine on port 5559...")

    while True:
        message = ai_socket.recv_json()
        ai_id = message.get("ai_id")
        cmd = message.get("command")

        if ai_id == valid_ai_id:
            registered_ai_engines[ai_id] = True
            print(f"[Register] Received command from {ai_id}: {cmd}")
            # Forward command to node
            forward_command_to_node(cmd)
            ai_socket.send_json({"status": "COMMAND_SENT"})
        else:
            ai_socket.send_json({"status": "INVALID_AI_ID"})

# Forward command to node

def forward_command_to_node(command):
    context = zmq.Context()
    node_cmd_socket = context.socket(zmq.REQ)
    node_cmd_socket.connect("tcp://192.168.0.178:5560")  # Node command port
    node_cmd_socket.send_string(command)
    ack = node_cmd_socket.recv_string()
    print(f"[Register] Node replied: {ack}")

if __name__ == "__main__":
    threading.Thread(target=handle_node_registration).start()
    threading.Thread(target=handle_ai_engine).start()
