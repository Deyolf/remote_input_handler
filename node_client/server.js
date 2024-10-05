const hostname = '192.168.178.89';
const port = 50050;

var express = require("express");
var fs = require("fs");
const path = require("path");

var app = express();
app.use(express.static(path.join(__dirname, "static")));

app.get("/", function documentazione(req, res) {
    //req oggetto che descrive il richiedente
    //res oggetto per la gestione della risposta
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200)

    const filePath = path.join(__dirname, "static", "Homepage.html");
    res.write(fs.readFileSync(filePath, "utf-8"));

    res.end();
});

var server = app.listen(port, hostname, () => {
    console.log(`Express App running at http://${hostname}:${port}/`);
})