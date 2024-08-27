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

def updatePoints(r,b,elapsedTime,message):
    #load the json file so the values can be incremnted
    with open('/home/jaxson/autoPointTracker/game_state.json', 'r') as game_state:
        scores = json.load(game_state)

    scores["red"] = r
    scores["blue"] = b
    scores["gameTime"] = round(90-elapsedTime)
    scores["message"] = message

    with open('/home/jaxson/autoPointTracker/game_state.json', 'w') as game_state:
        json.dump(scores, game_state)

def getPorts():
    for i in range(10):
        serialPort = f"/dev/ttyUSB{i}"
        try:
            ports[str(i)] = serial.Serial(serialPort, 9600, timeout = 0.001)
            print(f"beacon {i} connected")
        except serial.SerialException as e:
            print(f"beacon {i} not connected")

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
    return b, r

def sendGame():
    for i in ports:
        ports[str(i)].write(b"CaptureFlag\n")
        print(f"port {i}s gamemode set to CaptureFlag")

def resetBeacons():
    # startB = dict(list(ports.items())[len(ports)//2:])
    startR = dict(list(ports.items())[:len(ports)//2])
    for i in startR:
        ports[str(i)].write(b"RED\n")
    # print(f"\nstartR = {startR}\n")

getPorts()
sendGame()

while True:
    if keyboard.is_pressed('esc'):
        for i in ports:
            ports[str(i)].write(b"STOP\n") 
        print("exiting game mode")
        print("clicked esc running sys.exit()...")
        sys.exit()


    # if keyboard.is_pressed('r'):
    #     # resetBeacons()
    #     print("clicked r re seting beacons...")

    if keyboard.is_pressed('space'): 
        
        sendGame()
        resetBeacons()

        elapsedTime = 0
        r = 0
        b = 0

        print("space pressed")


        updatePoints(r,b,elapsedTime, "3")
        time.sleep(1)
        print("\n3\n")
        updatePoints(r,b,elapsedTime, "2")
        time.sleep(1)
        print("2\n")
        updatePoints(r,b,elapsedTime, "1")
        time.sleep(1)
        print("1\n")
        updatePoints(r,b,elapsedTime, "GO!")

        running = True
        startTime = time.time()
        
    while running and elapsedTime <= 90:

        getScores() 

        currentTime = time.time()
        elapsedTime = currentTime - startTime
        
        updatePoints(r,b,elapsedTime,"Game Mode: Capture The Flag")

        if keyboard.is_pressed('enter'):
            print("canceled (enter)")

            r = 0
            b = 0
            elapsedTime = 0
            updatePoints(r,b,elapsedTime,"Game Mode: Capture The Flag (reset)")

            for i in ports:
                ports[str(i)].write(b"STOP\n")
            resetBeacons()

            running = False
            break

        if elapsedTime > 180:
            updatePoints(r,b,elapsedTime,"Game Over! Good Job!")

            for i in ports:
                ports[str(i)].write(b"STOP\n")
            resetBeacons()

            running = False
            break
