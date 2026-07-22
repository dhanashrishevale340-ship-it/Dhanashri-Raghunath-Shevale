document.getElementById("uploadForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const file = document.getElementById("resume").files[0];

    if (!file) {
        alert("Please select a resume.");
        return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    document.getElementById("message").innerHTML =
        "<h3 style='text-align:center;'>⏳ Analyzing Resume...</h3>";

    try {

        const response = await fetch("/upload_resume", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {

            document.getElementById("message").innerHTML = `
                <div class="result-card">
                    <h3 style="color:red;">${result.message}</h3>
                </div>
            `;
            return;
        }

        let output = `

        <div class="result-card">

            <h2 style="text-align:center;color:green;">
                ✅ ${result.message}
            </h2>

            <div class="score">
                ${result.score}/100
            </div>

            <hr>

            <div class="section">

                <h3>👤 Candidate Details</h3>

                <p><b>Name :</b> ${result.details.name || "-"}</p>

                <p><b>Email :</b> ${result.details.email || "-"}</p>

                <p><b>Phone :</b> ${result.details.phone || "-"}</p>

            </div>

            <hr>

            <div class="section">

                <h3>🎓 Education</h3>

                <ul>
        `;

        if (result.education.length > 0) {

            result.education.forEach(item => {
                output += `<li>${item}</li>`;
            });

        } else {

            output += "<li>No Education Found</li>";

        }

        output += `
                </ul>

            </div>

            <hr>

            <div class="section">

                <h3>💼 Experience</h3>

                <ul>
        `;

        if (result.experience.length > 0) {

            result.experience.forEach(item => {
                output += `<li>${item}</li>`;
            });

        } else {

            output += "<li>No Experience Found</li>";

        }

        output += `
                </ul>

            </div>

            <hr>

            <div class="section">

                <h3>📁 Projects</h3>

                <ul>
        `;

        if (result.projects.length > 0) {

            result.projects.forEach(item => {
                output += `<li>${item}</li>`;
            });

        } else {

            output += "<li>No Projects Found</li>";

        }

        output += `
                </ul>

            </div>

            <hr>

            <div class="section">

                <h3>🧠 Skills</h3>
        `;

        if (result.skills.length > 0) {

            result.skills.forEach(skill => {

                output += `<span class="skill">${skill}</span>`;

            });

        } else {

            output += "<p>No Skills Found</p>";

        }

        output += `

            </div>

            <hr>

            <div class="section">

                <h3>💼 Recommended Jobs</h3>
        `;

        if (result.jobs.length > 0) {

            result.jobs.forEach(job => {

                output += `

                <div class="job">

                    <h4>${job.title}</h4>

                    <p><b>Match :</b> ${job.match}%</p>

                    <p><b>Salary :</b> ${job.salary}</p>

                    <p><b>Matched Skills :</b> ${job.matched_skills.join(", ")}</p>

                </div>

                `;

            });

        } else {

            output += "<p>No Job Recommendation Available</p>";

        }

        output += `

            <hr>

            <div class="section">

                <h3>⭐ AI Suggestions</h3>

                <ul>
        `;

        if (result.suggestions.length > 0) {

            result.suggestions.forEach(item => {

                output += `<li>${item}</li>`;

            });

        } else {

            output += "<li>No Suggestions Available</li>";

        }

        output += `

                </ul>

            </div>

        </div>

        `;

        document.getElementById("message").innerHTML = output;

        document.getElementById("uploadForm").reset();

    }

    catch (error) {

        console.error(error);

        document.getElementById("message").innerHTML = `

            <div class="result-card">

                <h3 style="color:red;">

                    Something went wrong!

                </h3>

            </div>

        `;

    }

});