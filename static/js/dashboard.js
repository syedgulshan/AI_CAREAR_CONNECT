/**
 * AI Career Connect - Dashboard JavaScript
 * ==========================================
 * Fetches activity data and renders the Chart.js bar chart.
 */

document.addEventListener("DOMContentLoaded", async () => {
    const canvas = document.getElementById("activityChart");
    if (!canvas) return;

    try {
        const data = await getJSON("/api/dashboard/activity?days=7");

        const labels = data.map((d) => d.date);
        const counts = data.map((d) => d.count);

        new Chart(canvas, {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Messages",
                    data: counts,
                    backgroundColor: "rgba(13, 110, 253, 0.6)",
                    borderColor: "rgba(13, 110, 253, 1)",
                    borderWidth: 1,
                    borderRadius: 6,
                }],
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } },
                },
                plugins: {
                    legend: { display: false },
                },
            },
        });
    } catch (err) {
        console.error("Failed to load activity chart:", err);
    }
});
