document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    function getUserId() {
        let userId = sessionStorage.getItem("user_id");
        if (!userId) {
            userId = crypto.randomUUID();
            sessionStorage.setItem("user_id", userId);
        }
        return userId;
    }

    const userId = getUserId();

    appendMessage("Welcome! Write your request, what you want to do", "bot");

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    userInput.addEventListener("input", () => {
        // Reset height to 'auto' to correctly calculate scrollHeight for the current content
        userInput.style.height = "auto";
        // Set the height, ensuring it stays between min-height (40px) and max-height (150px) for AUTO-EXPANSION.
        // The 'resize: vertical;' CSS property will allow MANUAL resizing beyond max-height if the user drags the handle.
        userInput.style.height = Math.min(userInput.scrollHeight, 150) + "px";
    });

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        appendMessage(userMessage, "user");
        userInput.value = "";
        // Reset to its minimum height after sending, as it's now empty.
        userInput.style.height = "40px";

        const typingIndicator = showTypingIndicator();

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator(typingIndicator);
            appendMessage(data.response, "bot");
            if (data.menu) appendMenuOptions(data.menu);
            if (data.reset) setTimeout(resetChat, 2000);
        })
        .catch(error => {
            console.error("Error:", error);
            removeTypingIndicator(typingIndicator);
            appendMessage("Oops! Something went wrong. Please try again.", "bot");
        });
    }

    function appendMessage(message, sender) {
        const wrapper = document.createElement("div");
        wrapper.classList.add("message-wrapper");
        wrapper.classList.add(sender); // Add sender class to wrapper for alignment

        const label = document.createElement("div");
        label.classList.add("message-label");
        label.textContent = sender === "bot" ? "Bot" : "You";

        const msgContent = document.createElement("div");
        msgContent.classList.add(sender === "bot" ? "bot-message-content" : "user-message-content");
        msgContent.innerHTML = linkify(message);

        const timeDiv = document.createElement("div");
        timeDiv.classList.add("timestamp");
        timeDiv.textContent = getTime();

        // Order: Label, Message Content, Timestamp
        wrapper.appendChild(label);
        wrapper.appendChild(msgContent);
        wrapper.appendChild(timeDiv);
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function appendMenuOptions(options) {
        const menuDiv = document.createElement("div");
        menuDiv.classList.add("menu-options");
        options.forEach(option => {
            const btn = document.createElement("button");
            btn.textContent = option;
            btn.addEventListener("click", () => {
                userInput.value = option;
                sendMessage();
            });
            menuDiv.appendChild(btn);
        });
        chatBox.appendChild(menuDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        const typing = document.createElement("div");
        typing.classList.add("typing-indicator");
        typing.textContent = "Bot is typing...";
        chatBox.appendChild(typing);
        chatBox.scrollTop = chatBox.scrollHeight;
        return typing;
    }

    function removeTypingIndicator(indicator) {
        if (indicator && chatBox.contains(indicator)) chatBox.removeChild(indicator);
    }

    function getTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function resetChat() {
        sessionStorage.removeItem("user_id"); // Clear user_id on reset
        location.reload();
    }

    function linkify(text) {
        // This regex looks for URLs starting with http/https or www.
        // It also handles URLs without protocol but containing a domain.
        const urlPattern = /((https?:\/\/|www\.)[\w\-]+(\.[\w\-]+)+[\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])|([a-zA-Z0-9.\-]+(?:\.[a-zA-Z]{2,})(?:[\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#]))/gi;

        return text.replace(urlPattern, url => {
            // Check if the URL already starts with http:// or https://
            let fullUrl = url;
            if (!url.match(/^(https?:\/\/)/i)) {
                // If it starts with www., add http://
                if (url.match(/^www\./i)) {
                    fullUrl = `http://${url}`;
                } else if (url.match(/^[a-zA-Z0-9.\-]+(?:\.[a-zA-Z]{2,})/)) {
                    // For bare domains like example.com, add http://
                    fullUrl = `http://${url}`;
                }
            }
            return `<a href="${fullUrl}" target="_blank" rel="noopener noreferrer">${url}</a>`;
        });
    }
});