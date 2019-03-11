import socket
import time

def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
    return ip

if __name__ == "__main__":
    time.sleep(5)
    print(get_ip())