# network_node2.py
import zmq
import time
import random

NODE_ID = "N002"
METRICS = {
    "Throughput": f"{random.randint(80, 120)} Mbps",
    "Delay": f"{random.uniform(2, 6):.2f} ms",
    "CQI": f"{random.randint(1, 15)}",
    "SINR": f"{random.uniform(5, 25):.2f} dB"
}

def register_with_register2():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5565")

    print("[Node2] Registering with Register2...")
    socket.send_json({
        "node_id": NODE_ID,
        "metrics": METRICS
    })

    reply = socket.recv_json()
    if reply.get("status") == "REGISTRATION_SUCCESS":
        print("[Node2] Successfully registered.")
    else:
        print("[Node2] Registration failed.")

def listen_for_commands():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.0.178:5567")
    print("[Node2] Listening for APP commands...")

    while True:
        command = socket.recv_string()
        if command == "APP3":
            for _ in range(5):
                print(f"[APP3] Throughput: {METRICS['Throughput']}, Delay: {METRICS['Delay']}, CQI: {METRICS['CQI']}, SINR: {METRICS['SINR']}")
                time.sleep(1)
            socket.send_string("APP3 completed")
        elif command == "APP4":
            for _ in range(5):
                print("[APP4] Hello 6GXCEL")
                time.sleep(1)
            socket.send_string("APP4 completed")
        elif command == "APP5":
            print("[APP5] Printing modified metrics:")
            for _ in range(5):
                print(f"[APP5] ↑Throughput: {int(METRICS['Throughput'].split()[0]) + 10} Mbps, ↓Delay: {float(METRICS['Delay'].split()[0]) - 1:.2f} ms, ↑CQI: {int(METRICS['CQI']) + 1}, ↑SINR: {float(METRICS['SINR'].split()[0]) + 2:.2f} dB")
                time.sleep(1)
            socket.send_string("APP5 completed")
        else:
            socket.send_string("Unknown command")

if __name__ == "__main__":
    register_with_register2()
    listen_for_commands()
