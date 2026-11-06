
const API_URL = "http://127.0.0.1:8000";


// ==========================================
// 1. PAGE NAVIGATION
// ==========================================

function showPage(page) {

    document.getElementById("studentPage").classList.remove("active");
    document.getElementById("adminPage").classList.remove("active");

    document.getElementById("studentNav").classList.remove("active");
    document.getElementById("adminNav").classList.remove("active");

    if (page === "student") {

        document.getElementById("studentPage").classList.add("active");
        document.getElementById("studentNav").classList.add("active");

    } else {

        document.getElementById("adminPage").classList.add("active");
        document.getElementById("adminNav").classList.add("active");

        loadComplaints();
    }
}


// ==========================================
// 2. MESSAGE HANDLING
// ==========================================

function showMessage(elementId, message, type) {

    const element = document.getElementById(elementId);

    element.textContent = message;
    element.className = `message ${type}-message`;
}


// Escape HTML to prevent unsafe user content
function escapeHTML(value) {

    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[character]);

}


// ==========================================
// 3. STUDENT COMPLAINT SUBMISSION
// ==========================================

document.getElementById("complaintForm").addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const submitBtn = document.getElementById("submitBtn");
        const resultPanel = document.getElementById("resultPanel");

        const payload = {
            student_name:
                document.getElementById("studentName").value.trim() || null,

            location:
                document.getElementById("location").value.trim(),

            description:
                document.getElementById("description").value.trim()
        };

        submitBtn.disabled = true;
        submitBtn.textContent = "Processing with AI...";

        resultPanel.style.display = "none";

        showMessage(
            "formMessage",
            "Your complaint is being analyzed by CampusFix AI agents...",
            "success"
        );

        try {

            const response = await fetch(`${API_URL}/api/complaints`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)

            });

            const data = await response.json();

            if (!response.ok || !data.success) {

                throw new Error(
                    data.detail?.error ||
                    data.detail?.message ||
                    data.error ||
                    data.message ||
                    "Unable to process complaint."
                );

            }

            const ticket = data.ticket || {};
            const triage = data.triage || {};

            document.getElementById("ticketId").textContent =
                ticket.ticket_id || "Not available";

            document.getElementById("ticketDetails").innerHTML = `

                <div class="detail-item">
                    <small>Category</small>
                    <strong>
                        ${escapeHTML(ticket.category || triage.category || "Pending")}
                    </strong>
                </div>

                <div class="detail-item">
                    <small>Priority</small>
                    <strong>
                        ${escapeHTML(ticket.priority || "Pending")}
                    </strong>
                </div>

                <div class="detail-item">
                    <small>Department</small>
                    <strong>
                        ${escapeHTML(ticket.department || "Pending")}
                    </strong>
                </div>

                <div class="detail-item">
                    <small>Status</small>
                    <strong>
                        ${escapeHTML(ticket.status || "Pending")}
                    </strong>
                </div>

            `;

            resultPanel.style.display = "block";

            // Display duplicate warning if detected
            if (data.duplicate_check?.duplicate_found === true) {

                const warning = document.createElement("p");

                warning.className = "warning";

                warning.textContent =
                    "Potential duplicate complaint detected. Flagged for admin review.";

                document.getElementById("ticketDetails")
                    .appendChild(warning);

            }

            showMessage(
                "formMessage",
                "Complaint submitted successfully! Your ticket has been generated.",
                "success"
            );

            document.getElementById("complaintForm").reset();

        }

        catch (error) {

            console.error("Complaint submission error:", error);

            showMessage(
                "formMessage",
                error.message.includes("Failed to fetch")
                    ? "Cannot connect to backend. Check whether FastAPI is running."
                    : error.message,
                "error"
            );

        }

        finally {

            submitBtn.disabled = false;
            submitBtn.textContent = "Submit Complaint";

        }

    }
);


// ==========================================
// 4. ADMIN DASHBOARD
// ==========================================

