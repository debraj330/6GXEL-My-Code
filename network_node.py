import json
import paho.mqtt.client as mqtt
import time

node_info = {
    "nodeID": "Node123",
    "PMs": {"CQI": 9, "MCS": 15},
    "control_params": {"freq": "3.5GHz", "bandwidth": "20MHz"}
}

client = mqtt.Client("Network_Node")
client.connect("localhost", 1883)
client.loop_start()

print("📡 Sending network node registration...\n")
client.publish("register/network_node", json.dumps(node_info))
time.sleep(1)
client.loop_stop()
