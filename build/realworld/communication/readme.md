# PC - installation instructions
All the code here should be copied to the machine where RL model is supposed to be running. Once the files are copied, run the 'install' file or manually execute commands that live inside to install all the dependencies necessary to run the code.

There are two demonstration files prepared to use either an Xbox controller or a keyboard to steer the vehicle and get images from its point of view via a network. Before running a demo, you have to set up everything on the Odroid first (network, run the server script) and ensure both devices can 'see' each other in a network. Use 'ping' command to do a quick test.

Once everything is set, open a demo file you are about to run and find a 'Client' constructor. You have to update the IP address to which the client should connect to. This is the address of the Odroid. If you are using a hotspot to connect both devices, you should be able to see IP addresses of both PC and Odroid inside the hotspot properties/settings. Now you're ready to run a demo.

## Controller demo
The controller demo provides an opportunity to steer a vehicle via an Xbox controller. To start the demo, run the following command in a command prompt while being inside the 'communication' directory:
```shell
python controller_demo.py
```

The usage of an XInput controller (e.g. XBox 360 controller) requires DirectX, which is only available on Windows. The necessary software will automatically be installed by Windows 10 when connecting the controller to the machine. With earlier versions of Windows, DirectX might have to be downloaded manually. Download the version that is appropriate for your version of Windows. The library reading the input also requires the software "Pyglet". Command line code to install it can be found in the "install" file.

### How to use the controller
- Pressing the right trigger (labelled "RT") moves the vehicle forwards.
- Pressing the left trigger (labelled "LT") moves the vehicle backwards.
- Pressing the two triggers simultaneously cancels their functions out.
- Moving the left analog stick to the left steers the car to the left.
- Moving it to the right functions similarly.
- Pressing the 'X' button requests an image and saves it locally where the demo code is running.

## Keyboard demo
This demo works similarly to the contorller one but this one utilises a keyboard instead to control the vehicle. To start the demo, run the following command in a command prompt while being inside the 'communication' directory:
```shell
python keyboard_demo.py
```

### How to use the keyboard
- 'W': move forwards.
- 'S': move backwards.
- 'A': turn left (without moving).
- 'D': turn right (without moving).
- 'Q': turn left while moving forward.
- 'E': turn right while moving forward.
- 'I': request an image (saves an image locally where the code is running).
- 'space': finish the demo.