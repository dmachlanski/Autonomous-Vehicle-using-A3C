import socket
from util import check_exit, encrypt, decrypt
import ctypes
import numpy as np
import sys

	
	
def connect(PORT):
	HOST = ""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print(s.getsockname())
	s.bind((HOST, PORT))
	s.listen(1)
	print("Waiting for connection....")
	conn, addr = s.accept()
	return s, conn, addr

def recv_msg(conn, addr, PORT):
	print('Connection established at ip:{}, port:{}'.format(addr[0], PORT))
	print("--"*5)
	print("Waiting for client message...")
	try:
		data = conn.recv(230400)
		result = (ctypes.c_ubyte * 230400).from_buffer_copy(data)
		check_exit(data)
		img = np.asarray(result, dtype=int)
		print(img.shape)
		return img
	except:
		return None
	
def send_msg(s):
	d = str.encode(input())
	s.sendall(encrypt(d))
	check_exit(d)

def recv_img():
	PORT = 7777   					#int(input('Assign port num:  '))
	s, conn, addr = connect(PORT)
	with conn:
		img = recv_msg(conn, addr, PORT)
		s.close()
	return img

def net(img):
	None
	
def drive_car():
	None
		
while True:
	img = recv_img()
	net(img)
	drive_car()