const input = document.getElementById("chat-input");
const button = document.querySelector(".send-button");
const messagesContainer = document.querySelector(".chat-messages");

function addMessage(text, sender) {
    const div = document.createElement("div");
    const span = document.createElement("span");

    span.classList.add("message-text");
    span.textContent = text;
    div.appendChild(span);

    
    if (sender === "bot") {
        const button = document.createElement("button");
        button.setAttribute("class", "speak-button");
        button.setAttribute("aria-label", "Ouvir mensagem");
        const icon = document.createElement("ion-icon");
        icon.setAttribute("name", "volume-medium-outline");
        button.appendChild(icon);
        div.appendChild(button);
        div.classList.add("message", "bot-message");
    } else {
        div.classList.add("message", "user-message");
    }

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
    const statsArea = document.getElementById("statsArea");
    if (!statsArea.classList.contains("hidden")) {
        statsArea.classList.add("hidden");
        return;
    }

    try {
        const res = await fetch("/api/stats");
        if (!res.ok) {
            throw new Error(`Erro ao buscar estatísticas: ${res.statusText}`);
        }
        const data = await res.json();

        const processedPersonalities = processPersonalities(data.personality_counts);

        let html = `<h3>Estatísticas</h3>`;
        html += `<p>Total de interações: ${data.total_interactions}</p>`;

        const top5Questions = Object.entries(data.question_counts)
            .sort(([, countA], [, countB]) => countB - countA)
            .slice(0, 5);

        if (top5Questions.length > 0) {
            html += `<h4>Perguntas mais frequentes:</h4><ul>`;
            for (const [q, count] of top5Questions) {
                html += `<li>${q} (${count} vez(es))</li>`;
            }
            html += `</ul>`;
        }

        if (Object.keys(processedPersonalities).length > 0) {
            html += `<h4>Personalidades usadas:</h4><ul>`;
            const sortedPersonalities = Object.entries(processedPersonalities)
                .sort(([, countA], [, countB]) => countB - countA);

            for (const [personality, count] of sortedPersonalities) {
                html += `<li>${personality}: ${count}</li>`;
            }
            html += `</ul>`;
        }

        statsArea.innerHTML = html;
        statsArea.classList.remove("hidden");

    } catch (error) {
        console.error("Falha ao carregar estatísticas:", error);
        statsArea.innerHTML = `<p style="color: red;">Não foi possível carregar as estatísticas.</p>`;
        statsArea.classList.remove("hidden");
    }
});

function processPersonalities(personalityCounts) {
    const counts = { ...personalityCounts };

    const academicTotal = (counts.academico || 0) + (counts.set_academico || 0);

    delete counts.academico;
    delete counts.set_academico;

    if (academicTotal > 0) {
        counts.academico = academicTotal;
    }

    const friendlyNamesMap = {
        academico: "Acadêmico",
        set_acessivel: "Acessível",
        set_gamificado: "Gamificado"
    };

    const result = {};
    for (const [key, count] of Object.entries(counts)) {
        const friendlyName = friendlyNamesMap[key] || key.replace("set_", "").charAt(0).toUpperCase() + key.slice(1);
        result[friendlyName] = count;
    }

    return result;
}