import socket
import numpy as np
import matplotlib.pyplot as plt
import pickle

#host = '172.20.10.4'
host = '127.0.0.1'
port = 6666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))
    client_socket.sendall(b"image")
    data = client_socket.recv(230400)

    print(f"Received data from the server")

    img = pickle.loads(data)
    print(img)
    print(img.shape)
    plt.imshow(img)
    plt.show()