const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

function appendMessage(sender, message, isHTML = false) {
    const messageElement = document.createElement("div");
    
    if (isHTML) {
        messageElement.innerHTML = `${sender}: ${message}`;
    } else {
        messageElement.textContent = `${sender}: ${message}`;
    }
    
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

sendButton.addEventListener("click", async () => {
    const prompt = userInput.value;
    if (!prompt) return;

    appendMessage("You", prompt);
    userInput.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    if (data.response) {
        appendMessage("Bot", data.response, true);  // HTML을 그대로 렌더링
    } else {
        appendMessage("Bot", "Error: " + data.error);
    }
});
