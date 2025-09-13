const input = document.getElementById("chat-input");
const button = document.querySelector(".send-button");
const messagesContainer = document.querySelector(".chat-messages");

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    div.textContent = text;
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        if (data.bot) {
            addMessage(data.bot, "bot");
        } else if (data.error) {
            addMessage("Erro: " + data.error, "bot");
        }
    } catch (err) {
        addMessage("Erro de conexão com o servidor.", "bot");
    }
}

button.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
