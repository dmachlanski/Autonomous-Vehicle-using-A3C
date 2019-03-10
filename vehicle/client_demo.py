import socket
import keyboard

host = '127.0.0.1'
port = 6666
keep_running = True

def send_data(forward, left, right):
    data = ""
    if(forward == True):
        data += '1'
    else:
        data += '0'
    data += ','
    if(left == True):
        data += '1'
    else:
        data += '0'
    data += ','
    if(right == True):
        data += '1'
    else:
        data += '0'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(data.encode('ascii'))
        data = client_socket.recv(230400)

def forward():
    send_data(True, False, False)
def left():
    send_data(False, True, False)
def right():
    send_data(False, False, True)
def forward_and_left():
    send_data(True, True, False)
def forward_and_right():
    send_data(True, False, True)
def finish():
    global keep_running
    keep_running = False

keyboard.hook_key('w', forward)
keyboard.hook_key('a', left)
keyboard.hook_key('d', right)
keyboard.hook_key('q', forward_and_left)
keyboard.hook_key('e', forward_and_right)
keyboard.hook_key('space', finish)

while keep_running:
    print("Running")