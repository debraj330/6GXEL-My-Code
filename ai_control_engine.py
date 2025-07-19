# ------------------------------
# File: ai_control_engine1.py
# ------------------------------
import zmq

AI_ID = "AI001"

def send_command(app_command):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5559")
    
    socket.send_json({
        "ai_id": AI_ID,
        "command": app_command
    })

    try:
        reply = socket.recv_json()
        print(f"[AI Engine] Register response: {reply}")
    except zmq.ZMQError as e:
        print(f"[AI Engine] ERROR: {e}")

if __name__ == "__main__":
    print("[AI Engine] Running...")
    while True:
        cmd = input("Enter command for App1 or App2 (APP1/APP2): ").strip()
        if cmd in ["APP1", "APP2"]:
            send_command(cmd)
        else:
            print("Invalid input. Try again.")
