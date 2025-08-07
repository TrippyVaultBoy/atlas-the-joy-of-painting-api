const express = require('express');
const routes = require('./routes/index.js');

const server = express();
server.use(express.json());
server.use('/', routes);

server.listen(4000, () => {
    console.log('Server listening at http://localhost:4000');
})