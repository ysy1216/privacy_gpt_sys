// 添加折叠按钮的点击事件监听器
document.querySelector('.collapse-chat-btn').addEventListener('click', () => {
    document.querySelector('.chat-history').classList.toggle('collapsed');
    document.querySelector('.chat-panel').classList.toggle('expanded');
});


// 选择青少年模式时隐藏敏感等级下列列表，更改模型选择列表内容
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggleButton');
    const hiddenSL = document.getElementById('sensitivity-level');  
    const modelSelect = document.getElementById('model-select');
    
    toggleButton.addEventListener('change', function() {
        if (toggleButton.checked) {
            hiddenSL.style.display = 'none'; // 隐藏敏感等级下拉列表
            
            // 清空模型选择器内容并添加新的下拉列表选项
            modelSelect.innerHTML = `
                <option value="new_model1">新模型1</option>
                <option value="new_model2">新模型2</option>
                <option value="new_model3">新模型3</option>
            `;
        } 
        
        else {
            hiddenSL.style.display = 'block'; // 恢复另一个复选框的显示
            
            // 恢复原有下拉列表选项
            modelSelect.innerHTML = `
                <option value="cloud_model1">百度云模型</option>
                <option value="cloud_model2">腾讯云模型</option>
                <option value="cloud_model3" selected>gpt-3.5-turbo</option>
            `;
        }
    });
});


// 添加消息到聊天框函数
function appendMessage(userType, message, modelMessage = "") {
    const chatDisplay = document.getElementById("chat-display");
    const outsideMessageContainer = document.createElement("div")
    outsideMessageContainer.classList.add(userType === "user" ? "user-message-outside" : "chatbot-message-outside");
    const messageContainer = document.createElement("div");

    // 消息内容
    const messageContent = document.createElement("div");
    messageContent.classList.add("message-content");
    messageContent.innerHTML = message;
    
    // 头像元素
    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    const avatarImg = document.createElement("img");
    avatarImg.classList.add("avatar-img")
    // 获取头像Src
    avatarImg.src = userType === "user" ? "../images/user-avatar.png" : "../images/bot-avatar.png";
    avatar.appendChild(avatarImg);

    // 复制按钮
    const copyButton = document.createElement("button");
    copyButton.textContent = "复制";
    copyButton.classList.add("copy-button");
    copyButton.addEventListener("click", function() {
        copyToClipboard(message);
        copyButton.textContent = "已复制";
        setTimeout(function() {
            copyButton.textContent = "复制";
        }, 1500); // 1.5s 后恢复复制按钮文本
    });

    // 隐藏模型消息按钮
    if (modelMessage !== "" && modelMessage.replace(/\s/g, '') != message.replace(/\s/g, '')) {
        const hideModelButton = document.createElement("button");
        hideModelButton.textContent = "隐藏模型消息";
        hideModelButton.classList.add("hide-model-button");
        hideModelButton.addEventListener("click", function() {
            outsideModelMessageContainer.style.display = outsideModelMessageContainer.style.display === "none" ? "flex" : "none";
            hideModelButton.textContent = outsideModelMessageContainer.style.display === "none" ? "展开模型消息" : "隐藏模型消息";
        });

        // 根据用户类型设置不同的样式类名
        messageContainer.classList.add(userType === "user" ? "user-message" : "chatbot-message");
        messageContainer.appendChild(avatar);
        messageContainer.appendChild(messageContent);
        messageContainer.appendChild(hideModelButton);
        messageContainer.appendChild(copyButton);
        outsideMessageContainer.appendChild(messageContainer)

        // 模型消息
        // width 100%外部盒子
        const outsideModelMessageContainer = document.createElement("div");
        outsideModelMessageContainer.classList.add("model-message-outside");
        // 包含头像、文本、按钮的盒子
        const modelMessageContainer = document.createElement("div");
        modelMessageContainer.classList.add("model-message");
        // 只占大小的模型头像
        const modelAvatar = document.createElement("div");
        modelAvatar.classList.add("avatar");
        // 模型文本区域
        const modelMessageContent = document.createElement("div");
        modelMessageContent.classList.add("model-message-content");
        modelMessageContent.innerHTML = modelMessage;
        // 模型消息复制按钮
        const modelCopyButton = document.createElement("button");
        modelCopyButton.textContent = "复制";
        modelCopyButton.classList.add("copy-button");
        modelCopyButton.addEventListener("click", function() {
            copyToClipboard(modelMessage);
            modelCopyButton.textContent = "已复制";
            setTimeout(function() {
                modelCopyButton.textContent = "复制";
            }, 1500); // 1.5s 后恢复复制按钮文本
        });

        modelMessageContainer.appendChild(modelAvatar);
        modelMessageContainer.appendChild(modelMessageContent);
        modelMessageContainer.appendChild(modelCopyButton);
        outsideModelMessageContainer.appendChild(modelMessageContainer)

        
        chatDisplay.appendChild(outsideMessageContainer);
        chatDisplay.appendChild(outsideModelMessageContainer);
    } 
    
    else {
        // 根据用户类型设置不同的样式类名
        messageContainer.classList.add(userType === "user" ? "user-message" : "chatbot-message");
        messageContainer.appendChild(avatar);
        messageContainer.appendChild(messageContent);
        messageContainer.appendChild(copyButton);

        outsideMessageContainer.appendChild(messageContainer)
        chatDisplay.appendChild(outsideMessageContainer);
    }
}


