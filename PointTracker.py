#!/usr/bin/python3
import serial
import keyboard
import time
import json
import sys

print("started")

r = 0
b = 0
running = False
elapsedTime = 0

with open('/home/jaxson/dronebeacon-board/game_state.json', 'r') as game_state:
    scores = json.load(game_state)

scores["red"] = r
scores["blue"] = b
scores["gameTime"] = elapsedTime

with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
    json.dump(scores, game_state)

while True:
    if keyboard.is_pressed('esc'):
        print("clicked esc running sys.exit()...")
        sys.exit()
    if keyboard.is_pressed('space'):
        ser0 = serial.Serial("/dev/ttyUSB0", 9600, timeout = 1)
        ser1 = serial.Serial("/dev/ttyUSB1", 9600, timeout = 1)
        running = True
        print("space pressed")
        startTime = time.time()
        elapsedTime = 0
        r = 0
        b = 0
        scores["red"] = r
        scores["blue"] = b
        scores["gameTime"] = elapsedTime
        with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
            json.dump(scores, game_state)

    while running and elapsedTime <= 180:
        print("in while running loop")

        data0 = ser0.readline().decode('utf-8', errors='ignore').strip()
        data1 = ser1.readline().decode('utf-8', errors='ignore').strip()
        
        if data0 == "BLUE":
            b += 1
            print(f"incremented blue to {b}")
            scores["blue"] = b

        if data1 == "BLUE":
            b += 1
            print(f"incremented blue to {b}")
            scores["blue"] = b

        if data0 == "RED":
            r += 1
            print(f"incremented red to {r}")
            scores["red"] = r

        if data1 == "RED":
            r += 1
            print(f"incremented red to {r}")
            scores["red"] = r

        currentTime = time.time()
        elapsedTime = currentTime - startTime
        scores["gameTime"] = round(elapsedTime)

        with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
            json.dump(scores, game_state)

        if keyboard.is_pressed('enter'):
            print("elapsed time > 180")
            r = 0
            b = 0
            elapsedTime = 0
            scores["red"] = r
            scores["blue"] = b
            scores["gameTime"] = elapsedTime
            with open('/home/jaxson/dronebeacon-board/game_state.json', 'w') as game_state:
                json.dump(scores, game_state)
            running = False
            break

        if elapsedTime > 180:
            running = False
            break