import socket
from camera import Camera
from vehicle import Vehicle
import pickle
import time

class Server:
	def __init__(self, host='127.0.0.1', port=7777, vehicle_port='/dev/ttyUSB0', baudrate=115200, img_width=50, img_height=50,
                vehicle_delta_speed=60, vehicle_delta_turn=150):
		self.host = host
		self.port = port
		self.vehicle_port = vehicle_port
		self.baudrate = baudrate
		self.img_width = img_width
		self.img_height = img_height
		self.vehicle_delta_speed = vehicle_delta_speed
		self.vehicle_delta_turn = vehicle_delta_turn

	def start(self):
		try:
			server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_socket.bind((self.host, self.port))
			server_socket.listen(0)

			while True:
				conn, _ = server_socket.accept()
				with Camera() as cam:            
					with Vehicle(self.vehicle_port, self.baudrate) as car:
						try:
							while True:
								data = conn.recv(800000)
								if not data:
									break
								decoded = data.decode()
								if decoded == "image":
									img = cam.shoot(self.img_width, self.img_height)
									data_to_send = pickle.dumps(img)
									conn.sendall(data_to_send)
								else:
									retMsg = b"ERROR"
									try:
										control = decoded.split(',')
										car.move_alt(control, self.vehicle_delta_speed, self.vehicle_delta_turn)
										retMsg = b"OK"
									except:
										print "Unrecognised request format"
										break
									finally:
										conn.sendall(retMsg)
						finally:
							conn.close()
		finally:
			server_socket.close()

def get_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			s.connect(("8.8.8.8", 80))
			ip = s.getsockname()[0]
		except:
			ip = '127.0.0.1'
	finally:
		s.close()
	return ip

if __name__ == "__main__":
  # Windows
  #port = 'COM3'
  # Linux (default)
  #port = '/dev/ttyUSB0'

  # Wait for the network to connect
	time.sleep(60)

	ip = get_ip()

	server = Server(ip)
	server.start()