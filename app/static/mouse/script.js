const ip = window.location.hostname;
const port = ":" + "50050";
const apisocket = ip + port;

const socket = new WebSocket(`ws://${ip}:50050/ws`);

document.getElementById("left").style = "display: none"
document.getElementById("right").style = "display: none"

let a = true;

const realWidth = window.innerWidth;
const realHeight = window.innerHeight;

let x, y;
let mappedX, mappedY;
let timeout;

socket.onopen = () => console.log("WebSocket connected.");
socket.onclose = () => console.log("WebSocket disconnected.");
socket.onmessage = (event) => console.log(event.data);

function sendClick(button) {
  a = true;
  document.getElementById("left").style = "display: none"
  document.getElementById("right").style = "display: none"
  fetch(`http://${apisocket}/recive_mouse_click`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ btn: button }),
  })
    .then((res) => res.text())
    .then(console.log)
    .catch(console.error);
}

/*document.addEventListener("click", function (event) {
  if (!event.target.closest("button")) {
    const realWidth = window.innerWidth;
    const realHeight = window.innerHeight;

    const x = event.clientX;
    const y = event.clientY;

    const mappedX = Math.round((x / realWidth) * 1920);
    const mappedY = Math.round((y / realHeight) * 1080);

    document.getElementById("mouseCoords").value = `X: ${mappedX}, Y: ${mappedY}`;
  }
});*/

document.addEventListener("click", function (event) {
  clearTimeout(timeout);
  if (!a){
    document.getElementById("left").style = "display: block"
    document.getElementById("right").style = "display: block"
  }
});

document.addEventListener("mousemove", function (event) {
  if (a) {
    a = false;
    x = event.clientX;
    y = event.clientY;

    let mappedX = Math.round((x / realWidth) * 1920);
    let mappedY = Math.round((y / realHeight) * 1080);

    socket.send(`${mappedX},${mappedY}`);
    timeout = setTimeout(() => {
      a = true;
    }, 100);
  }
});
