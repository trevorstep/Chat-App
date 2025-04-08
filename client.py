import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Server disconnected.")
                break
            print(f"\nServer: {data.decode()}")
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))

# Start receiver thread
receiver = threading.Thread(target=receive_messages, args=(client_socket,))
receiver.start()

# Main thread for sending messages
try:
    while True:
        message = input()
        if message.lower() == "exit":
            break
        client_socket.sendall(message.encode())
except:
    pass

client_socket.close()
print("Client closed.")

