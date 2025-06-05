document.addEventListener("DOMContentLoaded", () => {
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const chatBox = document.getElementById("chat-box");
  const notificationArea = document.getElementById("notification-area");

  function showNotification(message) {
    notificationArea.textContent = message;
    notificationArea.style.display = "block";
  }

  async function checkData() {
    try {
      const response = await fetch(`http://backend:8000/check-data`);
    } catch (error) {
      console.error("Error checking data:", error);
      showNotification("Error checking data status.");
    }
  }

  async function sendMessageToBackend(message, chatBox) {
    try {
      const response = await fetch(
        `http://backend:8000/chat?q=${encodeURIComponent(message)}`,
        {
          method: "GET",
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      await processStreamedResponse(reader, chatBox);
    } catch (error) {
      console.error("Error sending message:", error);
      displayMessage(
        "Error: Could not get response from the backend.",
        "bot",
        chatBox
      );
    }
  }

  async function handleSendMessage(userInput, chatBox) {
    const message = userInput.value.trim();
    if (message) {
      displayMessage(message, "user", chatBox);
      userInput.value = "";
      await sendMessageToBackend(message, chatBox);
    }
  }

  checkData();

  sendButton.addEventListener("click", async () => {
    await handleSendMessage(userInput, chatBox);
  });

  userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendButton.click();
    }
  });
});
