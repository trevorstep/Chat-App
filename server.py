import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen()

print("Server is listening on localhost:12345")

clients = {} 

def broadcast(message, sender_conn=None):
    for client_conn in clients:
        if client_conn != sender_conn:
            try:
                client_conn.sendall(message.encode())
            except:
                client_conn.close()

def handle_client(conn, addr):
    try:
        conn.sendall("Enter your username: ".encode())
        username = conn.recv(1024).decode().strip()
        clients[conn] = username
        print(f"{username} connected from {addr}")
        broadcast(f"{username} has joined the chat!", conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", sender_conn=conn)
    except ConnectionResetError:
        print(f"{clients.get(conn, 'Unknown')} disconnected unexpectedly.")
    finally:
        broadcast(f"{clients.get(conn, 'A user')} has left the chat.", conn)
        print(f"{clients.get(conn, 'A user')} has disconnected.")
        conn.close()
        clients.pop(conn, None)

while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
