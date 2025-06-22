import json
import paho.mqtt.client as mqtt

registered_nodes = {}
registered_ai_apps = {}

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload)
    
    if topic == "register/network_node":
        node_id = payload["nodeID"]
        print(f"[Register] Registering node: {node_id}")
        registered_nodes[node_id] = {
            "PMs": payload["PMs"],
            "control_params": payload["control_params"]
        }
        client.publish("register/response", json.dumps({"status": "success", "type": "node"}))

    elif topic == "register/ai_app":
        app_id = payload["appID"]
        node_id = payload["req_nodeID"]
        if node_id not in registered_nodes:
            print(f"[Register] AI {app_id} rejected: Node {node_id} not registered.")
            client.publish("register/response", json.dumps({"status": "fail", "reason": "node_absent", "appID": app_id}))
            return
        
        if app_id.startswith("fake"):
            print(f"[Register] AI {app_id} rejected: Fake AI detected.")
            client.publish("register/response", json.dumps({"status": "fail", "reason": "fake", "appID": app_id}))
            return

        print(f"[Register] AI {app_id} successfully registered.")
        registered_ai_apps[app_id] = {"nodeID": node_id}
        client.publish("register/response", json.dumps({
            "status": "success",
            "type": "ai_app",
            "PMs": registered_nodes[node_id]["PMs"]
        }))

client = mqtt.Client("Register")
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("register/network_node")
client.subscribe("register/ai_app")
print("🧾 Register is running and waiting for registrations...\n")
client.loop_forever()
