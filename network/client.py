import socket

host = '127.0.0.1'
port = 6666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))
    client_socket.sendall(b"Message from the client")
    data = client_socket.recv(1024)
    print(f"Received {repr(data)}")