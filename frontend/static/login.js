async function login(){
    let user = document.getElementById("user").value;
    let password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        body: JSON.stringify({
            user: user,
            password: password
        })
    });

    const json = await(response.json());
    console.log(json);

    if(json.status === "OK"){
        localStorage.setItem("token", json.token);
        window.location.href = '/';
    }else{
        document.getElementById("incorrect").hidden = false;
    }
}