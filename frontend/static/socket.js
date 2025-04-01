const socket = new WebSocket("ws://mc.eyangch.me:8000/ws");
const token = localStorage.getItem("token")

socket.addEventListener("open", (event) => {
    socket.send(token);
});

socket.addEventListener("message", (event) => {
    if(event.data === "OK"){
        document.getElementById("logged-in").hidden = false;
    }else{
        document.getElementById("not-login").hidden = false;
    }
});