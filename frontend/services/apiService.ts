// API Configuration
// For local development: http://127.0.0.1:8000
// For production: Replace with your Render backend URL

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function analyzeUrl(url: string) {
    const response = await fetch(`${API_BASE_URL}/analyze-url`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
    });

    if (!response.ok) {
        throw new Error("Backend request failed");
    }

    return response.json();
}
