#!/usr/bin/python3
import serial
import keyboard
import time
import json
import sys
import subprocess

#for debugging
print("started")

#initilize global vars
r = 0
b = 0
running = False
elapsedTime = 0
ports = {}

#load the json file so the values can be incremnted
with open('/home/jaxson/dronebeacon-board/game_state.json', 'r') as game_state:
    scores = json.load(game_state)

scores["red"] = r
scores["blue"] = b
scores["gameTime"] = 180-elapsedTime

#reset scores and gma etime to zero (they may not be because of past games)
with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
    json.dump(scores, game_state)

# ser0 = "nothing"
# ser1 = "nothing"
# ser2 = "nothing"
# ser3 = "nothing"
# ser4 = "nothing"
# ser5 = "nothing"
# ser6 = "nothing"
# ser7 = "nothing"

# data0 = "nothing"
# data1 = "nothing"
# data2 = "nothing"
# data3 = "nothing"
# data4 = "nothing"
# data5 = "nothing"
# data6 = "nothing"
# data7 = "nothing"

# isBlue = [
#     data0 == "BLUE",
#     data1 == "BLUE",
#     data2 == "BLUE",
#     data3 == "BLUE",
#     data4 == "BLUE",
#     data5 == "BLUE",
#     data6 == "BLUE",
#     data7 == "BLUE"
#         ]

# isRed = [
#     data0 == "RED",
#     data1 == "RED",
#     data2 == "RED",
#     data3 == "RED",
#     data4 == "RED",
#     data5 == "RED",
#     data6 == "RED",
#     data7 == "RED"
#         ]

# try:
#     ser0 = serial.Serial("/dev/ttyUSB0", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected (ser0)")
# try:
#     ser1 = serial.Serial("/dev/ttyUSB1", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected ser1")
# try:
#     ser2 = serial.Serial("/dev/ttyUSB2", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected ser2")
# try:
#     ser3 = serial.Serial("/dev/ttyUSB3", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected ser3")
# try:
#     ser4 = serial.Serial("/dev/ttyUSB4", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected ser4")
# try:
#     ser5 = serial.Serial("/dev/ttyUSB5", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected ser5")
# try:
#     ser6 = serial.Serial("/dev/ttyUSB6", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected ser6")
# try:
#     ser7 = serial.Serial("/dev/ttyUSB7", 9600, timeout = 1)
# except serial.SerialException as e:
#     print("not all beacons connected ser7")

while True:
    if keyboard.is_pressed('esc'):
        print("clicked esc running sys.exit()...")
        sys.exit()
    if keyboard.is_pressed('space'):

        for i in range(10):
            serialPort = f"/dev/ttyUSB{i}"
            try:
                ports[str(i)] = serial.Serial(serialPort, 9600, timeout = 0.001)
            except serial.SerialException as e:
                print(f"beacon {i} not connected")

        print(ports)

        running = True
        print("space pressed")
        startTime = time.time()
        elapsedTime = 0
        r = 0
        b = 0
        scores["red"] = r
        scores["blue"] = b
        scores["gameTime"] = 180-elapsedTime
        with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
            json.dump(scores, game_state)

    while running and elapsedTime <= 180:

        for i in ports:
            ser = ports[str(i)]
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data == "BLUE":
                b += 1
                print(f"incremented blue to {b}")
                scores["blue"] = b

            if data == "RED":
                r += 1  
                print(f"incremented red to {r}")
                scores["red"] = r

        # if ser0 != "nothing":
        #     data0 = ser0.readline().decode('utf-8', errors='ignore').strip()
        # if ser1 != "nothing":
        #     data1 = ser1.readline().decode('utf-8', errors='ignorestrip()').
        # if ser2 != "nothing":
        #     data2 = ser2.readline().decode('utf-8', errors='ignore').strip()
        # if ser3 != "nothing":
        #     data3 = ser3.readline().decode('utf-8', errors='ignore').strip()
        # if ser4 != "nothing":
        #     data4 = ser4.readline().decode('utf-8', errors='ignore').strip()
        # if ser5 != "nothing":
        #     data5 = ser5.readline().decode('utf-8', errors='ignore').strip()
        # if ser6 != "nothing":
        #     data6 = ser6.readline().decode('utf-8', errors='ignore').strip()
        # if ser7 != "nothing":
        #     data7 = ser7.readline().decode('utf-8', errors='ignore').strip()

        # if data1 == "BLUE":
        #     b += 1
        #     print(f"incremented blue to {b}")
        #     scores["blue"] = b

        # if data0 == "RED":
        #     r += 1
        #     print(f"incremented red to {r}")
        #     scores["red"] = r

        currentTime = time.time()
        elapsedTime = currentTime - startTime
        
        scores["gameTime"] = round(180-elapsedTime)

        with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
            json.dump(scores, game_state)

        if keyboard.is_pressed('enter'):
            print("elapsed time > 180")
            r = 0
            b = 0
            elapsedTime = 0
            scores["red"] = r
            scores["blue"] = b
            scores["gameTime"] = 180-elapsedTime
            with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
                json.dump(scores, game_state)
            running = False
            break

        if elapsedTime > 180:
            running = False
            break