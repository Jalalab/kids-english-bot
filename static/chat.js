// static/chat.js
// Sends messages to the Flask server and shows the replies.

const chat = document.getElementById("chat");
const input = document.getElementById("msg");
const sendBtn = document.getElementById("send");
const stats = document.getElementById("stats");

// One random id per browser tab = one child session
const sessionId = "s" + Math.random().toString(36).slice(2, 10);

function addBubble(text, who) {
  const div = document.createElement("div");
  div.className = "bubble " + who;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

async function sendMessage(text) {
  text = (text || "").trim();

  // An empty text is only allowed for the first greeting
  if (text) addBubble(text, "child");

  const thinking = addBubble("...", "bot");
  sendBtn.disabled = true;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message: text }),
    });
    const data = await res.json();
    thinking.textContent = data.reply;
    stats.textContent = "Level " + data.level + " · ⭐ " + data.score;
  } catch (err) {
    thinking.textContent = "Oops! Let's try again. 😊";
  }

  sendBtn.disabled = false;
  input.focus();
  chat.scrollTop = chat.scrollHeight;
}

function sendFromInput() {
  const text = input.value;
  if (!text.trim()) return;
  input.value = "";
  sendMessage(text);
}

sendBtn.addEventListener("click", sendFromInput);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendFromInput();
});

document.querySelectorAll(".q").forEach((btn) => {
  btn.addEventListener("click", () => sendMessage(btn.dataset.msg));
});

// Start the chat: empty message = Lumi says hello
sendMessage("");