html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Medisyn Chat</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    body {
        margin: 0;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #fff;
        display: flex;
        height: 100vh;
        overflow: hidden;
    }

    /* Sidebar */
    #sidebar {
        width: 250px;
        background: rgba(20, 20, 30, 0.95);
        backdrop-filter: blur(10px);
        padding: 20px;
        display: flex;
        flex-direction: column;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    #sidebar h2 {
        color: #00fff7;
        margin-bottom: 30px;
        text-align: center;
        font-weight: 700;
        text-shadow: 0 0 8px #00fff7;
    }
    #sidebar button {
        background: rgba(0, 255, 247, 0.1);
        border: 1px solid #00fff7;
        color: #00fff7;
        padding: 12px;
        margin: 8px 0;
        border-radius: 12px;
        cursor: pointer;
        transition: 0.3s;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    #sidebar button:hover {
        background: #00fff7;
        color: #121212;
        box-shadow: 0 0 12px #00fff7;
    }

    /* Main Chat Section */
    #main {
        flex: 1;
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(5px);
    }

    /* Header */
    #header {
        background: rgba(20, 20, 30, 0.9);
        padding: 15px;
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        color: #00fff7;
        text-shadow: 0 0 8px #00fff7;
    }

    /* Topic Section */
    #topic-box {
        display: flex;
        padding: 12px;
        background: rgba(20, 20, 30, 0.9);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        gap: 10px;
    }
    #topic-input {
        flex: 1;
        padding: 12px;
        border-radius: 10px;
        border: none;
        background: rgba(0,0,0,0.3);
        color: #fff;
        box-shadow: 0 0 10px rgba(0,255,247,0.2);
        font-size: 17px;
    }
    #topic-input:focus {
        outline: none;
        box-shadow: 0 0 15px #00fff7;
    }
    #set-topic {
        background: #00fff7;
        border: none;
        padding: 12px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
        color: #121212;
        transition: 0.3s;
    }
    #set-topic:hover {
        box-shadow: 0 0 15px #00fff7;
    }

    /* Chat Box */
    #chat-box {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: rgba(10,10,20,0.7);
        display: flex;
        flex-direction: column;
        gap: 12px;
        font-size: 17px;
        line-height: 1.5;
    }
    .message {
        margin: 5px 0;
        padding: 14px 18px;
        border-radius: 15px;
        max-width: 70%;
        word-wrap: break-word;
        backdrop-filter: blur(5px);
        white-space: pre-wrap; /* Preserve line breaks */
    }
    .user {
        background: linear-gradient(135deg, #00fff7, #00bcd4);
        align-self: flex-end;
        color: #121212;
        box-shadow: 0 0 10px #00fff7;
    }
    .bot {
        background: rgba(255,255,255,0.08);
        align-self: flex-start;
        color: #fff;
        border: 1px solid rgba(0,255,247,0.2);
        box-shadow: 0 0 8px rgba(0,255,247,0.2);
    }

    /* Input Area */
    #input-box {
        display: flex;
        padding: 15px;
        border-top: 1px solid rgba(255,255,255,0.1);
        background: rgba(20, 20, 30, 0.9);
        gap: 10px;
    }
    #message {
        flex: 1;
        padding: 14px;
        border: none;
        border-radius: 15px;
        background: rgba(0,0,0,0.3);
        color: #fff;
        box-shadow: 0 0 10px rgba(0,255,247,0.2);
        font-size: 17px;
    }
    #message:focus {
        outline: none;
        box-shadow: 0 0 15px #00fff7;
    }
    #send-btn {
        background: #00fff7;
        border: none;
        padding: 14px 25px;
        border-radius: 15px;
        cursor: pointer;
        font-weight: 600;
        color: #121212;
        transition: 0.3s;
    }
    #send-btn:hover {
        box-shadow: 0 0 15px #00fff7;
    }

    /* Scrollbar */
    #chat-box::-webkit-scrollbar {
        width: 8px;
    }
    #chat-box::-webkit-scrollbar-thumb {
        background: rgba(0,255,247,0.4);
        border-radius: 4px;
    }
    #chat-box::-webkit-scrollbar-track {
        background: transparent;
    }
</style>
</head>
<body>

<!-- Sidebar -->
<div id="sidebar">
    <h2>Medisyn</h2>
    <button>Home</button>
    <button>History</button>
    <button>Settings</button>
</div>

<!-- Main Chat -->
<div id="main">
    <div id="header">Medisyn Chat</div>

    <!-- Topic Input -->
    <div id="topic-box">
        <input type="text" id="topic-input" placeholder="Enter topic..." />
        <button id="set-topic">Set Topic</button>
    </div>

    <!-- Chat Messages -->
    <div id="chat-box"></div>

    <!-- Message Input -->
    <div id="input-box">
        <input type="text" id="message" placeholder="Type your message..." />
        <button id="send-btn">Send</button>
    </div>
</div>

<script>
    let ws = new WebSocket("ws://localhost:8000/ws/chat");
    let topic = "";

    document.getElementById("set-topic").onclick = function() {
        topic = document.getElementById("topic-input").value.trim();
        if(topic) {
            let chatBox = document.getElementById("chat-box");
            let msg = document.createElement("div");
            msg.classList.add("message", "bot");
            msg.textContent = "Topic set to: " + topic;
            chatBox.appendChild(msg);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    };

    ws.onmessage = function(event) {
        let chatBox = document.getElementById("chat-box");
        let msg = document.createElement("div");
        msg.classList.add("message", "bot");

        // Remove <|user|> and <|assistant|> tokens and preserve line breaks
        let text = event.data.replace(/<\\|user\\|>|<\\|assistant\\|>/g, "").trim();
        msg.textContent = text;

        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    document.getElementById("send-btn").onclick = function() {
        let input = document.getElementById("message");
        if (input.value.trim() !== "") {
            let chatBox = document.getElementById("chat-box");

            // User message
            let msg = document.createElement("div");
            msg.classList.add("message", "user");
            msg.textContent = input.value;
            chatBox.appendChild(msg);

            // Send only raw text
            ws.send(input.value);
            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    };
</script>
</body>
</html>
"""
