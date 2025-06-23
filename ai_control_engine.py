#PYTHON CODE

# File: ai_control_engine.py

import zmq
import threading
import time
import json
from register_utils.RegisterInterface import RegisterInterface
from register_utils import messages

AIC_ID = 0

class AIControlEngine:
    def __init__(self):
        self.register = RegisterInterface()
        self.running = True

    def handle_ai_app_registration(self, msg):
        print(f"[AIControlEngine] AI App Registration: {msg['node_id']}")
        try:
            self.register.register_ai_app(msg['node_id'])

            # Verify that the requested PMs and CTRLs exist
            missing_pms = [pm for pm in msg['list_of_pm'] if pm not in self.register.get_list_of_pm()]
            missing_ctrls = [ctrl for ctrl in msg['list_of_ctrl'] if ctrl not in self.register.get_list_of_ctrl()]

            if missing_pms or missing_ctrls:
                raise ValueError(f"Missing PMs: {missing_pms}, Missing CTRLS: {missing_ctrls}")

            self.register.register_ai_app_actions(
                msg['node_id'],
                msg['network_node_list'],
                msg['list_of_pm'],
                msg['list_of_ctrl']
            )

            ack = messages.ai_app_access_ack
            ack['node_id'] = AIC_ID
            ack['databus_ip'] = self.register.config['registration_ip_address']
            ack['ai_app_listen_port'] = self.register.config['pub_measurements']
            ack['ai_app_send_command_port'] = self.register.config['recv_commands']
            self.register.send_msg(ack)
        except Exception as e:
            print("[ERROR] AI App Registration Failed:", e)
            err = messages.err
            err['node_id'] = AIC_ID
            err['msg_content'] = str(e)
            self.register.send_msg(err)

    def handle_node_registration(self, msg):
        print(f"[AIControlEngine] Network Node Registration: {msg['node_id']}")
        try:
            self.register.register_network_node(msg['node_id'])
            ack = messages.network_node_registration_ack
            ack['node_id'] = AIC_ID
            self.register.send_msg(ack)
        except Exception as e:
            print("[ERROR] Node Registration Failed:", e)
            err = messages.err
            err['node_id'] = AIC_ID
            err['msg_content'] = str(e)
            self.register.send_msg(err)

    def handle_pm_availability(self, msg):
        print(f"[AIControlEngine] PM Availability from {msg['node_id']}: {msg['available_pms']}")
        try:
            self.register.register_available_pms(msg['node_id'], msg['available_pms'])
            ack = messages.network_node_pm_availability_ack
            ack['node_id'] = AIC_ID
            ack['databus_ip'] = self.register.config['registration_ip_address']
            ack['send_pm_port'] = self.register.config['recv_measurements']
            self.register.send_msg(ack)
        except Exception as e:
            print("[ERROR] PM Availability Error:", e)
            err = messages.err
            err['node_id'] = AIC_ID
            err['msg_content'] = str(e)
            self.register.send_msg(err)

    def handle_alive(self, msg):
        print(f"[AIControlEngine] Alive signal from: {msg['node_id']}")
        try:
            self.register.alive_network_node_update(msg['node_id'])
            ack = messages.network_node_alive_ack
            ack['node_id'] = AIC_ID
            self.register.send_msg(ack)
        except Exception as e:
            print("[ERROR] Alive update failed:", e)
            err = messages.err
            err['node_id'] = AIC_ID
            err['msg_content'] = str(e)
            self.register.send_msg(err)

    def handle_msg(self, msg):
        node_type = msg.get("node_type")
        msg_type = msg.get("msg_type")

        if node_type == "network_node":
            if msg_type == "register":
                self.handle_node_registration(msg)
            elif msg_type == "pm_availability":
                self.handle_pm_availability(msg)
            elif msg_type == "alive":
                self.handle_alive(msg)

        elif node_type == "ai_app":
            if msg_type == "register":
                self.handle_ai_app_registration(msg)

    def start_msg_loop(self):
        while self.running:
            try:
                msg = self.register.read_msg()
                print("[AIControlEngine] Received message:", msg)
                self.handle_msg(msg)
            except Exception as e:
                print("[ERROR] Message handling failed:", e)

    def check_node_status_loop(self):
        while self.running:
            try:
                for node_id in self.register.get_network_nodes():
                    self.register.check_if_network_node_is_alive(node_id)
                time.sleep(2)
            except Exception as e:
                print("[ERROR] Node status check failed:", e)

    def run(self):
        threading.Thread(target=self.start_msg_loop).start()
        threading.Thread(target=self.check_node_status_loop).start()

if __name__ == "__main__":
    engine = AIControlEngine()
    engine.run()

