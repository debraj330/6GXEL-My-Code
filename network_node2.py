import zmq
import time
import threading
import random

NODE_ID = "N002"
METRICS = {
    "throughput": "120Mbps",
    "delay": "10ms",
    "CQI": "15",
    "SINR": "25dB"
}

def register_to_register2():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5570")
    print("[Node2] Registering to register2...")

    socket.send_json({
        "node_id": NODE_ID,
        "metrics": METRICS
    })
    reply = socket.recv_json()
    print(f"[Node2] Register Response: {reply}")

def listen_for_commands():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5572")
    print("[Node2] Ready to receive app commands...")

    while True:
        cmd = socket.recv_string()
        if cmd == "APP3":
            def app3():
                while True:
                    print(f"[APP3] Throughput: {METRICS['throughput']}, Delay: {METRICS['delay']}, CQI: {METRICS['CQI']}, SINR: {METRICS['SINR']}")
                    time.sleep(1)
            threading.Thread(target=app3, daemon=True).start()
            socket.send_string("APP3 Started")

        elif cmd == "APP4":
            def app4():
                while True:
                    print("[APP4] Hello 6GXCEL")
                    time.sleep(1)
            threading.Thread(target=app4, daemon=True).start()
            socket.send_string("APP4 Started")

        elif cmd == "APP5":
            def app5():
                while True:
                    print(f"[APP5] Boosted Throughput: 150Mbps, Reduced Delay: 5ms, CQI: 20, SINR: 30dB")
                    time.sleep(1)
            threading.Thread(target=app5, daemon=True).start()
            socket.send_string("APP5 Started")

if __name__ == "__main__":
    register_to_register2()
    listen_for_commands()
