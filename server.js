#!/home/jaxson/.nvm/versions/node/v22.3.0/bin/node
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const filePath = '/home/jaxson/dronebeacon-board/game_state.json';

app.get('/', (req, res) => {
    res.sendFile('/home/jaxson/dronebeacon-board/index.html');
});

io.on('connection', (socket) => {
    console.log('a user connected');
    const sendFileContent = () => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                return;
            }
            socket.emit('fileContent', data);
        });
    };

    sendFileContent();
    fs.watchFile(filePath, { interval: 500 }, (curr, prev) => { // Check every second
        sendFileContent();
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

server.listen(3000, () => {
    console.log('Server is listening on port 3000');
});