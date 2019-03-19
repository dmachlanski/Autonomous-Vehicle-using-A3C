Torcs files that have been changed:
->raceengine.cpp
->raceman.h
->/src/libs/raceengineclient/Makefile
->car.h
->/src/drivers/ce903

Other files required:
->exporter.cpp
->exporter.h
->server.py

Instructions to run:
->Go to Documents folder
->run server.py
->Open a separate terminal
->run torcs
->In torcs GUI:
->->Race
->->Practice
->->Configure Race
->->Select Track
->->Ensure that the ce903 car is in the selected box on the left side of the screen
->->Accept
->->New Race

Program Flow:
->Server.py opens and waits for message over the socket
->torcs begins a race:
->->reupdate() function is called in the race engine
->->(1 in 500 times):
->->->An Exporter class is created
->->->Screen image data is taken from the framebuffer
->->->The Exporter class resizes the image and sends it to server.py via a socket
->server.py recieves the image and converts it to np array
->the image is converted to [[R,G,B][R,G,B]....]

->This is where the NN code will be implemented

->Output driving instructions are written to a csv [acceleration, steering, askRestart]

->torcs goes to ce903.cpp for driving instructions
->instructions are read from the csv (csv is better in this instance because of the refresh frequency 
  of torcs)
->the car drives!!!

---If any torcs files are changed you must "make install" the program again---

To create reinforcement learning:
->Open ce903.cpp (this is the robot car)
->Look in car.h
->car.h shows all the car information which can be accessed (damage, laptime, distance from centre of
  track)
->Use the car information to evaluate the previous instructions
->Feedback to the NN via csv
	http://www.berniw.org/tutorials/robot/tutorial.html