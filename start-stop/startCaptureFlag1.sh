#!/bin/bash

sudo python /home/jaxson/autoPointTracker/PointTracker.py &

echo $! > /tmp/pythonCaptureFlagPID.txt