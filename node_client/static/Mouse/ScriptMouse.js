const ip = window.location.hostname;
const port = ":" + "50000";
const apisocket = ip + port;

const socket = new WebSocket(`ws://${ip}:8765`);

socket.onopen = () => console.log("WebSocket connected.");
socket.onclose = () => console.log("WebSocket disconnected.");
socket.onmessage = (event) => console.log(event.data);

function sendClick(button) {
  fetch(`http://${apisocket}/recive_mouse_click`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ btn: button }),
  })
    .then((res) => res.text())
    .then(console.log)
    .catch(console.error);
}

document.addEventListener("click", function (event) {
  if (!event.target.closest("button")) {
    const realWidth = window.innerWidth;
    const realHeight = window.innerHeight;

    const x = event.clientX;
    const y = event.clientY;

    const mappedX = Math.round((x / realWidth) * 1920);
    const mappedY = Math.round((y / realHeight) * 1080);

    document.getElementById("mouseCoords").value = `X: ${mappedX}, Y: ${mappedY}`;
  }
});
