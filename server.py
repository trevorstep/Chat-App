import socket
import threading
import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
HOST = os.getenv("SERVER_IP", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"Received from {addr}: {data}")

            if data.lower() == "time":
                response = f"Server time: {datetime.now()}"
            elif data.lower() == "hello":
                response = "Hello, client!"
            else:
                response = "Unknown command"

            conn.sendall(response.encode())
    finally:
        print(f"Disconnected: {addr}")
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
