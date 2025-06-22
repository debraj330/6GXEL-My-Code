from .parse_config import parse_config
from .xapp_setup import check_entropy
import zmq
import json
from . import messages

class RegisterXapp:
    def __init__(self):
        # read configuration file
        self.config = parse_config('./xApp.conf')
        self.socket = "tcp://" + self.config["ip_address"] + ":" + self.config["near_rt_RIC"]

        # check entropy before establishing the connection with the databus
        check_entropy()

        print("Connecting to the RIC Registration****************: ", self.config["ip_address"], self.config["near_rt_RIC"])
        self.databus_ip = ""
        self.send_port = ""
        self.rcv_port = ""

        # connect to the databus pub and sub sockets
        self.connect()

    def connect(self):
        self.context = zmq.Context()
        #  Socket to talk to server
        self.registration_handle = self.context.socket(zmq.REQ)
        self.registration_handle.connect(self.socket)

    def read_msg(self):
        recv_msg =  self.registration_handle.recv()
        recv_msg = json.loads(recv_msg.decode("utf-8"))
        return recv_msg

    def send_msg(self, msg):
        msg = json.dumps(msg).encode("utf-8")
        self.registration_handle.send(msg)
        print("Command sent")

    def register_xapp(self, xApp):
        reg_msg = messages.register_xApp
        reg_msg['node_id'] = xApp.node_id
        self.send_msg(reg_msg)
        print("Registration message sent: ", xApp.node_id)

        reg_response = self.read_msg()
        print(reg_response)
        if reg_response["msg_type"] == "err_msg":
            raise RuntimeError("xApp was not able to register with the near-RT RIC \n Error msg: %s " % reg_response["msg_content"])

        pm_ctrl_req = messages.pm_ctrl_req
        pm_ctrl_req["node_id"] = xApp.node_id
        pm_ctrl_req['e2_node_list'] = xApp.cell_ids
        pm_ctrl_req['list_of_pm'] = xApp.read_measurements
        pm_ctrl_req['list_of_ctrl'] = xApp.send_commands
        self.send_msg(pm_ctrl_req)
        print("PM_CTRL_REQUEST SENT")

        pm_ctrl_response = self.read_msg()
        print(pm_ctrl_response)
        if pm_ctrl_response["msg_type"] == "err_msg":
            raise RuntimeError("xApp was not able to register with the near-RT RIC \n Error msg: %s " % pm_ctrl_response["msg_content"])

        self.databus_ip = pm_ctrl_response["databus_ip"]
        self.send_port = pm_ctrl_response["xApp_send_command_port"]
        self.rcv_port = pm_ctrl_response["xApp_listen_port"]





    # def __del__(self):
    #     self.producer.close()
    #     self.consumer.close()
    #     self.contex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t.term()
