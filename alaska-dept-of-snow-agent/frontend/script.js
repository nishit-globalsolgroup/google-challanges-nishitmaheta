const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const chatBox = document.getElementById("chat-box");

const API_URL = "http://localhost:8000/chat";

function addMessage(role, text, sources = []) {
  const div = document.createElement("div");
  div.className = `message ${role}`;

  let html = `<div>${text}</div>`;

  if (sources && sources.length > 0) {
    html += `<div class="sources"><strong>Sources:</strong><br>${sources.join("<br>")}</div>`;
  }

  div.innerHTML = html;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;

  return div;
}

function addLoader() {
  const div = document.createElement("div");
  div.className = "message bot loader";
  div.innerHTML = `
    <div class="dots">
      <span></span><span></span><span></span>
    </div>
  `;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = input.value.trim();
  if (!question) return;

  addMessage("user", `You: ${question}`);
  input.value = "";

  const loader = addLoader();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();

    loader.remove();

    addMessage(
      "bot",
      data.answer || "No answer returned.",
      data.sources || []
    );

  } catch (error) {
    loader.remove();
    addMessage("bot", "Unable to reach the ADS agent API.");
  }
});