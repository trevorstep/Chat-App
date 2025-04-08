import socket  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.bind(("localhost", 12345)) 
server_socket.listen(1)  

print("Server is listening...")  
conn, addr = server_socket.accept() 
print(f"Connected by {addr}")  

while True:  
    data = conn.recv(1024) 
    if not data:  
        break  
    print(f"Received: {data.decode()}")  
    conn.sendall(data) 

conn.close()  
