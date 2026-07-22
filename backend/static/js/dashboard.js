async function loadDashboard() {

    try {

        const response = await fetch("/dashboard_data");
        const data = await response.json();

        // Dashboard Cards
        document.getElementById("totalResume").innerText = data.total;
        document.getElementById("avgScore").innerText = data.average;
        document.getElementById("highestScore").innerText = data.highest;

        // Recent Upload Table
        let rows = "";

        data.recent.forEach(item => {

            rows += `
            <tr>
                <td>${item.name}</td>
                <td>${item.score}</td>
                <td>${item.date}</td>
            </tr>
            `;

        });

        document.querySelector("#recentTable tbody").innerHTML = rows;

        // Chart
        const ctx = document.getElementById("scoreChart").getContext("2d");

        new Chart(ctx, {

            type: "bar",

            data: {

                labels: data.recent.map(item => item.name),

                datasets: [{

                    label: "ATS Score",

                    data: data.recent.map(item => item.score),

                    borderWidth: 1

                }]

            },

            options: {

                responsive: true,

                scales: {

                    y: {

                        beginAtZero: true,

                        max: 100

                    }

                }

            }

        });

    }

    catch(err) {

        console.log("Dashboard Error:", err);

    }

}

window.onload = loadDashboard;