"""
NEEDS TO BE TESTED
"""

import time
import xinput
import sys
from client import Client
import cv2

def main():
    # Default values for analog input
    #global steering, speed, stick_deadzone, running, last_l_stick_x, last_left_trigger, last_right_trigger
    #steering = 250
    #speed = 250
    #stick_deadzone = 0.15
    #last_l_stick_x = 0.0
    #last_left_trigger = 0.0
    #last_right_trigger = 0.0
    
    # Default values for digital input
    global left, right, forward, stop
    left = False
    right = False
    forward = False
    stop = False
    
    running = True
    img_count = 1

    # Networking
    client = Client('192.168.137.130', 7777)

    # Controller initialisation
    joysticks = xinput.XInputJoystick.enumerate_devices()
    if not joysticks:
        sys.exit(0)
    j = joysticks[0]

    @j.event
    def on_button(button, pressed):
        """
        This event is triggered when one of the digital buttons are pressed.
        If it's the "Start" button, the program resets all values and stops running.
        """
        # For analog input
        #global steering, speed, running
        
        global left, right, forward, stop, running, img_count
        
        if button == 5:
            # Button 5 = "Start" button
            running = False
            left = False
            right = False
            forward = False
            stop = True
            
            # For analog input
            #steering = 250
            #speed = 250

        if button == 10:
            img = client.get_image()
            cv2.imwrite(f'img{img_count}.png', img)
            img_count += 1

    @j.event
    def on_axis(axis, value):
        """
        This event triggers when one of the analog items on the controller changes value.
        If it's any of the triggers, "speed" is updated, if it's the left analog stick, "steering" is updated.
        """
        # For analog input
        #global steering, speed, stick_deadzone
        #global last_l_stick_x, last_left_trigger, last_right_trigger
        
        global left, right, forward, stop
        
        if not stop and axis == "right_trigger":
            if value >= 0.5:
                forward = True
            else:
                forward = False
            # For analog input
            #last_left_trigger = value
            #speed = trigger_to_speed(last_left_trigger, last_right_trigger)
        elif axis == "left_trigger":
            if value >= 0.5:
                stop = True
                forward = False
            else:
                stop = False
            # For analog input
            #last_right_trigger = value
            #speed = trigger_to_speed(last_left_trigger, last_right_trigger)
        elif axis == "l_thumb_x":
            if value >= 0.3:
                left = False
                right = True
            elif value <= -0.3:
                left = True
                right = False
            else:
                left = False
                right = False
            # For analog input
            #last_l_stick_x = value
            #steering = stick_to_steering(last_l_stick_x, stick_deadzone)

    # Running loop
    while running:
        j.dispatch_events()
        print(f"Left:{left}, Right:{right}, Forward:{forward}, Stop:{stop}")
        client.set_control(forward, left, right)
        time.sleep(0.3)


def trigger_to_speed(left_trigger, right_trigger):
    """
    This is only for analog input.
    Converts the two float values of left_trigger and right_trigger (both of which are between 0.0 and 1.0,
    inclusive on both sides) to a single value between 0 and 500, inclusive on both sides.
    This is the value sent to the vehicle as the speed.
    """
    triggers = right_trigger - left_trigger
    rounded = round(triggers * 250)
    inted = int(rounded)
    return inted + 250


def stick_to_steering(left_stick_x, deadzone):
    """
    This is only for analog input.
    Converts the float value of the left stick's X axis (left_stick_x, which is approximately between -0.5 and 0.5)
    to a value between 0 and 500. If the initial value is within the deadzone (stick_deadzone), the new value
    is automatically 250.
    This is the value sent to the vehicle for steering.
    """
    multiplier = 250 / (0.5 - deadzone)

    if left_stick_x >= deadzone:
        stick_value = left_stick_x - deadzone
        steering_value = stick_value * multiplier
        int_steering_value = int(round(steering_value))
        return int_steering_value + 250
    elif left_stick_x <= -deadzone:
        stick_value = left_stick_x + deadzone
        steering_value = stick_value * multiplier
        int_steering_value = int(round(steering_value))
        return int_steering_value + 250
    else:
        return 250


if __name__ == "__main__":
    main()
