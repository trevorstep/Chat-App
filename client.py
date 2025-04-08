import socket
import threading
import random

COLORS = [
    '\033[91m',  # Red
    '\033[92m',  # Green
    '\033[93m',  # Yellow
    '\033[94m',  # Blue
    '\033[95m',  # Magenta
    '\033[96m',  # Cyan
]
RESET = '\033[0m'

username_colors = {}

def get_color_for_username(username):
    if username not in username_colors:
        username_colors[username] = random.choice(COLORS)
    return username_colors[username]

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode()
            if ':' in message:
                username, msg = message.split(':', 1)
                color = get_color_for_username(username.strip())
                print(f"{color}{username.strip()}{RESET}:{msg}")
            else:
                print(message)
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))

threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

while True:
    try:
        msg = input()
        if msg.lower() == "exit":
            break
        client_socket.sendall(msg.encode())
    except:
        break

client_socket.close()
