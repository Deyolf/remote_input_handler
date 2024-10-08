//intervals
a = setInterval(getVolume, 500);


function sendKeycap(key) {
    console.log(key)
    fetch('http://192.168.178.89:50000/receive_keycap', {
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
    fetch('http://192.168.178.89:50000/receive_volume', {
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
    fetch('http://192.168.178.89:50000/get_volume')
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
            sdocument.getElementById("customRange").innerHTML=volume;
        })
        .catch(error => {
            console.error('Errore:', error);
        });
}