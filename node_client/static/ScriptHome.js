
function sendKeycap(key) {
    fetch('http://192.168.178.89:50000/receive_keycap', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keycap: key }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.message || data.error;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById("response").innerText = "Error sending the keycap!";
    });
}

function updateValue(){
    
}