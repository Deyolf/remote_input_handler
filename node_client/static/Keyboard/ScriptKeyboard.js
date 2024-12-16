//intervals
a = setInterval(getVolume, 500);

const domainName = window.location.hostname;

console.log(domainName);

let ip = "192.168.178.89"
let port = ":"+"50000"
let socket= ip+port

var queue = [];

function sendBuffer(key) {
    console.log(key)
    fetch(`http://${socket}/receive_keycap`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keycap: key }),
    })
        .then(response => response.json())
        .then(response => {

        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function sendKeycap(key) {
    console.log(key)
    queue.push(key)
    fetch(`http://${socket}/receive_keycap`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keycap: key }),
    })
        .then(response => response.json())
        .then(response => {
            console.log(response)
            console.log(queue)
            //if (response.status == 200)
            //queue.shift(key)
            return true
        })
        .catch((error) => {
            console.error('Error:', error);
            console.log(queue)
            return false
        });
}

function sendKeycapHold(key) {
    console.log(key)
    fetch(`http://${socket}/receive_keycap_hold`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keycap: key }),
    })
        .then(response => response.json())
        .catch((error) => {
            console.error('Error:', error);
        });
}

function sendKeycapRelease(key) {
    console.log(key)
    fetch(`http://${socket}/receive_keycap_release`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keycap: key }),
    })
        .then(response => response.json())
        .catch((error) => {
            console.error('Error:', error);
        });
}

function updateVolume(voli) {
    vol = voli + '';
    console.log(vol)
    fetch(`http://${socket}/receive_volume`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ volume: vol }),
    })
        .then(response => response.json())
        .catch((error) => {
            console.error('Error:', error);
        });
}

function getVolume() {
    fetch(`http://${socket}/get_volume`, { method: 'GET' })
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta');
            }
            return response.json();
        })
        .then(data => {
            console.log("Volume corrente:", data.volume);
            volume = data.volume;
            document.getElementById("customRange").value = isNaN(parseInt(volume, 10)) ? 0 : parseInt(volume, 10);
            document.getElementById("customRange").innerHTML = volume;
        })
        .catch(error => {
            console.error('Errore:', error);
        });
}

function AltF4() {
    //alt tab
    sendKeycapHold('Alt')
    sendKeycap('f4')
    sendKeycapRelease('Alt')
}

function TskMgr() {
    //ctrl shift escape
    sendKeycapHold('Ctrl')
    sendKeycapHold('Shift')
    sendKeycap('Esc')
    sendKeycapRelease('Shift')
    sendKeycapRelease('Ctrl')
}

var promises = [];
var letters = [];
const input = document.getElementById('textInput');
input.addEventListener('input', () => {
    console.log(input.value)
    sendKeycap(input.value[0])
    input.value = input.value.slice(1);
})