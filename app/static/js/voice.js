let preferredVoice = null;

function loadVoices() {
    const voices = window.speechSynthesis.getVoices();
    preferredVoice = voices.find(voice => voice.name === 'Google português do Brasil') || 
                     voices.find(voice => voice.lang === 'pt-BR');
    
    console.log("Selected voice:", preferredVoice ? preferredVoice.name : "No pt-BR voice found");
}

window.speechSynthesis.onvoiceschanged = loadVoices;

const chatMessagesContainer = document.querySelector('.chat-messages');

chatMessagesContainer.addEventListener('click', function(event) {
    const speakButton = event.target.closest('.speak-button');
    if (!speakButton) {
        return;
    }

    const messageElement = speakButton.closest('.bot-message');
    const textElement = messageElement.querySelector('.message-text');
    if (!textElement) {
        console.error("Element .message-text not found in bot message.");
        return;
    }

    const textToSpeak = textElement.textContent;
    const utterance = new SpeechSynthesisUtterance(textToSpeak);

    utterance.rate = 1.2;
    utterance.lang = 'pt-BR';

    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
});
