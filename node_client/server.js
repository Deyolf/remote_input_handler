let hostname ;
const port = 50050;

var express = require("express");
var fs = require("fs");
const path = require("path");

var app = express();

console.log('leggo il file');
hostname= fs.readFileSync("../ip.txt", 'utf8', (err, data) => {
    if (err) {
        console.log('Errore nella lettura del file:', err);
        return;
    }
    return data
});

app.use(express.static(path.join(__dirname, "static")));

app.get("/", function Homepage(req, res) {
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