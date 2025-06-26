import zmq
import threading

registered_nodes = {}
valid_node_id = "node-001"  # Only this node is considered genuine

def handle_node_registration():
    context = zmq.Context()
    node_socket = context.socket(zmq.REP)
    node_socket.bind("tcp://192.168.0.178:5558")
    print("[Register] Binding socket to tcp://192.168.0.178:5558")

    while True:
        print("[Register] Waiting for node registration message...")
        message = node_socket.recv_json()
        print(f"[Register] Received: {message}")
        node_id = message.get("node_id")

        if node_id == valid_node_id:
            registered_nodes[node_id] = message.get("metrics")
            print(f"[Register] Registered Node: {node_id} with metrics {registered_nodes[node_id]}")
            node_socket.send_json({"status": "REGISTRATION_SUCCESS"})
            node_socket.close()
            break  # Exit loop after successful registration
        else:
            print(f"[Register] Invalid node ID: {node_id}")
            node_socket.send_json({"status": "REGISTRATION_FAILED"})

def handle_ai_requests():
    context = zmq.Context()
    ai_socket = context.socket(zmq.REP)
    ai_socket.bind("tcp://192.168.0.178:5559")
    print("[Register] Binding socket to tcp://192.168.0.178:5559")

    while True:
        print("[Register] Waiting for AI engine message...")
        message = ai_socket.recv_string()
        print(f"[Register] Received from AI engine: {message}")

        if message == "CHECK_NODE":
            if valid_node_id in registered_nodes:
                ai_socket.send_string("NODE_PRESENT")
            else:
                ai_socket.send_string("NO_NODE")

        elif message == "GET_METRICS":
            if valid_node_id in registered_nodes:
                ai_socket.send_json({
                    "status": "SUCCESS",
                    "metrics": registered_nodes[valid_node_id]
                })
            else:
                ai_socket.send_json({
                    "status": "FAILED",
                    "reason": "No node registered"
                })

        elif message.startswith("CMD:"):
            command = message.split("CMD:")[1]
            print(f"[Register] Received Control Command: {command}")
            # You can implement command forwarding logic here if needed
            ai_socket.send_string(f"Command '{command}' executed.")

        else:
            print("[Register] Unknown message received.")
            ai_socket.send_string("UNKNOWN_COMMAND")

if __name__ == "__main__":
    print("[Register] Register service started...")

    # Step 1: Wait for a valid node registration (blocking)
    handle_node_registration()

    # Step 2: Start handling AI engine messages
    handle_ai_requests()
