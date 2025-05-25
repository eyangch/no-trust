const socket = new WebSocket("ws://mc.eyangch.me:8000/ws");
const token = localStorage.getItem("token");

function enable_single(set, enable){
    for(let i = 0; i < set.length; i++){
        document.getElementById(set[i]).hidden = true;
    }
    if(enable !== null){
        document.getElementById(enable).hidden = false;
    }
}

const login_set = ["logged-in", "not-login"];
const pw_change_set = ["pass-no-match", "pass-change-fail", "pass-changed"];

socket.addEventListener("open", (event) => {
    socket.send(JSON.stringify({
        type: "auth",
        token: token
    }));
});

socket.addEventListener("message", (event) => {
    data = JSON.parse(event.data);
    if(data.type === "auth"){
        if(data.status === "OK"){
            enable_single(login_set, "logged-in");
            document.getElementById("user").textContent = data.msg;
            socket.send(JSON.stringify({
                type: "get-ports"
            }));
        }else{
            enable_single(login_set, "not-login");
        }
    }
    if(data.type === "change-pw"){
        enable_single(pw_change_set, null);
        if(data.status === "OK"){
            enable_single(pw_change_set, "pass-changed");
        }else{
            enable_single(pw_change_set, "pass-change-fail");
        }
    }
    if(data.type === "get-ports"){
        if(data.status === "OK"){
            const table = document.getElementById("port-table-body");
            table.innerHTML = "";
            for(let i = 0; i < data.msg.length; i++){
                const port_row = table.insertRow();
                const proxy_port_cell = port_row.insertCell();
                const hidden_port_cell = port_row.insertCell();
                proxy_port_cell.textContent = data.msg[i][0];
                hidden_port_cell.textContent = data.msg[i][1];
            }
        }
    }
    if(data.type === "new-port"){
        if(data.status === "OK"){
            socket.send(JSON.stringify({
                type: "get-ports"
            }));
        }
    }
});

function logout(){
    localStorage.removeItem("token");
    window.location.reload();
}

function change_pass(){
    const pass1 = document.getElementById("new-password-1").value;
    const pass2 = document.getElementById("new-password-2").value;
    if(pass1 !== pass2){
        enable_single(pw_change_set, "pass-no-match");
    }else{
        document.getElementById("pass-no-match").hidden = true;
        socket.send(JSON.stringify({
            type: "change-pw",
            password: pass1
        }));
    }
}

function add_port(){
    const proxy_port = parseInt(document.getElementById("new-proxy-port").value);
    const hidden_port = parseInt(document.getElementById("new-hidden-port").value);
    socket.send(JSON.stringify({
        "type": "new-port",
        "proxy_port": proxy_port,
        "hidden_port": hidden_port
    }));
}