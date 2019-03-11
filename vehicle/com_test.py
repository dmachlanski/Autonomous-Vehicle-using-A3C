from vehicle import Vehicle

port = '/dev/ttyUSB0'
baudrate = 115200

with Vehicle(port, baudrate) as car:
    print("Connected to the device")
    car.move(250, 250)
    print("Command sent")

print("Finishing")