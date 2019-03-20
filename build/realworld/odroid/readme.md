# Odroid - installation instructions
All the code here should be deployed into the Odroid device. The next step is to install python dependencies, which require Python 2.x already installed on the machine. Run 'install' file to acquire all the packages needed or run commands manually, which can be found inside the file.

Before running the code, make sure the Odroid is in the same network as the PC. You can create a hotspot network to achieve that.

There are two ways to start running the code: manually or automatically. Automatic approach is definitely more convenient as it doesn't require connecting external screen, mouse and keyboard to the devide in order to just run a script.

There should be no need to edit the server.py file at all as it obtains current IP address automatically before starting the actual server code. It waits for 60 seconds until starting the server in order to give the device some time to connect to a network.

## Running code manually
To start the code by hand, simply run the following command in the terminal:

```shell
python server.py
```

After 60 seconds, the server should start listening for incoming requests from clients.

## Running code automatically (Linux)
To start the code automatically at the startup of the system copy the following files to /bin:
- server.py
- vehicle.py
- camera.py

```shell
sudo cp /path/to/your_script.py /bin
```

Then, add a new Cron job:

```shell
sudo crontab -e
```

Scroll to the bottom and add the following line (after all the #'s):

```shell
@reboot python /bin/server.py &
```

Now the server script should start automatically after rebooting the device.