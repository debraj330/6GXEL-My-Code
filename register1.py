import zmq
import threading

registered_node = {}
valid_node_id = "N001"
valid_ai_id = "AI001"

def handle_node_registration():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5558")
    print("[Register1] Listening for Network Node on port 5558")

    while True:
        msg = socket.recv_json()
        node_id = msg.get("node_id")
        metrics = msg.get("metrics")

        if node_id == valid_node_id:
            registered_node[node_id] = metrics
            print(f"[Register1] Registered Node: {node_id}, Metrics: {metrics}")
            socket.send_json({"status": "NODE_REGISTRATION_SUCCESS"})
            break  # Move to AI registration only after successful node reg
        else:
            print(f"[Register1] Invalid node ID: {node_id}")
            socket.send_json({"status": "NODE_REGISTRATION_FAILED"})

def handle_ai_registration_and_command():
    context = zmq.Context()
    ai_socket = context.socket(zmq.REP)
    ai_socket.bind("tcp://192.168.0.178:5561")
    print("[Register1] Listening for AI Control Engine on port 5561")

    pub_socket = context.socket(zmq.PUB)
    pub_socket.connect("tcp://192.168.0.178:5563")  # inter_ai_broker.py listens here
    print("[Register1] Connected to inter_ai_broker PUB port 5563")

    while True:
        message = ai_socket.recv_json()
        ai_id = message.get("ai_id")

        if ai_id == valid_ai_id and valid_node_id in registered_node:
            print(f"[Register1] Valid AI ID: {ai_id} registered")
            ai_socket.send_json({"status": "AI_REGISTRATION_SUCCESS"})

            app_choice = input("[Register1] Enter APP to instruct (APP1/APP2): ").strip().upper()

            if app_choice == "APP1":
                pub_socket.send_string("APP1")
                print("[Register1] Sent APP1 instruction via inter_ai_broker")
            else:
                pub_socket.send_string("APP2")
                print("[Register1] Sent APP2 instruction via inter_ai_broker")
        else:
            ai_socket.send_json({"status": "AI_REGISTRATION_FAILED"})
            print("[Register1] Invalid AI ID or no node registered.")

if __name__ == "__main__":
    print("[Register1] Service started...")
    threading.Thread(target=handle_node_registration).start()
    threading.Thread(target=handle_ai_registration_and_command).start()
