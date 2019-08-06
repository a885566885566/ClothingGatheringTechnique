const express = require('express');
const app = express();
const port = 11230;
app.use(express.static(__dirname + '/public'));
app.listen(port);
console.log('Server working')
