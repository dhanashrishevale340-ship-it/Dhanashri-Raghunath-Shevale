// ===========================
// Format Resume Data
// ===========================

function formatData(data) {

    if (!data) return "N/A";

    try {

        let arr = JSON.parse(data);

        if (Array.isArray(arr)) {

            return arr
                .map(item => "• " + item)
                .join("<br>");

        }

        return arr;

    } catch (e) {

        return data
            .replace(/\\u2022/g, "•")
            .replace(/\\u2013/g, "-")
            .replace(/\\"/g, "")
            .replace(/"/g, "")
            .replace(/\[/g, "")
            .replace(/\]/g, "")
            .replace(/,/g, "<br>• ")
            .replace(/\n/g, "<br>");

    }

}


// ===========================
// Load Resume History
// ===========================

async function loadHistory() {

    const response = await fetch("/history");
    const data = await response.json();

    let rows = "";

    data.forEach(item => {

        rows += `
        <tr>

            <td>${item.id}</td>

            <td>${item.candidate_name}</td>

            <td>${item.email}</td>

            <td>${item.phone}</td>

            <td>${item.score}</td>

            <td>${item.uploaded_at}</td>

            <td>
                <button class="view-btn"
                    onclick="viewResume(${item.id})">
                    👁 View
                </button>
            </td>

            <td>
                <button class="delete-btn"
                    onclick="deleteResume(${item.id})">
                    🗑 Delete
                </button>
            </td>

            <td>
                <a href="/download_report/${item.filename}.pdf">
                    <button class="download-btn">
                        📄 Download PDF
                    </button>
                </a>
            </td>

        </tr>
        `;

    });

    document.querySelector("#historyTable tbody").innerHTML = rows;

}


// ===========================
// View Resume
// ===========================

async function viewResume(id) {

    try {

        const response = await fetch(`/resume/${id}`);
        const data = await response.json();

        if (!response.ok) {

            alert(data.message);
            return;

        }

        document.getElementById("resumeDetails").innerHTML = `

            <div class="detail">
                <strong>👤 Candidate Name</strong><br>
                ${data.name}
            </div>

            <div class="detail">
                <strong>📧 Email</strong><br>
                ${data.email}
            </div>

            <div class="detail">
                <strong>📱 Phone</strong><br>
                ${data.phone}
            </div>

            <div class="detail">
                <strong>🎓 Education</strong><br>
                ${formatData(data.education)}
            </div>

            <div class="detail">
                <strong>💼 Experience</strong><br>
                ${formatData(data.experience)}
            </div>

            <div class="detail">
                <strong>🚀 Projects</strong><br>
                ${formatData(data.projects)}
            </div>

            <div class="detail">
                <strong>🛠 Skills</strong><br>
                ${formatData(data.skills)}
            </div>

            <div class="detail">
                <strong>📊 ATS Score</strong><br>
                ${data.score}
            </div>

            <div class="detail">
                <strong>📅 Uploaded At</strong><br>
                ${data.uploaded_at}
            </div>

        `;

        document.getElementById("resumeModal").style.display = "block";

    }

    catch (error) {

        console.error(error);
        alert("Unable to load resume details.");

    }

}


// ===========================
// Close Modal
// ===========================

function closeModal() {

    document.getElementById("resumeModal").style.display = "none";

}


// ===========================
// Close Modal When Click Outside
// ===========================

window.onclick = function(event) {

    const modal = document.getElementById("resumeModal");

    if (event.target === modal) {

        modal.style.display = "none";

    }

};


// ===========================
// Delete Resume
// ===========================

async function deleteResume(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this resume?"
    );

    if (!confirmDelete) return;

    const response = await fetch(`/delete_resume/${id}`, {

        method: "DELETE"

    });

    const result = await response.json();

    alert(result.message);

    loadHistory();

}


// ===========================
// Search Resume
// ===========================

function searchResume() {

    const input = document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    const rows = document.querySelectorAll(
        "#historyTable tbody tr"
    );

    rows.forEach(row => {

        const name = row.cells[1].innerText.toLowerCase();

        const email = row.cells[2].innerText.toLowerCase();

        if (
            name.includes(input) ||
            email.includes(input)
        ) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });

}


// ===========================
// Load History
// ===========================

window.onload = loadHistory;