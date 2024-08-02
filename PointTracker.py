#!/usr/bin/python3
import serial
import keyboard
import time
import json
import sys

#for debugging
print("started")

#initilize global vars
r = 0
b = 0
running = False
elapsedTime = 0
ports = {}
portAmount = 0

def updatePoints(r,b,elapsedTime):
    #load the json file so the values can be incremnted
    with open('/home/jaxson/AutoPointTracker/game_state.json', 'r') as game_state:
        scores = json.load(game_state)

    scores["red"] = r
    scores["blue"] = b
    scores["gameTime"] = round(180-elapsedTime)

    with open('/home/jaxson/AutoPointTracker/game_state.json', 'w') as game_state:
        json.dump(scores, game_state)

def getPorts():
    for i in range(10):
        serialPort = f"/dev/ttyUSB{i}"
        try:
            ports[str(i)] = serial.Serial(serialPort, 9600, timeout = 0.001)
            print(f"beacon {i} connected")
        except serial.SerialException as e:
            print(f"beacon {i} not connected")

getPorts()
for i in ports:
    i.write("CaptureFlag")

def getScores():
    global b
    global r
    for i  in ports:
        ser = ports[str(i)]
        data = ser.readline().decode('utf-8', errors='ignore').strip()
        if data == "BLUE":
            b += 1
            print(f"incremented blue to {b}")

        elif data == "RED":
            r += 1  
            print(f"incremented red to {r}")
    return b, r, 

def resetBeacons():
    global ports
    startB = dict(list(ports.items())[len(ports)//2:])
    startR = dict(list(ports.items())[:len(ports)//2])
    for i in startB:
        i.write("Blue")
    for i in startR:
        i.write("Red")
    print(f"\nstartB = {startB}\n")
    print(f"\nstartR = {startR}\n")

while True:
    if keyboard.is_pressed('esc'):
        print("clicked esc running sys.exit()...")
        sys.exit()

    if keyboard.is_pressed('space'):
        
        getPorts()
        resetBeacons()
        running = True
        print("space pressed")
        startTime = time.time()
        elapsedTime = 0
        r = 0
        b = 0
        
        updatePoints(r,b,elapsedTime)

    while running and elapsedTime <= 180:

        getScores() 

        currentTime = time.time()
        elapsedTime = currentTime - startTime
        
        updatePoints(r,b,elapsedTime)

        if keyboard.is_pressed('enter'):
            print("canceled (enter)")

            r = 0
            b = 0
            elapsedTime = 0
            updatePoints(r,b,elapsedTime)
            running = False
            break

        if elapsedTime > 180:
            running = False
            break
