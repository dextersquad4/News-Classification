const https = await import('node:https');
const fs = await import('node:fs');
const cron = await imort('node-cron');
const { spawn } = require('child_process');

import { callEndpoints } from './routing.js';


const port = "3000";
const host = "0.0.0.0";
const cronExpression = '32 13 * * *';

const options = {
    key: fs.readFileSync('key.pem'),
    cert: fs.readFileSync('cert.pem'),
}

const server = https.createServer(options, (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8000');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end('<h1>Secure Node.js Server</h1><p>Your connection is secure!</p>');
    } else if (req.url.startsWith('/api/')) {
        const desiredEndpoint = req.url.replace('/api/', '');
        callEndpoints(desiredEndpoint).then(endResponse=>{
            res.writeHead(endResponse.Status, { 'Content-Type': 'text/plain' });
            res.end(JSON.stringify(endResponse));
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
    }
});

server.listen(port, host, () => {
    const {address, port} = server.address();
    console.log(`We are running on https://${address}:${port}`);
})

cron.schedule(cronExpression, () => {
    const pythonProcess = spawn('python', ["schedule.py"])
    pythonProcess.on('close', (code) => {
        console.log(`Scheduler ended on ${code}`);
    })
})
