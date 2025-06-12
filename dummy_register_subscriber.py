import json
import paho.mqtt.client as mqtt

TOPIC = "topic/1"  # can be topic/2, etc.

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print(f"[SUB] Received from {msg.topic}: {payload}")

client = mqtt.Client(f"Dummy_Subscriber_{TOPIC}")
client.connect("localhost", 1883)
client.subscribe(TOPIC)
client.on_message = on_message
client.loop_forever()