// 复制文本到剪贴板函数
function copyToClipboard(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
}

// 一键隐藏所有模型消息按钮点击事件
// document.getElementById("hide-all-model-messages-button").addEventListener("click", function() {
//     const modelMessages = document.querySelectorAll(".model-message");
//     modelMessages.forEach(function(modelMessage) {
//         modelMessage.style.display = "none";
//         const hideModelButton = modelMessage.nextElementSibling;
//         if (hideModelButton) {
//             hideModelButton.textContent = "展开模型消息";
//         }
//     });
// });


// 发送用户消息并获取机器人回复
function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const selectedModel = document.getElementById('model-select').value;
    appendMessage("user", userInput, "我是测试模型消息");
    
    // 清空输入框
    document.getElementById("user-input").value = "";

    fetch("/get_response", {
        method: "POST", // 使用 POST 请求方法发送数据
        body: new URLSearchParams({
            "user_input": userInput, // 用户输入的内容
            "cloud_model": selectedModel // 选择的模型
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded" // 请求头的内容类型是表单编码的数据
        }
    })
    .then(response => response.text()) // 将响应转换为文本
    .then(data => {
        appendMessage("bot", data); // 将服务器响应添加到聊天界面
    })
    .catch(error => {
        console.error("Error:", error); // 捕捉错误并打印到控制台
    });
}


// 为发送按钮添加事件监听器
document.getElementById('send-button').addEventListener('click', sendMessage);
// Enter+ctrl发送
document.getElementById('user-input').addEventListener('keydown', function (event) {
    if (event.key === "Enter" && !event.ctrlKey) {
        // 阻止默认的 Enter 键行为（换行）
        event.preventDefault();
    
        // 在光标位置插入换行符
        const startPos = this.selectionStart;
        const endPos = this.selectionEnd;
        this.value = this.value.substring(0, startPos) + "\n" + this.value.substring(endPos);
        
        // 设置新的光标位置
        this.selectionStart = startPos + 1;
        this.selectionEnd = startPos + 1;
    } 
    else if (event.key === "Enter" && event.ctrlKey) {
        // 阻止默认的 Enter 键行为
        event.preventDefault();
        
        // 执行发送内容的操作
        sendMessage();
    }
});

// 一键清除聊天框内容
function clearChat() {
    var chatDisplay = document.getElementById("chat-display");
    var confirmation = confirm("记录清除后无法恢复，您确定要清除吗？");
    if (confirmation) {
      chatDisplay.innerHTML = ""; // 清空聊天显示区域的内容
    }
  }

 
  // 导出聊天记录的函数
  function handleExport() {
    // 获取聊天显示区域的引用
    var chatDisplay = document.getElementById("chat-display");
    var chatContent = chatDisplay.innerText;
    var blob = new Blob([chatContent], { type: "text/plain" });

    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "chat_export.txt";
    a.textContent = "Download";
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }