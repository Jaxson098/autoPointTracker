#!/bin/bash

node /home/jaxson/autoPointTracker/server.js &

echo $! > /tmp/jsCaptureFlagPID.txt