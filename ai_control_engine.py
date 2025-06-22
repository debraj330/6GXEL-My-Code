#PYTHON CODE

import json
import time
import paho.mqtt.client as mqtt

app_id = "AI_App_1"  # Change to "fake_AI_1" to simulate fake case
requested_node = "Node123"

def on_message(client, userdata, msg):
    response = json.loads(msg.payload)
    
    if response.get("status") == "fail":
        reason = response.get("reason")
        print(f"❌ Registration failed: {reason}")
        exit()
    
    if response.get("type") == "ai_app":
        print(f"✅ AI {app_id} registered. PMs received: {response['PMs']}")
        # Control logic (for now, just printing)
        print("🛠️ Controlling network node based on PMs...")
        # Simulate sending control
        print(f"📤 Control command: Adjust MCS to 18")

client = mqtt.Client("AI_Engine")
client.connect("localhost", 1883)
client.subscribe("register/response")
client.on_message = on_message
client.loop_start()

print("🤖 Sending AI registration request...\n")
register_msg = {
    "appID": app_id,
    "req_nodeID": requested_node
}
client.publish("register/ai_app", json.dumps(register_msg))
time.sleep(3)
client.loop_stop()
