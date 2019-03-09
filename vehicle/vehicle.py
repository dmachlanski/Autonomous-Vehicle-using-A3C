import serial

class Vehicle:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate=baudrate)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.ser.close()    

    def move(self, speed, turn):
        """ Sets vehicle's speed and steering angle. Both variables are in the range of [0, 500].
            Speed:
            - 0: Go backwards at maximum speed
            - 250: Break
            - 500: Go forwards at maximum speed
            Turn:
            - 0: Turn left (max)
            - 250: Straight
            - 500: Turn right (max)
        """
        if(speed < 0 or speed > 500 or turn < 0 or turn > 500):
            print("Speed and turn must be within [0, 500] range")
            return

        cmd1 = 'y1' + '{:0>3d}'.format(speed) + '!'
        cmd2 = 'y2' + '{:0>3d}'.format(turn) + '!'
        self.ser.write(cmd1.encode('ascii'))
        self.ser.write(cmd2.encode('ascii'))

    def reset(self):
        self.move(250, 250)