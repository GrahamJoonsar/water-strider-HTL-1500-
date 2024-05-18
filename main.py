"""
Author(s): Graham Joonsar, Jacob Banta

Run pi code first, then here

This is the code for the surface laptop.

RPI Password:
 - password-
    
SSH into RPI:
 - ssh pi@raspberrypi.local
 - cd Desktop/whale
 - python3 control.py

""" 

# External Libs
from numpysocket import NumpySocket
import numpy
import cv2

# Internal libs
import controls

""" Starting the Robot """
print("Initializing Joysticks")
controls.init_joysticks()

# Clear screen and set cursor to the top right
#print("\033[?25l")
#print("\033[2J")

# Vars
cam_scale = 2
img_count = 0

# Establishing Connection and Main Loop
port = 4444
host = "raspberrypi.local"
with NumpySocket() as sock:
    # Attempt Connection
    sock.connect((host, port))

    # Main code loop
    while True:
        # Sending the control data to the pi
        send_data = controls.get_send_data()

        # Getting pilot input 
        controls.get_input()
        controls.process_input()

        buffer = numpy.arange(1000)
        buffer[0:len(send_data)] = numpy.array(send_data)
        sock.sendall(buffer)
        img = sock.recv()

        if controls.capture_img():
            h, w, channels = img.shape
            left_part = img[:, :w//2]
            cv2.imwrite("images/image.png", left_part)
            img_count += 1
        else:
            img = cv2.resize(img, (int(320*2*cam_scale), int(240*cam_scale)))
            cv2.imshow("Cameras", img)

        # Stops the code
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()