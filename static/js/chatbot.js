// Get references to DOM elements
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Event listener for the send button
sendButton.addEventListener('click', () => {
    const messageText = messageInput.value;
    if (messageText.trim() === '') {
        return;
    }

    // Send the user message to the server
    sendMessage('User', messageText);

    // Clear the input field
    messageInput.value = '';

    // Simulate a bot response (you would replace this with a server response)
    simulateBotResponse(messageText);
});

// Function to send a message and display it in the chat
function sendMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.textContent = sender + ': ' + text;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Function to simulate a bot response
function simulateBotResponse(userMessage) {
    // Simulate a simple bot response (you can replace this with actual bot logic)
    const botResponse = 'Bot: This is a simulated bot response to "' + userMessage + '".';

    // Display the bot response in the chat
    setTimeout(() => {
        sendMessage('Bot', botResponse);
    }, 1000); // Simulate a delay for the bot's response
}

// Example: Simulate an initial bot greeting
simulateBotResponse('Hello, how can I help you?');
