/**
 * AI Career Connect - Career JavaScript
 * ========================================
 * Handles career profile creation and roadmap generation.
 */

document.addEventListener("DOMContentLoaded", () => {
    // ── Create Profile ──
    const form = document.getElementById("profile-form");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const data = {
                current_role: document.getElementById("current_role").value,
                desired_role: document.getElementById("desired_role").value,
                experience_years: parseInt(document.getElementById("experience_years").value),
                skills: document.getElementById("skills").value,
                education: document.getElementById("education").value,
            };

            const result = await postJSON("/api/career/profile", data);
            alert(`Profile created: ${result.current_role} → ${result.desired_role}`);
            location.reload();
        });
    }

    // ── Generate Roadmap ──
    document.querySelectorAll(".btn-generate-roadmap").forEach((btn) => {
        btn.addEventListener("click", async () => {
            const profileId = btn.dataset.profileId;
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Generating...';

            try {
                const result = await postJSON(`/api/career/roadmap/${profileId}`, {});
                alert("Roadmap generated successfully!");
                location.reload();
            } catch (err) {
                alert("Failed to generate roadmap.");
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-magic me-1"></i>Generate New Roadmap';
            }
        });
    });

    // ── Resume Analyzer ──
    const resumeForm = document.getElementById("resume-form");
    if (resumeForm) {
        resumeForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const btn = document.getElementById("btn-analyze-resume");
            const originalText = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Analyzing...';

            try {
                const data = { resume_text: document.getElementById("resume_text").value };
                const result = await postJSON("/api/career/resume/analyze", data);
                
                document.getElementById("resume-empty-state").classList.add("d-none");
                document.getElementById("resume-feedback-container").classList.remove("d-none");
                document.getElementById("resume-feedback").textContent = result.analysis;
            } catch (err) {
                alert("Failed to analyze resume.");
            } finally {
                btn.disabled = false;
                btn.innerHTML = originalText;
            }
        });
    }

    // ── Interview Question Analyzer ──
    const interviewForm = document.getElementById("interview-form");
    if (interviewForm) {
        interviewForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const btn = document.getElementById("btn-generate-questions");
            const originalText = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Generating...';

            try {
                const data = { 
                    role: document.getElementById("interview_role").value,
                    skills: document.getElementById("interview_skills").value
                };
                const result = await postJSON("/api/career/interview/questions", data);
                
                document.getElementById("interview-empty-state").classList.add("d-none");
                document.getElementById("interview-questions-container").classList.remove("d-none");
                document.getElementById("interview-questions").textContent = result.questions;
            } catch (err) {
                alert("Failed to generate questions.");
            } finally {
                btn.disabled = false;
                btn.innerHTML = originalText;
            }
        });
    }
});
