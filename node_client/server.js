let hostname;
const port = process.env.PORT || 50050;

var express = require("express");
var fs = require("fs");
const path = require("path");

var app = express();

console.log('leggo il file');
hostname = fs.readFileSync("../ip.txt", 'utf8', (err, data) => {
    if (err) {
        console.log('Errore nella lettura del file:', err);
        return;
    }
    return data
});

app.use(express.static(path.join(__dirname, "static")));

function loadHomepage(req, res) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200)

    const filePath = path.join(__dirname, "static", "Homepage.html");
    res.write(fs.readFileSync(filePath, "utf-8"));

    res.end();
}

function loadKeyboard(req, res) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200)

    const filePath = path.join(__dirname, "static", "Keyboard/Keyboard.html");
    res.write(fs.readFileSync(filePath, "utf-8"));

    res.end();
}

function loadMouse(req, res) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200)

    const filePath = path.join(__dirname, "static", "Mouse/Mouse.html");
    res.write(fs.readFileSync(filePath, "utf-8"));

    res.end();
}

function diocane(req, res) {
    fetch(`http://${hostname}:500000/recive_mouse_move`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: { a },
    })
        .then(response => response.json())
        .then(response => {
            console.log(response)
            //if (response.status == 200)
            //queue.shift(key)
            return true
        })
        .catch((error) => {
            console.error('Error:', error);
            return false
        });
}
app.get("/recive_mouse_move/:a", (req, res) => diocane(req, res))
app.get("/", (req, res) => loadHomepage(req, res));
app.get("/homepage", (req, res) => loadHomepage(req, res));
app.get("/keyboard", (req, res) => loadKeyboard(req, res));
app.get("/mouse", (req, res) => loadMouse(req, res));

var server = app.listen(port, hostname, () => {
    console.log(`Express App running at http://${hostname}:${port}/`);
})