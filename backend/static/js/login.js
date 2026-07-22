document.getElementById("loginForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const response = await fetch("/login",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("message").innerHTML=result.message;

    if(response.status==200){

        window.location.href="/upload_page";

    }

});