# Terminal 3
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:5558")
print("[Simple Register] Waiting for message...")
while True:
    try:
        msg = socket.recv_json()
        print("[Simple Register] Got:", msg)
        socket.send_json({"status": "OK"})
    except Exception as e:
        print("[Simple Register] Error:", e)
