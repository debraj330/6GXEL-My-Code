# ------------------------------
# File: ai_control_engine1.py
# ------------------------------
import zmq

AI_ID = "AI001"

def register_ai():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.178:5559")

    # Step 1: Send only registration
    socket.send_json({
        "ai_id": AI_ID
    })

    try:
        reply = socket.recv_json()
        print(f"[AI Engine] Register response: {reply}")
        if reply.get("status") == "AI_REGISTRATION_SUCCESS":
            return True
    except zmq.ZMQError as e:
        print(f"[AI Engine] ERROR: {e}")

    return False

if __name__ == "__main__":
    print("[AI Engine] Running...")

    if register_ai():
        print("[AI Engine] Registered. Waiting for further instructions in broker...")
    else:
        print("[AI Engine] Registration failed.")
