import socket  

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
client_socket.connect(("localhost", 12345))  

while True:  
    message = input("Enter message: ")  
    if message.lower() == "exit":  
        break  
    client_socket.sendall(message.encode())   
    data = client_socket.recv(1024) 

client_socket.close()  
