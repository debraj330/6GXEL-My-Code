from .parse_config import parse_config
from .setup import check_entropy
import zmq
import json
import redis


class RegisterInterface:
    # registered_cells = []
    # registered_cells_pm = {}
    # registered_cells_ctrl = {}
    # registered_ai_apps = []
    # registered_ai_apps_info = {}


    def __init__(self):
        # read configuration file
        self.config = parse_config('./register.conf')
        self.sub_socket = "tcp://" + self.config["ip_address"] + ":" + self.config["register_sub"]
        self.pub_socket = "tcp://" + self.config["ip_address"] + ":" + self.config["register_pub"]

        # check entropy before establishing the connection with the databus
        check_entropy()

       # Connect to the Redis server
        self.redis_db = redis.Redis(host='redis', port=6379, decode_responses=True)
        # Create namespaces for different tables
        self.network_node_namespace = 'network_nodes'
        self.network_node_list = 'network_node_list'
        self.network_node_pm_list = 'network_node_pm_list'
        self.network_node_ctrl_list = 'network_node_ctrl_list'
        self.ai_app_namespace = 'ai_apps'
        self.ai_apps_list = 'ai_apps_list'
        self.ai_apps_info_list = 'ai_apps_info_list'

        print("Connecting to the databus****************")
        # connect to the databus pub and sub sockets
        self.connect()

    def connect(self):
        self.context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to the databus")
        # self.consumer = self.context.socket(zmq.SUB)
        self.consumer = self.context.socket(zmq.REP)
        self.consumer.bind(self.sub_socket)
        self.consumer.setsockopt(zmq.LINGER, 0)
        # self.consumer.setsockopt(zmq.SUBSCRIBE,b"")
        self.consumer.setsockopt(zmq.CONFLATE, 1)

        # self.producer = self.context.socket(zmq.PUSH)
        # self.producer.connect(self.pub_socket)

    def get_network_nodes(self):
        registered_cells = list(self.redis_db.smembers(f'{self.network_node_namespace}:{self.network_node_list}'))
        return registered_cells
    #     return self.registered_cells

    def get_list_of_pm(self):
        registered_cells_pm = {}
        namespace_keys = list(self.redis_db.keys(f'{self.network_node_namespace}:{self.network_node_pm_list}*'))
        for network_node_n in namespace_keys:
            registered_cells_pm[int(network_node_n[-1])] = list(self.redis_db.smembers(network_node_n))
        return registered_cells_pm

        # if not self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_pm_list}:{network_node_n}') or not self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_pm_list}:{network_node_n}', int(network_node_n)):
        # my_set = r.smembers('my-set')
        # return self.registered_cells_pm

    def get_list_of_ctrl(self):
        registered_ctrl = {}
        namespace_keys = list(self.redis_db.keys(f'{self.network_node_namespace}:{self.network_node_ctrl_list}*'))
        for network_node_n in namespace_keys:
            registered_ctrl[int(network_node_n[-1])] = list(self.redis_db.smembers(network_node_n))
        return registered_ctrl
    #     return self.registered_cells_ctrl

    def read_msg(self):
        print("(******tying to receive******)")
        recv_msg = self.consumer.recv()
        print(recv_msg.decode("utf-8"))
        return json.loads(recv_msg.decode("utf-8"))
        # return self.consumer.recv_json()
        # return json.loads(self.consumer.recv().decode("utf-8"))
        # return self.consumer.recv().decode("utf-8")

    def send_msg(self, msg):
        msg = json.dumps(msg).encode("utf-8")
        self.consumer.send(msg)
        print("Command sent")

    def register_ai_app(self, node_id):
        if self.redis_db.exists(f'{self.ai_app_namespace}:{self.ai_apps_list}'):
            if self.redis_db.sismember(f'{self.ai_app_namespace}:{self.ai_apps_list}', int(node_id)):
                raise Exception("ai_app already registered")
        # if int(node_id) in self.registered_ai_apps:
            # raise Exception("ai_app already registered")
        # self.registered_ai_apps.append(int(node_id))
        self.redis_db.sadd(f'{self.ai_app_namespace}:{self.ai_apps_list}', int(node_id))
        # print(self.redis_db.smembers(f'{self.ai_app_namespace}:{self.ai_apps_list}'))



    def register_ai_app_actions(self, node_id, network_node_list, list_of_pm, list_of_ctrl):
        if not self.redis_db.exists(f'{self.ai_app_namespace}:{self.ai_apps_list}') or not self.redis_db.sismember(f'{self.ai_app_namespace}:{self.ai_apps_list}', int(node_id)):
            raise Exception("ai_app not registered")
        # if node_id not in self.registered_ai_apps:
        #     raise Exception("ai_app not registered")

        for network_node_n in network_node_list:
            # if network_node_n not in self.registered_cells:
            if not self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_list}') or not self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_list}', int(network_node_n)):
                raise Exception("E2 node " + str(network_node_n) + " not registered with the near-RT RIC!")

        for pm in list_of_pm:
            for network_node_n in network_node_list:
                # if pm not in self.registered_cells_pm[network_node_n]:
                if not self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_pm_list}:{network_node_n}') or not self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_pm_list}:{network_node_n}', pm):
                    raise Exception("The requested PM: " + pm + " is not available from node: " + str(network_node_n))

        for ctrl in list_of_ctrl:
            for network_node_n in network_node_list:
                # if ctrl not in self.registered_cells_ctrl[network_node_n]:
                if not self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_ctrl_list}:{network_node_n}') or not self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_ctrl_list}:{network_node_n}', ctrl):
                    raise Exception("The requested CTRL handle: " + ctrl + " is not available for node: " + str(network_node_n))

        # self.registered_ai_apps_info[node_id] = {'network_nodes': network_node_list,'pm': list_of_pm, 'ctrl': list_of_ctrl}
        ai_app_info = {'network_nodes': network_node_list,'pm': list_of_pm, 'ctrl': list_of_ctrl}
        self.redis_db.sadd(f'{self.ai_app_namespace}:{self.ai_apps_info_list}:{int(node_id)}', *ai_app_info)


    def register_network_node(self, node_id):
        if self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_list}'):
            if self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_list}', int(node_id)):
                raise Exception("E2 Node already registered")
        self.redis_db.sadd(f'{self.network_node_namespace}:{self.network_node_list}', int(node_id))
        self.redis_db.set(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}', int(9))
        # print(self.redis_db.smembers(f'{self.ai_app_namespace}:{self.ai_apps_list}'))
        # if int(node_id) in self.registered_cells:
        #     raise Exception("E2 Node already registered")
        # self.registered_cells.append(int(node_id))

    def register_available_pms(self, node_id, available_pms):
        if not self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_list}') or not self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_list}', int(node_id)):
            raise Exception("E2 node not registered")
        # if int(node_id) not in self.registered_cells:
        #     raise Exception("E2 node not registered")
        self.redis_db.sadd(f'{self.network_node_namespace}:{self.network_node_pm_list}:{int(node_id)}', *available_pms)

        # self.registered_cells_pm[int(node_id)] = available_pms

    def send_command(self, msg):
        self.consumer.send(msg)
        # self.consumer.send_json(msg)
        # self.producer.send_string(command)
        print("Command sent")


    def alive_network_node_update(self, node_id):
        if self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}'):
            # print(str(self.redis_db.get(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}')))
            alive_value = int(self.redis_db.get(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}'))
            alive_value = 3
            self.redis_db.set(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}', alive_value)
            # if self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_list}', int(node_id)):
            #     raise Exception("E2 Node already registered")
        else:
            raise Exception("E2 Node was not registered")

    def check_if_network_node_is_alive(self, node_id):
        # print("Checking if e2 ", node_id, "is alive\n")
        if self.redis_db.exists(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}'):
            # print(str(self.redis_db.get(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}')))
            alive_value = int(self.redis_db.get(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}'))
            alive_value -= 1
            if alive_value < 0:
                self.redis_db.delete(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}')
                self.redis_db.srem(f'{self.network_node_namespace}:{self.network_node_list}', int(node_id))
                raise Exception("E2 node is not available! UNREGISTERING: ", str(node_id))
            else:
                self.redis_db.set(f'{self.network_node_namespace}:{self.network_node_list}:{str(int(node_id))}', alive_value)
            # if self.redis_db.sismember(f'{self.network_node_namespace}:{self.network_node_list}', int(node_id)):
            #     raise Exception("E2 Node already registered")
        else:
            raise Exception("E2 node: ", str(node_id), "is not registered!")


    # def __del__(self):
    #     self.producer.close()
    #     self.consumer.close()
    #     self.contex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t.term()
