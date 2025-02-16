import subprocess
import time

def run_client(client_id, server_ip, port, message=None):
    command = ["python", "client.py", "-client_id", str(client_id), "-server_ip", server_ip, "-port", str(port)]
    if message:
        command.extend(["-message", message])
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def log_output(process, name):
    """Logs output from a client process"""
    stdout, stderr = process.communicate()
    if stdout:
        print(f"[{name} Output]:\n{stdout}")
    if stderr:
        print(f"[{name} Error]:\n{stderr}")

if __name__ == '__main__':
    print("🔹 Starting test scenario...")

    # To start the server
    server_process = subprocess.Popen(["python3", "server.py", "-client_ids", "1,2,3", "-port", "50051"])
    time.sleep(2)  # Give server time to initialize

    print("\n✅ Alice is online and sending a message...\n")
    alice = run_client(1, "localhost", 50051, "Hello everyone!")
    log_output(alice, "Alice")

    time.sleep(5)  # Simulating Bob and Chad joining late

    print("\n✅ Bob and Chad are coming online to receive messages...\n")
    bob = run_client(2, "localhost", 50051)
    chad = run_client(3, "localhost", 50051)
    
    log_output(bob, "Bob")
    log_output(chad, "Chad")

    time.sleep(2)

    print("\n✅ Bob is sending a message to the group...\n")
    bob_send = run_client(2, "localhost", 50051, "Hi Alice and Chad!")
    log_output(bob_send, "Bob (Sent Message)")

    time.sleep(2)

    print("\n✅ Alice and Chad checking messages...\n")
    alice_receive = run_client(1, "localhost", 50051)
    chad_receive = run_client(3, "localhost", 50051)

    log_output(alice_receive, "Alice (Received Messages)")
    log_output(chad_receive, "Chad (Received Messages)")

    time.sleep(2)

    print("\n✅ Doug (unauthorized) is joining the server...\n")
    doug = run_client(4, "localhost", 50051)  # Doug is not in the group
    log_output(doug, "Doug")

    time.sleep(2)

    print("\n🔴 Stopping all processes...\n")
    server_process.terminate()

    print("\n✅ Test scenario completed successfully! ")
