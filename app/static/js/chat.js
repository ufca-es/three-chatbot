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
    let text = input.value.trim();
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


document.getElementById("btnStats").addEventListener("click", async () => {
    const res = await fetch("/api/stats");
    const data = await res.json();
    const statsArea = document.getElementById("statsArea");

    if (statsArea.classList.contains("hidden")) {
        statsArea.classList.remove("hidden");
        let html = `<h3>Estatísticas</h3>`;
        html += `<p>Total de interações: ${data.total_interactions}</p>`;

        const top5Questions = Object.entries(data.question_counts)
            .sort(([, countA], [, countB]) => countB - countA)
            .slice(0, 5);

        html += `<h4>Perguntas mais frequentes:</h4><ul>`;

        for (const [q, count] of top5Questions) {
            html += `<li>${q} (${count} vez(es))</li>`;
        }
        html += `</ul>`;

        html += `<h4>Personalidades usadas:</h4><ul>`;
        for (const [p, count] of Object.entries(data.personality_counts)) {
            html += `<li>${p} (${count} vez(es))</li>`;
        }
        html += `</ul>`;

        statsArea.innerHTML = html;
    } else {
        statsArea.classList.add("hidden");
        return;
    }

});
