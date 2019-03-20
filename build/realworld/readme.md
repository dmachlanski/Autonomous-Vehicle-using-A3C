# Installation instructions
The real-world part of the system is divided into two computers:
- PC (RL model is running there)
- Odroid (located on the vehicle)

Both machines have to be in the same network to be able to communicate with each other wirelessly. Perhaps the easiest solution is to create a hotspot using a third device and connect both PC and Odroid to a newly created network.

## PC
The code that should be deployed into a PC can be found inside the 'communication' folder, together with further instructions.

## Odroid
The code required and further instructions can be found inside the 'odroid' directory.

# How to run demonstrations
Before running any demo, first you need to set up the Odroid part and run necessary code (server). You can start the code on Odroid either manually or automatically at OS startup. More about this can be found in the 'odroid' folder.

Requirements to run a demo:
- Both PC and Odroid are in the same network and can 'talk' to each other.
- The server code is running on the Odroid and waiting for new requests.

Now you can run a demo on a PC, two examples of which can be found inside the 'communication' folder.