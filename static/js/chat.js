/**
 * AI Career Connect - Chat JavaScript
 * ======================================
 * Handles conversation CRUD, message sending,
 * and voice input via the Web Speech API.
 */

let currentConvId = null;

document.addEventListener("DOMContentLoaded", () => {
    // ── New Chat button ──
    const btnNewChat = document.getElementById("btn-new-chat");
    if (btnNewChat) {
        btnNewChat.addEventListener("click", async () => {
            const data = await postJSON("/api/chat/conversations", {
                title: "New Conversation",
            });
            currentConvId = data.id;
            addConversationToList(data.id, data.title);
            clearChat();
        });
    }

    // ── Conversation list click ──
    document.getElementById("conversation-list")?.addEventListener("click", async (e) => {
        const item = e.target.closest("[data-conv-id]");
        if (!item) return;
        currentConvId = parseInt(item.dataset.convId);
        await loadMessages(currentConvId);
    });

    // ── Send message ──
    const chatForm = document.getElementById("chat-form");
    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const input = document.getElementById("chat-input");
            const message = input.value.trim();
            if (!message || !currentConvId) return;

            appendMessage("user", message);
            input.value = "";

            const data = await postJSON(
                `/api/chat/conversations/${currentConvId}/send`,
                { message, is_voice: false }
            );
            appendMessage("assistant", data.ai_response.content);
        });
    }

    // ── Voice Input (Web Speech API) ──
    const btnVoice = document.getElementById("btn-voice");
    if (btnVoice && "webkitSpeechRecognition" in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = false;

        btnVoice.addEventListener("click", () => {
            btnVoice.classList.toggle("recording");
            recognition.start();
        });

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById("chat-input").value = transcript;
            btnVoice.classList.remove("recording");
        };

        recognition.onerror = () => btnVoice.classList.remove("recording");
        recognition.onend = () => btnVoice.classList.remove("recording");
    }
});

// ── Helpers ──

async function loadMessages(convId) {
    const messages = await getJSON(`/api/chat/conversations/${convId}/messages`);
    clearChat();
    messages.forEach((m) => appendMessage(m.role, m.content));
}

function appendMessage(role, content) {
    const container = document.getElementById("chat-messages");
    const div = document.createElement("div");
    div.className = `message-bubble message-${role} d-flex`;
    div.textContent = content;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function clearChat() {
    const container = document.getElementById("chat-messages");
    if (container) container.innerHTML = "";
}

function addConversationToList(id, title) {
    const list = document.getElementById("conversation-list");
    const a = document.createElement("a");
    a.href = "#";
    a.className = "list-group-item list-group-item-action";
    a.dataset.convId = id;
    a.textContent = title;
    list.prepend(a);
}
