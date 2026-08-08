/**
 * AI Career Connect - Main JavaScript
 * =====================================
 * Shared utilities and initialization logic.
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("AI Career Connect loaded.");

    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll(".alert-dismissible").forEach((alert) => {
        setTimeout(() => {
            const closeBtn = alert.querySelector(".btn-close");
            if (closeBtn) closeBtn.click();
        }, 5000);
    });
});

/**
 * Helper: POST JSON to an endpoint and return parsed response.
 */
async function postJSON(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return response.json();
}

/**
 * Helper: GET JSON from an endpoint.
 */
async function getJSON(url) {
    const response = await fetch(url);
    return response.json();
}
