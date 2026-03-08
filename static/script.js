let selectedPantheon = null;
let selectedEntity = null;

function selectPantheon(name) {
    selectedPantheon = name.toLowerCase();
    localStorage.setItem("pantheon", selectedPantheon);

    if (selectedPantheon === "greek") {
        window.location.href = "/pantheon/greek";
    }
}

function selectEntity(name) {
    selectedEntity = name.toUpperCase();
    localStorage.setItem("entity", selectedEntity);
    window.location.href = "/chat";
}

function loadChatContext() {
    selectedPantheon = localStorage.getItem("pantheon") || "greek";
    selectedEntity = localStorage.getItem("entity") || "CHAOS";

    const title = document.getElementById("chat-entity");
    if (title) {
        title.innerText = selectedEntity;
    }
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    if (!input || !chatBox) return;

    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                pantheon: selectedPantheon || "greek",
                entity: selectedEntity || "CHAOS",
                message: message
            })
        });

        const data = await response.json();

        if (data.reply) {
            appendMessage("assistant", data.reply);
        } else if (data.error) {
            appendMessage("assistant", "Error: " + data.error);
        } else {
            appendMessage("assistant", "No response received.");
        }

    } catch (error) {
        appendMessage("assistant", "Connection error.");
    }
}

function appendMessage(role, text) {
    const chatBox = document.getElementById("chat-box");
    if (!chatBox) return;

    const message = document.createElement("div");
    message.className = "message " + role;
    message.innerText = text;

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}
