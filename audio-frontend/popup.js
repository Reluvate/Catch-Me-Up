showLatestTranscript();
chrome.storage.local.get("transcript", ({ transcript }) => {
  if (transcript && transcript !== "") {
    document.getElementById("stop").disabled = false;
    document.getElementById("start").disabled = true;
  }
});
document.getElementById("stop").addEventListener("click", async () => {
  document.getElementById("stop").disabled = true;
  document.getElementById("start").disabled = false;
  const tab = await getCurrentTab();
  if (!tab) return alert("Require an active tab");
  chrome.tabs.sendMessage(tab.id, { message: "stop" });
});

document.getElementById("clear").addEventListener("click", async () => {
  document.querySelector("#transcript").innerHTML = "";
  chrome.storage.local.set({ transcript: "" });
});

document.getElementById("start").addEventListener("click", async () => {
  const tab = await getCurrentTab();
  document.getElementById("stop").disabled = false;
  document.getElementById("start").disabled = true;
  if (!tab) return alert("Require an active tab");
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["main.js"],
  });
});

async function getCurrentTab() {
  const queryOptions = { active: true, lastFocusedWindow: true };
  const [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

chrome.runtime.onMessage.addListener(({ message }) => {
  if (message == "transcriptavailable") {
    console.log(showLatestTranscript());
  }
});

chrome.runtime.onMessage.addListener(({ message }) => {
  if (message == "stop") {
    socket.close();
    alert("Transcription ended");
    console.log("message", message);
  }
});

function showLatestTranscript() {
  chrome.storage.local.get("transcript", ({ transcript }) => {
    // document.getElementById("transcript").innerHTML = transcript;
  });
}

document.getElementById("form").onsubmit = sendQuestion;

async function sendQuestion(e) {
  e.preventDefault();
  const input = document.getElementById("question-input").value;
  const res = await fetch("http://localhost:5000/questioning", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: input,
      url: window.location.href,
    }),
  });
  const data = await res.json();
  console.log(data);
}
