import serial
import random
import keyboard
import time

ports = {}
beacon_amount = 0
p = 0
avg = 0
running = False
lastChanged = None

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

# def getScores():
#     global p
#     for i  in ports:
#         ser = ports[str(i)]
#         data = ser.readline().decode('utf-8', errors='ignore').strip()
#         if data == "POINT":
#             p += 1
#             print(f"points: {p}")
#             changeRandom()

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

while True:
    if keyboard.is_pressed('space'):
        sendGame()
        print("space pressed")
        startTime = time.time()
        elapsedTime = 0
        p = 0
        running = True
        changeRandom()

    while running and elapsedTime <= 60:
        getScores()
        currentTime = time.time()
        elapsedTime = currentTime - startTime
        # print(elapsedTime)

        if keyboard.is_pressed('enter'):
            print("canceled (enter)")
            elapsedTime = 0
            p = 0
            avg = 0
            running = False
            for i in ports:
                ports[str(i)].write(b"RESET\n")
            break

        if elapsedTime > 60:
            print("elapsedTime > 60")
            running = False
            for i in ports:
                ports[str(i)].write(b"RESET\n")
            break 