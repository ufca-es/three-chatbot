    const aboutWindow = document.getElementById('about-window');
    const codeOutput = document.getElementById('code-output');
    const terminalInput = document.getElementById('terminal-input');
    const aboutTextContent = document.getElementById('about-text-content');

    const challengeState = {
        code: `
<span class="token-comment">// SISTEMA OFFLINE. Ativação necessária.</span>
<span class="token-keyword">class</span> <span class="token-class-name">ThreeSystem</span> {
    <span class="token-function">constructor</span>() {
        <span class="token-keyword">this</span><span class="token-punctuation">.</span>status <span class="token-punctuation">=</span> <span class="token-string">'offline'</span><span class="token-punctuation">;</span>
    }
    <span class="token-comment">// Método de ativação aguardando a chave...</span>
    <span class="token-function">activate</span>(<span class="token-parameter">activationKey</span>) { <span class="token-comment">/* ... */</span> }
}
<span class="token-keyword">const</span> system <span class="token-punctuation">=</span> <span class="token-keyword">new</span> <span class="token-class-name">ThreeSystem</span>()<span class="token-punctuation">;</span>`,
        text: `
            <h2><span style="color: #ff5f56;">●</span> ALERTA: Sistema Offline</h2>
            <p>O núcleo da plataforma <strong>Three</strong> precisa ser reativado. A função <code>activate()</code> requer uma chave de ativação para restaurar as operações.</p>
            <p><strong>Pista:</strong> Nossa filosofia é que aprender a programar deve ser uma verdadeira... <strong>aventura</strong>.</p>
            <p>Use o terminal ao lado para chamar a função com a chave correta. Ex: <code>system.activate('sua-chave')</code></p>`
    };

    const successState = {
        codeToType: `
<span class="token-comment">// Bem-vindo ao código-fonte do Three!</span>
<span class="token-keyword">class</span> <span class="token-class-name">ThreePlatform</span> {
    <span class="token-function">constructor</span>(<span class="token-parameter">user</span>) {
        <span class="token-keyword">this</span><span class="token-punctuation">.</span>user <span class="token-punctuation">=</span> user<span class="token-punctuation">;</span>
        <span class="token-keyword">this</span><span class="token-punctuation">.</span>missions <span class="token-punctuation">=</span> [<span class="token-string">'HTML'</span>, <span class="token-string">'CSS'</span>, <span class="token-string">'JavaScript'</span>]<span class="token-punctuation">;</span>
        <span class="token-keyword">this</span><span class="token-punctuation">.</span>status <span class="token-punctuation">=</span> <span class="token-string">'<span style="color: #27c93f;">ONLINE</span>'</span><span class="token-punctuation">;</span>
    }

    <span class="token-function">startLearning</span>() {
        <span class="token-keyword">return</span> <span class="token-string">\`Jornada de \${<span class="token-keyword">this</span><span class="token-punctuation">.</span>user} iniciada!\`</span><span class="token-punctuation">;</span>
    }

    <span class="token-function">completeMission</span>(<span class="token-parameter">mission</span>) {
        console<span class="token-punctuation">.</span><span class="token-function">log</span>(<span class="token-string">\`\${mission} concluída. Recompensas desbloqueadas!\`</span>)<span class="token-punctuation">;</span>
    }
}
        `.trim(),
        text: `
            <h2><span style="color: #27c93f;">●</span> Sistema Online: O que é o Three?</h2>
            <p>O <strong>Three</strong> é mais que uma plataforma: é o seu novo universo para aprender a programar. Desenhada desde o início para ser <strong>gamificada, acessível e prática</strong>.</p>
            <p>Nossa missão é transformar o aprendizado de código em uma jornada divertida e cheia de recompensas.</p>
            <a href="#chat" class="cta-button">Comece sua jornada</a>`
    };

    const correctAnswer = "system.activate('aventura')";

    function initializeChallenge() {
        codeOutput.innerHTML = challengeState.code;
        aboutTextContent.innerHTML = challengeState.text;
    }

    function handleTerminalInput(event) {
        if (event.key === 'Enter') {
            const userInput = terminalInput.value.trim();

            if (userInput === correctAnswer) {
                triggerSuccessSequence();
            } else {
                triggerErrorSequence();
            }
        }
    }

    function triggerSuccessSequence() {
        aboutWindow.classList.add('success-glow');
        terminalInput.disabled = true;
        terminalInput.placeholder = "Comando aceito... inicializando sistema...";
        aboutTextContent.innerHTML = successState.text;
        typeCodeAnimation(successState.codeToType);
    }

    function triggerErrorSequence() {
        terminalInput.classList.add('shake-error');
        setTimeout(() => {
            terminalInput.classList.remove('shake-error');
            terminalInput.value = '';
        }, 300);
    }

    let typeIndex = 0;
    function typeCodeAnimation(codeString) {
        if (typeIndex < codeString.length) {
            codeOutput.innerHTML = codeString.substring(0, typeIndex + 1) + '<span class="typing-cursor">▋</span>';
            typeIndex++;
            setTimeout(() => typeCodeAnimation(codeString), 15); 
        } else {
            codeOutput.innerHTML = codeString; 
        }
    }

    initializeChallenge();
    terminalInput.addEventListener('keydown', handleTerminalInput);
