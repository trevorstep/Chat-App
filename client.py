import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))

# Start message receiver thread
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

# Send messages
while True:
    try:
        msg = input()
        if msg.lower() == "exit":
            break
        client_socket.sendall(msg.encode())
    except:
        break

client_socket.close()
