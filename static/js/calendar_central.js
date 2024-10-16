// Server-side JavaScript code (Node.js with Express.js)
//const express = require('express');
const app = express();
const port = 3000;

// Define a variable on the server
const serverVariable = 'Hello from server!';

// Define a route to handle the client's request
app.get('/getData', (req, res) => {
    // Send the variable's value as part of the HTTP response
    res.send({ data: serverVariable });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
