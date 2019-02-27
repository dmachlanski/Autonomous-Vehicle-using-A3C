from vehicle import Vehicle
import time
import keyboard

if __name__ == "__main__":
    speed = 250
    turn = 250
    delta_speed = 10
    delta_turn = 50
    keep_running = True
    # Windows
    port = 'COM3'
    # Linux
    #port = '/dev/ttyUSB0'
    baudrate = 115200

    def up():
        global speed, delta_speed
        speed += delta_speed
        if speed > 500: speed = 500
    def down():
        global speed, delta_speed
        speed -= delta_speed
        if speed < 0: speed = 0
    def left():
        global turn, delta_turn
        turn -= delta_turn
        if turn < 0: turn = 0
    def right():
        global turn, delta_turn
        turn += delta_turn
        if turn > 500: turn = 500
    def stop():
        global speed
        speed = 250
    def reset():
        global speed, turn
        speed = turn = 250
    def finish():
        global keep_running
        keep_running = False

    keyboard.hook_key('up', up)
    keyboard.hook_key('down', down)
    keyboard.hook_key('left', left)
    keyboard.hook_key('right', right)
    keyboard.hook_key('space', stop)
    keyboard.hook_key('r', reset)
    keyboard.hook_key('q', finish)

    with Vehicle(port, baudrate) as car:
        while keep_running:
            time.sleep(0.5)
            car.move(speed, turn)
            print(f'Speed: {speed}, turn: {turn}')