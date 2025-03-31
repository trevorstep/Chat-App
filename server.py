import socket
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", "0.0.0.0")
PORT = int(os.getenv("PORT", 12345))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(5)

print(f"Server listening on {SERVER_IP}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")
    
    message = client_socket.recv(1024).decode()
    print(f"Client: {message}")

    client_socket.send("Message received!".encode())

    client_socket.close()
