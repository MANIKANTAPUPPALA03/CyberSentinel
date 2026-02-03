async function checkURL() {
    const url = document.getElementById("urlInput").value;
    const resultDiv = document.getElementById("result");

    if (!url) {
        alert("Please enter a URL");
        return;
    }

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/check-url?url=${encodeURIComponent(url)}`,
            { method: "POST" }
        );

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();

        resultDiv.classList.remove("hidden");
        resultDiv.style.display = "block"; // Ensure it's visible

        document.getElementById("status").innerText =
            `Status: ${data.final_status}`;

        document.getElementById("score").innerText =
            `Trust Score: ${data.trust_score}/100`;

        document.getElementById("details").innerText =
            JSON.stringify(data.signals, null, 2);

    } catch (error) {
        console.error("Error checking URL:", error);
        alert("Failed to connect to the backend. Is it running?");
    }
}
