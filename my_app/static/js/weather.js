let minimizeQueue = []; // Queue to store weather IDs
let isMinimizing = false; // Flag to track if an animation is running

function minimizeWeatherCard(weatherId) {
  minimizeQueue.push(weatherId); // Add to queue
  processQueue(); // Start queue processing
}

function processQueue() {
  if (isMinimizing || minimizeQueue.length === 0) return; // Stop if busy or empty

  isMinimizing = true;
  let weatherId = minimizeQueue.shift(); // Take the first ID in the queue
  let weatherCard = document.getElementById("weather-card-" + weatherId);

  if (weatherCard) {
    // ✅ Apply smooth fade-out & shrink effect
    weatherCard.style.transition =
      "opacity 0.4s ease-out, transform 0.3s ease-in-out";
    weatherCard.style.opacity = 0;
    weatherCard.style.transform = "translateY(-10px) scale(0.9)"; // Move up slightly

    setTimeout(() => {
      weatherCard.remove(); // Remove after animation
      sendMinimizeRequest(weatherId); // ✅ Send request to update DB
      isMinimizing = false;
      processQueue(); // Continue queue
    }, 400);
  } else {
    isMinimizing = false;
    processQueue(); // Continue if element doesn't exist
  }
}

function sendMinimizeRequest(weatherId) {
  fetch(`/update_clear/${weatherId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": "{{ csrf_token }}",
    },
    body: JSON.stringify({ weather_id: weatherId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.success) {
        console.error("Error:", data.error);
        alert("Failed to minimize. Try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Network issue. Try again.");
    });
}
