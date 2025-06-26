import zmq
import time
import json

context = zmq.Context()
register_socket = context.socket(zmq.REQ)
register_socket.connect("tcp://192.168.0.178:5559")

def wait_for_node():
    while True:
        user_input = input("Do you start the network_node and your network_node is successfully registered to the register.py? (Yes/No): ")
        if user_input.lower() == "yes":
            register_socket.send_string("CHECK_NODE")
            reply = register_socket.recv_string()
            if reply == "NODE_PRESENT":
                print("[AI Engine] Network Node is registered. Proceeding with interaction...\n")
                return
            else:
                print("[AI Engine] No valid network_node present. Waiting again.")
        else:
            print("[AI Engine] Waiting for valid network node...")

def app1_fetch_metrics():
    register_socket.send_string("GET_METRICS")
    response = register_socket.recv_json()
    if response["status"] == "SUCCESS":
        print("[App1] Received Metrics:", response["metrics"])
    else:
        print("[App1] Failed to fetch metrics:", response.get("reason", "Unknown error"))

def app2_send_command():
    cmd = input("[App2] Enter control command to send: ")
    register_socket.send_string(f"CMD:{cmd}")
    response = register_socket.recv_string()
    print(f"[App2] Register response: {response}")

def main_menu():
    while True:
        print("\n--- AI Engine App Menu ---")
        print("1. App1: Fetch Metrics")
        print("2. App2: Send Control Command")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            app1_fetch_metrics()
        elif choice == '2':
            app2_send_command()
        elif choice == '3':
            print("Exiting AI Engine.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    wait_for_node()
    main_menu()
