import random
import socket, select
from time import gmtime, strftime
from random import randint

host = '127.0.0.1'
port = 6666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    conn, addr = server_socket.accept()

    with conn:
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received from client: {repr(data)}")
            conn.sendall(b"Message from the server")