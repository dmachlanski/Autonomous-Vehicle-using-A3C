import socket
import keyboard
from client import Client
import time
import cv2

keep_running = True
client = Client('192.168.137.130', 7777)
img_count = 1

def forward():
    global client
    client.set_control(1,0,0,0)
def left():
    global client
    client.set_control(0,0,1,0)
def right():
    global client
    client.set_control(0,0,0,1)
def backward():
    global client
    client.set_control(0,1,0,0)
def forward_and_left():
    global client
    client.set_control(1,0,1,0)
def forward_and_right():
    global client
    client.set_control(1,0,0,1)
def image():
    global client, img_count
    img = client.get_image()
    cv2.imwrite(f'img{img_count}.png', img)
    img_count += 1
def finish():
    global keep_running
    keep_running = False

keyboard.hook_key('w', forward)
keyboard.hook_key('a', left)
keyboard.hook_key('d', right)
keyboard.hook_key('s', backward)
keyboard.hook_key('q', forward_and_left)
keyboard.hook_key('e', forward_and_right)
keyboard.hook_key('i', image)
keyboard.hook_key('space', finish)

while keep_running:
    print("Running")
    time.sleep(0.5)

print("Stopped")