var canvas = document.getElementById("canvas");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var ctx = canvas.getContext("2d");

var mouseLocations = new Map();

var socket = io();
socket.on("connection", function(msg) {
	console.log(msg)
});

function update() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	for(let entry of mouseLocations) {
		ctx.beginPath();
		ctx.arc(entry[1][0], entry[1][1], 3, 0, 2 * Math.PI);
		ctx.fill();
		ctx.fillText(entry[0], entry[1][0] + 5, entry[1][1] - 5);
	}
}

socket.on("mouse", function(msg) {
	mouseLocations.set(msg.username, [msg.x, msg.y]);
	update();
});

function onMouseDown(ev) {
}

function onMouseUp(ev) {
}

function onMouseMove(ev) {
	socket.emit("mousePosition", {"x": ev.clientX, "y": ev.clientY});
}

canvas.addEventListener("pointerdown", onMouseDown);
canvas.addEventListener("pointerup", onMouseUp);
canvas.addEventListener("pointermove", onMouseMove);
