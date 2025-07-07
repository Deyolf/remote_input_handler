// Connessione WebSocket
const ip = window.location.hostname;
const port = "50050"; // Nuova porta WebSocket
const ws = new WebSocket(`ws://${ip}:${port}/ws`);

// Variabile volume
let volume = 0;

// Apertura connessione
ws.onopen = () => {
  console.log("🔌 WebSocket connesso");
};

ws.onerror = (error) => {
  console.error("Errore WebSocket:", error);
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("📨 Messaggio ricevuto:", data);

  if (data.volume !== undefined) {
    volume = data.volume;
    const range = document.getElementById("customRange");
    if (range) {
      range.value = isNaN(parseInt(volume, 10)) ? 0 : parseInt(volume, 10);
      range.innerHTML = volume;
    }
  }
};

// 🎹 Invio tasti
function sendKeycap(key) {
  ws.send(JSON.stringify({
    type: "keycap",
    action: "press",
    keycap: key
  }));
}

function sendKeycapHold(key) {
  ws.send(JSON.stringify({
    type: "keycap",
    action: "hold",
    keycap: key
  }));
}

function sendKeycapRelease(key) {
  ws.send(JSON.stringify({
    type: "keycap",
    action: "release",
    keycap: key
  }));
}

// 🔊 Volume
function updateVolume(voli) {
  ws.send(JSON.stringify({
    type: "volume",
    action: "set",
    volume: voli
  }));
}

function getVolume() {
  ws.send(JSON.stringify({
    type: "volume",
    action: "get"
  }));
}

// 💻 Macro
function AltF4() {
  sendKeycapHold("Alt");
  sendKeycap("f4");
  sendKeycapRelease("Alt");
}

function TskMgr() {
  sendKeycapHold("Ctrl");
  sendKeycapHold("Shift");
  sendKeycap("Esc");
  sendKeycapRelease("Shift");
  sendKeycapRelease("Ctrl");
}

// 🔤 Invio input da text field
const input = document.getElementById("textInput");
if (input) {
  input.addEventListener("input", () => {
    console.log(input.value);
    sendKeycap(input.value[0]);
    input.value = input.value.slice(1);
  });
}