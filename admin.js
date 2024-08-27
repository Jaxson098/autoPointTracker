#!/home/jaxson/.nvm/versions/node/v22.3.0/bin/node
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const childProces = require('child_process')

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.get('/', (req, res) => {
    res.sendFile('/home/jaxson/autoPointTracker/admin.html');
});

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });

    socket.on('startWack', () => {
        console.log("start wack")
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/startWack1.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/startWack2.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
    });

    socket.on('stopWack', () => {
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/stopWack1.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/stopWack2.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
    });

    socket.on('startCapture', () => {
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/startCaptureFlag1.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/startCaptureFlag2.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
    });

    socket.on('stopCapture', () => {
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/stopCaptureFlag1.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
        childProces.exec('sh /home/jaxson/autoPointTracker/start-stop/stopCaptureFlag2.sh', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting script: ${error}`);
            }
        });
    });

});

server.listen(3100, () => {
    console.log('Server is listening on port 3000');
});
