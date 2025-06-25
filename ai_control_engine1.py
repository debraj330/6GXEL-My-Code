import zmq
import threading
import time
import uuid
import json
import configparser

# Config
def read_config(path="node_msg_broker.conf"):
    parser = configparser.ConfigParser()
    parser.read(path)
    cfg = parser["broker"]
    return {
        "ip_address": cfg["ip_address"],
        "recv_measurements": cfg["recv_measurements"],
        "pub_measurements": cfg["pub_measurements"],
        "recv_commands": cfg["recv_commands"],
        "pub_commands": cfg["pub_commands"],
        "registration_ip_address": cfg["registration_ip_address"]
    }

# Constants
AIC_ID = f"ai_engine_{uuid.uuid4()}"[:12]

class AIControlEngine:
    def __init__(self):
        self.config = read_config()
        self.context = zmq.Context()
        self.running = True

        self.register_push_socket = self.context.socket(zmq.PUSH)
        self.register_push_socket.connect(f"tcp://{self.config['ip_address']}:{self.config['recv_measurements']}")

        self.register_sub_socket = self.context.socket(zmq.SUB)
        self.register_sub_socket.connect(f"tcp://{self.config['ip_address']}:{self.config['pub_commands']}")
        self.register_sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        print(f"[AIControlEngine] Initialized with ID: {AIC_ID}")

    def register_with_register(self):
        print("[AIControlEngine] Sending registration to register...")
        msg = {
            "node_type": "ai_app",
            "msg_type": "register",
            "node_id": AIC_ID
        }
        self.register_push_socket.send_json(msg)

    def request_pm_ctrl_access(self, target_node_id, pms, ctrls):
        print("[AIControlEngine] Requesting PM/CTRL access for AI App...")
        msg = {
            "node_type": "ai_app",
            "msg_type": "pm_ctrl_req",
            "node_id": AIC_ID,
            "network_node_list": [target_node_id],
            "list_of_pm": pms,
            "list_of_ctrl": ctrls
        }
        self.register_push_socket.send_json(msg)

    def listen_for_messages(self):
        while self.running:
            try:
                msg = self.register_sub_socket.recv_json()
                print("[AIControlEngine] Message from register or node:", msg)

                if msg.get("msg_type") == "ai_app_registration_ack":
                    print("[AIControlEngine] Registered with Register successfully.")
                    # After registration, ask for access
                    if msg["network_node_list"]:
                        node_id = msg["network_node_list"][0]
                        pms = msg["list_of_pm"]
                        ctrls = msg["list_of_ctrl"]
                        self.request_pm_ctrl_access(node_id, pms, ctrls)

                elif msg.get("msg_type") == "ai_app_access_ack":
                    print(f"[AIControlEngine] Access granted for PM/CTRL on {msg['databus_ip']}")
                    # You may now connect to PUB/SUB for live PMs and send commands to PULL socket

                elif msg.get("msg_type") == "err":
                    print("[AIControlEngine] ERROR from Register:", msg["msg_content"])

            except Exception as e:
                print("[AIControlEngine] Error receiving message:", e)

    def run(self):
        self.register_with_register()
        threading.Thread(target=self.listen_for_messages).start()


if __name__ == "__main__":
    engine = AIControlEngine()
    engine.run()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[AIControlEngine] Shutting down...")
