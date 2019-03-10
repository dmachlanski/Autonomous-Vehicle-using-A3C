import socket
from random import randint
from camera import Camera
from vehicle import Vehicle
import pickle

#host = '172.20.10.4'
host = '127.0.0.1'
port = 6666
vehicle_port = 'COM3'
#vehicle_port = '/dev/ttyUSB0'
vehicle_baudrate = 115200

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()

    # Listen constantly for requests
    while True:
        conn, addr = server_socket.accept()

        with Camera() as cam:            
            with Vehicle(vehicle_port, vehicle_baudrate) as car:
                with conn:
                    #print(f"Connected by {addr}")

                    while True:
                        data = conn.recv(230400)
                        if not data:
                            break

                        print(f"Received from client: {repr(data)}")
                        data = data.decode()
                        if data == "image":
                            # Send an image
                            img = cam.shoot(100, 100)
                            print(img.shape)
                            data_to_send = pickle.dumps(img)
                            conn.sendall(data_to_send)
                        else:
                            retMsg = b"BAD"
                            try:
                                control = data.split(',')
                                speed = 250
                                turn = 250
                                if(control[0] == '1'):
                                    speed = 310
                                if(control[1] == '1'):
                                    turn = 100
                                elif(control[2] == '1'):
                                    turn = 400
                                car.move(speed, turn)
                                retMsg = b"OK"
                            except:
                                print("Unrecognised request format")
                                break
                            finally:
                                conn.sendall(retMsg)