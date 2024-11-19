const socket = new WebSocket("ws://127.0.0.1:8000/ws/progress/");

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    document.getElementById("progress-bar").style.width = data.progress + "%";
    document.getElementById("progress-text").innerText = data.progress + "%";
};
