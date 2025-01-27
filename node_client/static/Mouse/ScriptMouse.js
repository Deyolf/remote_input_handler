//Nothing for u here
//intervals
const ip = window.location.hostname;

console.log(ip);

let port = ":" + "50000"
let socket = ip + port

window.addEventListener('load', () => {

    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    resize();

    //Gestione movimento tramite mouse
    document.addEventListener('mousedown', startDrawing);
    document.addEventListener('mouseup', stopDrawing);
    document.addEventListener('mousemove', Draw);
    
    //Gestione movimento tramite touchscreen
    document.addEventListener('touchstart', startDrawing);
    document.addEventListener('touchend', stopDrawing);
    document.addEventListener('touchcancel', stopDrawing);
    document.addEventListener('touchmove', Draw);
    window.addEventListener('resize', resize);

    document.getElementById("x_coordinate").innerText = 0;
    document.getElementById("y_coordinate").innerText = 0;
    document.getElementById("speed").innerText = 0;
    document.getElementById("angle").innerText = 0;
});

function move(x, y, speed, angle) {
    speed = Math.floor(speed / 15)
    console.log(speed)
    console.log(x)
    console.log(y)
    let x_movement = Math.floor(speed * Math.cos(angle));
    let y_movement = Math.floor(speed * Math.sin(angle));
    console.log(`x_movement: ${x_movement}`)
    console.log(`y_movement: ${y_movement}`)
    sendMouse(x_movement, y_movement)

}

var width, height, radius, x_orig, y_orig;
//Funzione che gestisce il ridimensionamento
function resize() {
    width = window.innerWidth;
    radius = 120;
    height = radius * 6.5;
    ctx.canvas.width = width;
    ctx.canvas.height = height;
    background();
    joystick(width / 2, height / 3);
}

//Posizionamento e creazione BASE joystick  
function background() {
    x_orig = width / 2;
    y_orig = height / 3;

    ctx.beginPath();
    ctx.arc(x_orig, y_orig, radius + 20, 0, Math.PI * 2, true); //disegna cerchio
    ctx.fillStyle = '#ECE5E5';
    ctx.fill();
}

//Creazione del joystick per il movimento
function joystick(width, height) {
    ctx.beginPath();
    ctx.arc(width, height, radius, 0, Math.PI * 2, true); //disegna joystick
    ctx.fillStyle = '#F08080';
    ctx.fill();
    ctx.strokeStyle = '#F6ABAB';
    ctx.lineWidth = 8;
    ctx.stroke();
}

let coord = { x: 0, y: 0 };
let paint = false;
//Otteniamo la posizione assoluta del mouse
function getPosition(event) {
    e = window.event || e;
    var mouse_x = e.clientX || event.touches[0].clientX; //touches[0] prende i dati del primo tocco 
    var mouse_y = e.clientY || event.touches[0].clientY; //client X e Y prendono la posizione X/Y assoluta del mouse o del tocco
    coord.x = mouse_x - canvas.offsetLeft;               //Otteniamo la posizione effettiva
    coord.y = mouse_y - canvas.offsetTop;
}

//Tramite teorema di pitagora troviamo la posizione del mouse rispetto alla base
function is_it_in_the_circle() {
    var current_radius = Math.sqrt(Math.pow(coord.x - x_orig, 2) + Math.pow(coord.y - y_orig, 2));
    if (radius >= current_radius) return true
    else return false
}

function startDrawing(event) {
    paint = true;
    getPosition(event);
    if (is_it_in_the_circle()) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        background();
        joystick(coord.x, coord.y);
        intervallo_che_vuole_Fabio = setInterval(Draw, 7);
        //Draw();
    }
}

function stopDrawing() {
    paint = false;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    background();
    joystick(width / 2, height / 3);
    document.getElementById("x_coordinate").innerText = 0;
    document.getElementById("y_coordinate").innerText = 0;
    document.getElementById("speed").innerText = 0;
    document.getElementById("angle").innerText = 0;
    clearInterval(intervallo_che_vuole_Fabio);
}

function sendMouse(x_movement, y_movement) {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "x_movement": x_movement,
        "y_movement": y_movement
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch(`http://${socket}/receive_mouse_move`, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}

function sendClick(button) {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "btn": button
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch(`http://${socket}/recive_mouse_click`, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}

function Draw(event) {

    if (paint) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        background();
        var angle_in_degrees, x, y, speed;
        var angle = Math.atan2((coord.y - y_orig), (coord.x - x_orig));

        if (Math.sign(angle) == -1) {
            angle_in_degrees = Math.round(-angle * 180 / Math.PI);
        }
        else {
            angle_in_degrees = Math.round(360 - angle * 180 / Math.PI);
        }

        if (is_it_in_the_circle()) {
            joystick(coord.x, coord.y);
            x = coord.x;
            y = coord.y;
        }
        else {
            x = radius * Math.cos(angle) + x_orig;
            y = radius * Math.sin(angle) + y_orig;
            joystick(x, y);
        }

        getPosition(event);

        var speed = Math.round(100 * Math.sqrt(Math.pow(x - x_orig, 2) + Math.pow(y - y_orig, 2)) / radius);

        var x_relative = Math.round(x - x_orig);
        var y_relative = Math.round(y - y_orig);

        document.getElementById("x_coordinate").innerText = x_relative;
        document.getElementById("y_coordinate").innerText = y_relative;
        document.getElementById("speed").innerText = speed;
        document.getElementById("angle").innerText = angle_in_degrees;

        move(x_relative, y_relative, speed, angle);

        //send( x_relative,y_relative,speed,angle_in_degrees);
    }
} 