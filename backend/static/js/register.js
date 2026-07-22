document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("registerForm");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const data = {

            full_name: document.getElementById("full_name").value,

            email: document.getElementById("email").value,

            password: document.getElementById("password").value

        };

        try {

            const response = await fetch("/register", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)

            });

            const result = await response.json();

            document.getElementById("message").innerHTML = result.message;

            if (response.status === 201) {

                form.reset();

            }

        } catch (err) {

            console.log(err);

            document.getElementById("message").innerHTML =
                "Server Error";

        }

    });

});