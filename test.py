# import random

# num = random.randint(0 ,0)
# print(num)

import serial
import keyboard

port = serial.Serial("/dev/ttyUSB0", 9600, timeout = 0.001)
port.write(b"Wack-A-Mole\n")
while True:
    if keyboard.is_pressed("enter"):
        port.write(b"Wack-A-Mole\n")
        print("enter")
    if keyboard.is_pressed("space"):
        port.write(b"GREEN\n")