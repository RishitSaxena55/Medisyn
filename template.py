# template.py

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>AI Topic Chat</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Roboto', sans-serif;
      background: linear-gradient(to right, #74ebd5, #ACB6E5);
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px;
      height: 100vh;
      margin: 0;
    }
    h1 {
      color: #333;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }
    #chatContainer {
      width: 650px;
      max-width: 95%;
      background: #ffffffee;
      border-radius: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.1);
      padding: 20px;
      display: flex;
      flex-direction: column;
      height: 75vh;
    }
    #topicContainer {
      display: flex;
      gap: 10px;
      margin-bottom: 12px;
    }
    #topicText {
      flex: 1;
      padding: 12px 15px;
      border-radius: 10px;
      border: 1px solid #ccc;
      font-size: 15px;
      outline: none;
    }
    #connectBtn {
      padding: 12px 16px;
      border: none;
      border-radius: 10px;
      background-color: #007bff;
      color: white;
      cursor: pointer;
      font-size: 15px;
    }
    #messages {
      flex: 1;
      overflow-y: auto;
      border: 1px solid #eee;
      padding: 15px;
      border-radius: 15px;
      background-color: #f9f9f9;
      margin-bottom: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .message {
      padding: 10px 14px;
      border-radius: 18px;
      max-width: 80%;
      word-wrap: break-word;
      animation: fadeIn 0.12s ease-in-out;
    }
    .userMsg {
      background: linear-gradient(145deg, #6dd5ed, #2193b0);
      color: white;
      align-self: flex-end;
      box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    .botMsg {
      background: #e0e0e0;
      color: #222;
      align-self: flex-start;
      box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
      white-space: pre-wrap;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    #inputContainer {
      display: flex;
      gap: 10px;
      margin-top: 6px;
    }
    #messageText {
      flex: 1;
      padding: 12px 15px;
      border-radius: 10px;
      border: 1px solid #ccc;
      font-size: 15px;
      outline: none;
    }
    #sendBtn {
      padding: 12px 16px;
      border: none;
      border-radius: 10px;
      background-color: #28a745;
      color: white;
      cursor: pointer;
      font-size: 15px;
    }
    #status {
      margin-top: 8px;
      font-size: 13px;
      color: #444;
    }
    /* scrollbar */
    #messages::-webkit-scrollbar { width: 8px; }
    #messages::-webkit-scrollbar-thumb { background-color: rgba(0,0,0,0.15); border-radius: 8px; }
  </style>
</head>
<body>
  <h1>AI Topic Chat (RAG)</h1>
  <div id="chatContainer">
    <div id="topicContainer">
      <input id="topicText" type="text" placeholder="Enter topic (used as thread_id) — e.g. aging, cardiology" />
      <button id="connectBtn" onclick="connectWebSocket()">Connect</button>
    </div>

    <div id="messages"></div>

    <div id="inputContainer">
      <input id="messageText" type="text" placeholder="Type your message..." autocomplete="off" />
      <button id="sendBtn" onclick="sendMessage(event)">Send</button>
    </div>

    <div id="status">Not connected</div>
  </div>

  <script>
    let ws = null;
    let currentBotMsgDiv = null;
    let pendingMessage = null;

    function setStatus(text) {
      document.getElementById('status').innerText = text;
    }

    function scrollMessages() {
      const messagesDiv = document.getElementById('messages');
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function connectWebSocket() {
      const topic = document.getElementById('topicText').value.trim();
      if (!topic) {
        alert('Please enter a topic to connect (this acts as the thread id).');
        return;
      }

      // If already connected to same topic, do nothing
      if (ws && ws.readyState === WebSocket.OPEN) {
        setStatus('Already connected');
        return;
      }

      const scheme = (window.location.protocol === 'https:') ? 'wss' : 'ws';
      const url = `${scheme}://${window.location.host}/ws/${encodeURIComponent(topic)}`;

      setStatus('Connecting...');
      document.getElementById('connectBtn').disabled = true;
      ws = new WebSocket(url);

      ws.onopen = () => {
        setStatus('Connected — streaming ready');
        document.getElementById('connectBtn').disabled = false;
        document.getElementById('connectBtn').innerText = 'Connected';
        // If user tried to send while connecting, send it now
        if (pendingMessage) {
          ws.send(pendingMessage);
          pendingMessage = null;
        }
      };

      ws.onmessage = (event) => {
        const data = event.data;

        // End-of-response marker
        if (data === "__END__") {
          currentBotMsgDiv = null;
          return;
        }

        // Errors from server
        if (data.startsWith("[ERROR]")) {
          const err = document.createElement('div');
          err.className = 'message botMsg';
          err.innerText = data;
          document.getElementById('messages').appendChild(err);
          currentBotMsgDiv = null;
          scrollMessages();
          return;
        }

        // Append token/chunk to current bot bubble, or create one
        if (!currentBotMsgDiv) {
          currentBotMsgDiv = document.createElement('div');
          currentBotMsgDiv.className = 'message botMsg';
          currentBotMsgDiv.innerText = data;
          document.getElementById('messages').appendChild(currentBotMsgDiv);
        } else {
          // Append new chunk without replacing entire bubble (keeps cursor stable)
          currentBotMsgDiv.innerText += data;
        }

        scrollMessages();
      };

      ws.onclose = () => {
        setStatus('Disconnected');
        document.getElementById('connectBtn').innerText = 'Connect';
        document.getElementById('connectBtn').disabled = false;
        ws = null;
      };

      ws.onerror = (err) => {
        console.error('WebSocket error', err);
        setStatus('Error: see console');
      };
    }

    function sendMessage(event) {
      event.preventDefault();
      const input = document.getElementById('messageText');
      const msg = input.value.trim();
      if (!msg) return;

      // Add user message bubble
      const userMsg = document.createElement('div');
      userMsg.className = 'message userMsg';
      userMsg.innerText = msg;
      document.getElementById('messages').appendChild(userMsg);
      scrollMessages();

      // If websocket not ready, connect and queue the message
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        pendingMessage = msg;
        connectWebSocket();
      } else {
        ws.send(msg);
      }

      input.value = '';
    }

    // Optional: allow Enter key to send
    document.getElementById('messageText').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        sendMessage(new Event('submit'));
      }
    });

    // Try to prefill topic from URL path (if you want)
    (function prefillTopicFromPath(){
      try {
        const pathParts = window.location.pathname.split('/');
        if (pathParts.length > 1 && pathParts[1]) {
          const topicEl = document.getElementById('topicText');
          if (topicEl && topicEl.value.trim() === '') {
            topicEl.value = decodeURIComponent(pathParts[1]);
          }
        }
      } catch(e){}
    })();
  </script>
</body>
</html>
"""
