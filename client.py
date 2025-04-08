import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import random

# ANSI-free colors (for GUI)
COLORS = [
    "red", "green", "blue", "purple", "orange", "teal"
]

username_colors = {}

def get_color(username):
    if username not in username_colors:
        username_colors[username] = random.choice(COLORS)
    return username_colors[username]

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=5)

        self.msg_entry = tk.Entry(master, width=40)
        self.msg_entry.pack(side=tk.LEFT, padx=(10, 5), pady=(0, 10))
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        self.username = tk.simpledialog.askstring("Username", "Enter your username:")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 12345))

        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                self.display_message(message)
            except:
                break

    def display_message(self, message):
        if ':' in message:
            username, msg = message.split(':', 1)
            username = username.strip()
            msg = msg.strip()
            color = get_color(username)
        else:
            username = ""
            msg = message
            color = "black"

        self.chat_area.configure(state='normal')
        if username:
            self.chat_area.insert(tk.END, f"{username}: ", (username,))
            self.chat_area.insert(tk.END, f"{msg}\n")
            self.chat_area.tag_config(username, foreground=color)
        else:
            self.chat_area.insert(tk.END, f"{msg}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg:
            full_msg = f"{self.username}: {msg}"
            try:
                self.client_socket.sendall(full_msg.encode())
                self.msg_entry.delete(0, tk.END)
            except:
                self.display_message("Error sending message.")

if __name__ == '__main__':
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
