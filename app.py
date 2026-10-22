from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

FAQS = {
    "hello": "Hello! 👋 Welcome to our AI Chatbot.",
    "hi": "Hi there! How can I help you today?",
    "how are you": "I'm doing great! Thanks for asking 😊",
    "your name": "I'm CodeAlpha Chatbot, your virtual assistant.",
    "what can you do": "I can answer basic questions and help you with common queries.",
    "cloud computing": "Cloud computing provides computing services like servers, storage, and databases over the internet.",
    "python": "Python is a beginner-friendly programming language used in web development, AI, and automation.",
    "internship": "An internship helps you gain practical experience and improve your professional skills.",
    "thank you": "You're welcome! 😊",
    "bye": "Goodbye! Have a great day! 👋"
}

def get_reply(message):
    text = message.lower().strip()

    if not text:
        return "Please type a message."

    for keyword, reply in FAQS.items():
        if keyword in text:
            return reply

    return "Sorry, I don't know that yet. Try asking about Python, cloud computing, or internships!"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CodeAlpha AI Chatbot</title>
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #101827;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
.chat {
    width: 90%;
    max-width: 480px;
    background: #1d293b;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 10px 35px #0005;
}
header {
    background: #2563eb;
    padding: 20px;
    text-align: center;
}
header h2 { margin: 0 0 6px; }
header p { margin: 0; font-size: 13px; }
#messages {
    height: 350px;
    overflow-y: auto;
    padding: 16px;
}
.msg {
    padding: 11px 14px;
    border-radius: 12px;
    margin: 10px 0;
    max-width: 85%;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}
.bot { background: #334155; }
.user { background: #2563eb; margin-left: auto; }
form {
    display: flex;
    gap: 8px;
    padding: 14px;
    background: #172235;
}
input {
    flex: 1;
    min-width: 0;
    padding: 12px;
    border: 0;
    border-radius: 8px;
    font-size: 15px;
}
button {
    border: 0;
    border-radius: 8px;
    padding: 12px 16px;
    background: #3b82f6;
    color: white;
    font-weight: bold;
    cursor: pointer;
}
</style>
</head>
<body>
<div class="chat">
    <header>
        <h2>🤖 CodeAlpha Chatbot</h2>
        <p>Online · Ready to help</p>
    </header>
    <div id="messages">
        <div class="msg bot">Hi! 👋 I'm your virtual assistant. Ask me about Python, cloud computing, or internships.</div>
    </div>
    <form id="chat-form">
        <input id="message" placeholder="Type your message..." autocomplete="off" required>
        <button type="submit">Send</button>
    </form>
</div>
<script>
const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const messages = document.getElementById("messages");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: text})
        });
        const data = await response.json();
        addMessage(data.reply, "bot");
    } catch (error) {
        addMessage("Something went wrong. Please try again.", "bot");
    }
});

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "msg " + sender;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    return jsonify({"reply": get_reply(message)})

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)