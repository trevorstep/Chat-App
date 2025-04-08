import socket
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
HOST = "127.0.0.1"  # or use os.getenv("SERVER_IP")
PORT = int(os.getenv("PORT", "5000"))

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        while True:
            message = input("Enter command (time, hello, or quit): ").strip()
            if message.lower() == "quit":
                break

            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            print("Response:", response)

if __name__ == "__main__":
    run_client()
