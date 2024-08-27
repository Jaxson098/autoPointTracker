import serial
import random
import keyboard
import time
import json
import sys

ports = {}
beacon_amount = 0
p = 0
avg = 0
running = False
lastChanged = None

def updatePoints(p,elapsedTime, message):
    #load the json file so the values can be incremnted
    with open('/home/jaxson/autoPointTracker/wack_state.json', 'r') as game_state:
        scores = json.load(game_state)

    scores["points"] = p
    scores["gameTime"] = round(60-elapsedTime)
    scores["message"] = message

    with open('/home/jaxson/autoPointTracker/wack_state.json', 'w') as game_state:
        json.dump(scores, game_state)

for i in range(10):
    serialPort = f"/dev/ttyUSB{i}"
    try:
        ports[str(i)] = serial.Serial(serialPort, 9600, timeout = 0.001)
        print(f"beacon {i} CONNECTED")
    except serial.SerialException as e:
        print(f"beacon {i} NOT connected")

print(f"ports: {ports}")

def sendGame():
    for i in ports:
        ports[str(i)].write(b"Wack-A-Mole\n")
        print(f"port {i}s gamemode set to Wack-A-Mole")

# sendGame()


for i in ports:
    beacon_amount += 1
    print(f"beacon_amount: {beacon_amount}")

def changeRandom():
    global lastChanged
    while True:
        toChange = random.randint(0, beacon_amount - 1)
        print(f"to change: {toChange}")

        if toChange != lastChanged:
            ports[str(toChange)].write(b"GREEN\n")
            lastChanged = toChange
            print(f"chnaged port {toChange}")
            break
        else:
            print("same as last changed regenerating...")

def getScores():
    global p
    for i in ports:
        try:
            ser = ports[str(i)]
            # Attempt to read a line from the serial port
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data == "POINT":
                p += 1
                print(f"points: {p}")
                changeRandom()
        except serial.serialutil.SerialException as e:
            # Log the error or take other actions as needed
            print(f"Error reading from serial port {i}: {e}. Skipping this port.")

sendGame()

while True:
    if keyboard.is_pressed('esc'):
        for i in ports:
            ports[str(i)].write(b"STOP\n") 
        print("exiting game mode")
        print("clicked esc running sys.exit()...")
        sys.exit()


    if keyboard.is_pressed('space'):
        sendGame()
        print("space pressed")
        elapsedTime = 0
        p = 0

        updatePoints(p,elapsedTime, "3")
        print("\n3\n")
        time.sleep(1)
        updatePoints(p,elapsedTime, "2")
        print("2\n")
        time.sleep(1)
        updatePoints(p,elapsedTime, "1")
        print("1\n")
        time.sleep(1)
        updatePoints(p,elapsedTime, "GO!")

        running = True
        changeRandom()
        startTime = time.time()

    while running and elapsedTime <= 60:
        getScores()
        currentTime = time.time()
        elapsedTime = currentTime - startTime
        updatePoints(p,elapsedTime,"Game Mode: Wack-A-Mole")
        # print(elapsedTime)

        if keyboard.is_pressed('enter'):
            print("canceled (enter)")
            elapsedTime = 0
            p = 0
            avg = 0
            updatePoints(p,elapsedTime,"Game Mode: Wack-A-Mole (reset)")
            running = False
            for i in ports:
                ports[str(i)].write(b"RESET\n")
            break

        if elapsedTime > 60:
            print("elapsedTime > 60")
            updatePoints(p,60,"Game Over! Good Job!")
            running = False
            for i in ports:
                ports[str(i)].write(b"RESET\n")
            break 