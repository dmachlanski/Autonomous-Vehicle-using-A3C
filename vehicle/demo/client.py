import socket
import pickle

class Client:
    def __init__(self, host='127.0.0.1', port=6666):
        self.host = host
        self.port = port

    def request(self, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(msg.encode('ascii'))
            return client_socket.recv(800000)

    def get_image(self):
        data = self.request('image')
        return pickle.loads(data, encoding='latin1')

    def set_control(self, forward, left, right):
        msg = f'{int(forward)},{int(left)},{int(right)}'
        self.request(msg)