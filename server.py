import socket
import threading

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected.")
                break
            print(f"\nClient: {data.decode()}")
        except:
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen(1)

print("Server is listening...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Start receiver thread
receiver = threading.Thread(target=receive_messages, args=(conn,))
receiver.start()

# Main thread for sending messages
try:
    while True:
        message = input()
        if message.lower() == "exit":
            break
        conn.sendall(message.encode())
except:
    pass

conn.close()
server_socket.close()
print("Server closed.")
