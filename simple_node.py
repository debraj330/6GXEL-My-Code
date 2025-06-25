# Terminal 2
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.0.178:5558")
socket.RCVTIMEO = 5000  # timeout in ms

print("[Simple Node] Sending hello...")
try:
    socket.send_json({"hello": "world"})
    reply = socket.recv_json()
    print("[Simple Node] Got reply:", reply)
except zmq.Again:
    print("[Simple Node] ERROR: Timeout waiting for reply")
except Exception as e:
    print("[Simple Node] ERROR:", e)
