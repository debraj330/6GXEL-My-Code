import zmq
import threading

AI_ID = "AI002"

def register_to_register2():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5571")
    print("[AI2] Registering to register2...")

    socket.send_json({"ai_id": AI_ID})
    reply = socket.recv_json()
    print(f"[AI2] Register Response: {reply}")

def listen_from_inter_broker():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.0.178:5573")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    node_socket = context.socket(zmq.REQ)
    node_socket.connect("tcp://192.168.0.178:5572")

    print("[AI2] Listening to inter_ai_broker...")

    while True:
        app_info = socket.recv_string()
        print(f"[AI2] Received app info from inter_ai_broker: {app_info}")
        if app_info == "APP1":
            node_socket.send_string("APP3")
            print(node_socket.recv_string())
            node_socket.send_string("APP4")
            print(node_socket.recv_string())
        elif app_info == "APP2":
            node_socket.send_string("APP5")
            print(node_socket.recv_string())

if __name__ == "__main__":
    register_to_register2()
    listen_from_inter_broker()
