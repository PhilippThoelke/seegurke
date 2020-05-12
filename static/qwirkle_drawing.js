var canvas = document.getElementById("canvas");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var ctx = canvas.getContext("2d");

var socket = io();
socket.on("connection", function(msg) {
	console.log(msg)
});

socket.on("mouse", function(msg) {
	console.log(msg)
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.beginPath();
	ctx.arc(msg.x, msg.y, 3, 0, 2 * Math.PI);
	ctx.fill();
	ctx.fillText(msg.username, msg.x + 5, msg.y - 5);
});

function onMouseDown(ev) {
}

function onMouseUp(ev) {
}

function onMouseMove(ev) {
	socket.emit("mousePosition", {"x": ev.clientX, "y": ev.clientY})
}

canvas.addEventListener("pointerdown", onMouseDown)
canvas.addEventListener("pointerup", onMouseUp)
canvas.addEventListener("pointermove", onMouseMove)
