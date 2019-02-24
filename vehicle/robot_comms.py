import serial

def vehicle(speed, turn):
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

    ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
    ser.write(b'y1' + '{:0>3d}'.format(speed) + '!')
    ser.write(b'y2' + '{:0>3d}'.format(turn) + '!')
    ser.close()

if __name__ == "__main__":
    
    # No speed, max turn right
    vehicle(250, 500)