// 添加消息到聊天记录
function appendMessage(message) {
    var chatDisplay = document.getElementById("chat-display");
    var newMessage = document.createElement("div");
    newMessage.innerHTML = message;
    chatDisplay.appendChild(newMessage);
}

// 发送用户消息并获取机器人回复
function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const selectedModel = document.getElementById('model-select').value;
    appendMessage("<strong>user：</strong>" + userInput);
    document.getElementById("user-input").value = "";

    // Send user input and selected model to the server
    fetch("/get_response", {
        method: "POST",
        body: new URLSearchParams({
            "user_input": userInput,
            "cloud_model": selectedModel
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.text())
    .then(data => {
        appendMessage("<strong>chatbot：</strong>" + data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

document.getElementById('send-button').addEventListener('click', sendMessage);
// Enter监听
document.getElementById('user-input').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});





