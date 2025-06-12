## PYTHON CODE

import time
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPICS = ["Hello 6GXCEL", ...., "topic/3"]  # AI apps publish to various topics

client = mqtt.Client("AI_Engine_Publisher")
client.connect(BROKER, 1883)

msg_id = 0
while True:
    for topic in TOPICS:
        payload = {
            "app": topic,
            "msg_id": msg_id,
            "timestamp": time.time(),
            "decision": f"set_param_{msg_id % 5}"
        }
        client.publish(topic, json.dumps(payload))
        print(f"[AI_PUB] -> {topic}: {payload}")
        msg_id += 1
    time.sleep(2)
