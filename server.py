import socket
import threading

# Set up server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen()

print("Server is listening on localhost:12345")

clients = {}  # Keep track of client sockets and usernames

def handle_client(conn, addr):
    try:
        # Ask for username
        conn.sendall("Enter your username: ".encode())
        username = conn.recv(1024).decode().strip()
        clients[conn] = username
        print(f"{username} connected from {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"{username}: {message}")
            conn.sendall(f"{username}: {message}".encode())
    except ConnectionResetError:
        print(f"{clients.get(conn, 'Unknown')} disconnected unexpectedly.")
    finally:
        print(f"{clients.get(conn, 'A user')} has disconnected.")
        conn.close()
        clients.pop(conn, None)

# Accept clients forever
while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