async function loadComplaints() {

    const tableBody = document.getElementById("complaintsTable");

    tableBody.innerHTML = `
        <tr>
            <td colspan="7">Loading complaints...</td>
        </tr>
    `;

    try {

        const response = await fetch(`${API_URL}/api/complaints`);

        const data = await response.json();

        if (!response.ok || !data.success) {

            throw new Error(
                data.detail?.error ||
                data.detail?.message ||
                data.error ||
                "Failed to load complaints."
            );

        }

        const complaints = data.tickets || [];

        // Update dashboard statistics

        document.getElementById("totalCount").textContent =
            complaints.length;

        document.getElementById("highCount").textContent =
            complaints.filter(c =>
                (c.priority || "").toLowerCase() === "high"
            ).length;

        document.getElementById("mediumCount").textContent =
            complaints.filter(c =>
                (c.priority || "").toLowerCase() === "medium"
            ).length;

        document.getElementById("lowCount").textContent =
            complaints.filter(c =>
                (c.priority || "").toLowerCase() === "low"
            ).length;


        // Empty dashboard

        if (complaints.length === 0) {

            tableBody.innerHTML = `
                <tr>
                    <td colspan="7">
                        No complaints have been submitted yet.
                    </td>
                </tr>
            `;

            showMessage(
                "adminMessage",
                "Dashboard loaded successfully.",
                "success"
            );

            return;

        }


        // Generate complaint table

        tableBody.innerHTML = complaints.map(complaint => {

            const currentStatus = complaint.status || "Pending";

            const statuses = [
                "Pending",
                "Approved",
                "Rejected",
                "In Progress",
                "Resolved"
            ];

            const options = statuses.map(status => `

                <option
                    value="${status}"
                    ${currentStatus === status ? "selected" : ""}>
                    ${status}
                </option>

            `).join("");

            return `

                <tr>

                    <td>
                        ${escapeHTML(complaint.ticket_id)}
                    </td>

                    <td>
                        ${escapeHTML(complaint.description)}
                    </td>

                    <td>
                        ${escapeHTML(complaint.location)}
                    </td>

                    <td>
                        ${escapeHTML(complaint.priority || "Pending")}
                    </td>

                    <td>
                        ${escapeHTML(complaint.department || "Pending")}
                    </td>

                    <td>
                        <span class="status-badge">
                            ${escapeHTML(currentStatus)}
                        </span>
                    </td>

                    <td>

                        <select class="status-select">
                            ${options}
                        </select>

                        <button
                            class="primary-btn update-status-btn"
                            type="button"
                            data-ticket-id="${escapeHTML(complaint.ticket_id)}">
                            Update
                        </button>

                    </td>

                </tr>

            `;

        }).join("");


        // Attach status update events

        tableBody.querySelectorAll(".update-status-btn")
            .forEach(button => {

                button.addEventListener("click", function () {

                    const row = this.closest("tr");

                    const selectedStatus =
                        row.querySelector(".status-select").value;

                    const ticketId =
                        this.dataset.ticketId;

                    updateComplaintStatus(ticketId, selectedStatus, this);

                });

            });


        showMessage(
            "adminMessage",
            "Complaints loaded successfully.",
            "success"
        );

    }

    catch (error) {

        console.error("Dashboard error:", error);

        tableBody.innerHTML = `
            <tr>
                <td colspan="7">
                    Unable to load complaints.
                </td>
            </tr>
        `;

        showMessage(
            "adminMessage",
            error.message,
            "error"
        );

    }

}


// ==========================================
// 5. ADMIN STATUS MANAGEMENT
// ==========================================

async function updateComplaintStatus(ticketId, newStatus, button) {

    if (!ticketId) {

        showMessage(
            "adminMessage",
            "Invalid ticket ID.",
            "error"
        );

        return;

    }

    const confirmed = window.confirm(
        `Are you sure you want to change ticket ${ticketId} to ${newStatus}?`
    );

    if (!confirmed) return;

    button.disabled = true;
    button.textContent = "Updating...";

    try {

        const response = await fetch(
            `${API_URL}/api/complaints/${encodeURIComponent(ticketId)}/status`,
            {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: newStatus
                })

            }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {

            throw new Error(
                data.detail?.error ||
                data.detail?.message ||
                data.detail ||
                data.error ||
                "Status update failed."
            );

        }

        showMessage(
            "adminMessage",
            `Ticket ${ticketId} updated to ${newStatus}.`,
            "success"
        );

        // Refresh dashboard after successful update
        await loadComplaints();

    }

    catch (error) {

        console.error("Status update error:", error);

        showMessage(
            "adminMessage",
            error.message,
            "error"
        );

        button.disabled = false;
        button.textContent = "Update";

    }

}


// ==========================================
// 6. INITIALIZE APPLICATION
// ==========================================

showPage("student");
