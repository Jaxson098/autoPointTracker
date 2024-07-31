import serial
import random
import keyboard

ports = {}
beacon_amount = 0

for i in range(10):
    serialPort = f"/dev/ttyUSB{i}"
    try:
        ports[str(i)] = serial.Serial(serialPort, 9600, timeout = 0.001)
        print(f"beacon {i} CONNECTED")
    except serial.SerialException as e:
        print(f"beacon {i} NOT connected")

print(f"ports: {ports}")

def sendGame(event=None):
    for i in ports:
        i.write(b"Wack-A-Mole\n")
        print(f"port {i}s gamemode set to Wack-A-Mole")

sendGame()

for i in ports:
    beacon_amount += 1
    print(f"beacon_amount: {beacon_amount}")

def changeRandom():
    toChange = random.randint(1, beacon_amount)
    ports[str(toChange)].write()
    print(f"chnaged port {toChange}")



















# beacon_amount -= 1

# third = beacon_amount / 3
# print(f"third: {round(third)}")

# amountToChange = random.randint(1, round(third))
# print(f"amountToChange: {amountToChange}")

# beaconNumToChange = []

# for i in range(amountToChange):
#     beaconNumToChange[str(i)] = random.randint(1, beacon_amount)

# if keyboard.is_pressed('space'):
#     for i in beaconNumToChange:
#         ports[str(i)].write(b"change\n")

# beaconNumToChange = [random.randint(1, beacon_amount) for i in range(amountToChange)]
# print(f"beaconNumsToChange: {beaconNumsToChange}")
# while True:
#     for i in beaconNumsToChange:
#         ports[str(i)].write(b"change\n")
# import keyboard
# import serial

# port = serial.Serial("/dev/ttyUSB0", 9600)

# def sendGame():
#     port.write(b"Wack-A-Mole\n")
#     print("space")

# def sendGreen():
#     port.write(b"GREEN\n")
#     print("enter")

# while True:
#     keyboard.on_press_key('space', sendGame)
#     keyboard.on_press_key('enter', sendGreen)

import keyboard
import serial

port = serial.Serial("/dev/ttyUSB0", 9600)
# data = port.readline().decode('utf-8', errors='ignore').strip()
# print(data)

def sendGame(event=None):
    port.write(b"Wack-A-Mole\n")
    print("space")

def sendGreen(event=None):  # Add event=None to accept the event argument
    port.write(b"GREEN\n")
    print("enter")

# Make sure to call keyboard.unhook_all() at the end to avoid adding multiple hooks if you run the script multiple times.
keyboard.unhook_all()

keyboard.on_press_key('space', sendGame)
keyboard.on_press_key('enter', sendGreen)

# Keep the script running to listen for key events
keyboard.wait('esc')


    # data = port.readline().decode('utf-8', errors='ignore').strip()
    # print(f"\ndata: {data}\n")