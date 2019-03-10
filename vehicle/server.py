import socket
from camera import Camera
from vehicle import Vehicle
import pickle

class Server:
    def __init__(self, host='127.0.0.1', port=6666, vehicle_port='/dev/ttyUSB0', baudrate=115200, img_width=100, img_height=100,
                vehicle_speed=310, vehicle_delta_turn=150):
        self.host = host
        self.port = port
        self.vehicle_port = vehicle_port
        self.baudrate = baudrate
        self.img_width = img_width
        self.img_height = img_height
        self.vehicle_speed = vehicle_speed
        self.vehicle_delta_turn = vehicle_delta_turn

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            while True:
                conn, _ = server_socket.accept()
                with Camera() as cam:            
                    with Vehicle(self.vehicle_port, self.baudrate) as car:
                        with conn:
                            while True:
                                data = conn.recv(230400)
                                if not data:
                                    break

                                data = data.decode()
                                if data == "image":
                                    img = cam.shoot(self.img_width, self.img_height)
                                    data_to_send = pickle.dumps(img)
                                    conn.sendall(data_to_send)
                                else:
                                    retMsg = b"ERROR"
                                    try:
                                        control = data.split(',')
                                        car.move_alt(control, self.vehicle_speed, self.vehicle_delta_turn)
                                        retMsg = b"OK"
                                    except:
                                        print("Unrecognised request format")
                                        break
                                    finally:
                                        conn.sendall(retMsg)

if __name__ == "__main__":
    # Windows
    #port = 'COM3'
    # Linux (default)
    #port = '/dev/ttyUSB0'
    server = Server()
    server.start()