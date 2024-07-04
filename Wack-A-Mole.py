import serial
import random
import time

ports = {}
beacon_amount = 0

for i in range(10):
    serialPort = f"/dev/ttyUSB{i}"
    try:
        ports[str(i)] = serial.Serial(serialPort, 9600, timeout = 0.001)
    except serial.SerialException as e:
        print(f"beacon {i} not connected")

print(f"ports: {ports}")

for i in ports:
    beacon_amount += 1
    print(f"beacon_amount: {beacon_amount}")

beacon_amount -= 1

third = beacon_amount / 3
print(f"third: {round(third)}")

amountToChange = random.randint(1, round(third))
print(f"amountToChange: {amountToChange}")

beaconNumsToChange = [random.randint(1, beacon_amount) for i in range(amountToChange)]
print(f"beaconNumsToChange: {beaconNumsToChange}")
while True:
    for i in beaconNumsToChange:
        ports[str(i)].write(b"change\n")