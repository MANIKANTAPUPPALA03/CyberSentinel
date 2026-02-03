import os
import joblib
from urllib.parse import urlparse
from ml.feature_extraction import extract_features

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")

model = None
if os.path.exists(model_path):
    model = joblib.load(model_path)

# Known trusted domains - these should NEVER be flagged as malicious
TRUSTED_DOMAINS = [
    "google.com", "google.co.in", "google.co.uk",
    "youtube.com", "facebook.com", "instagram.com",
    "twitter.com", "x.com", "linkedin.com",
    "microsoft.com", "apple.com", "amazon.com",
    "github.com", "gitlab.com", "stackoverflow.com",
    "wikipedia.org", "reddit.com", "netflix.com",
    "spotify.com", "paypal.com", "dropbox.com",
    "zoom.us", "slack.com", "notion.so",
    "cloudflare.com", "aws.amazon.com", "azure.com",
]


def is_trusted_domain(url: str) -> bool:
    """Check if URL belongs to a known trusted domain."""
    try:
        parsed = urlparse(url if url.startswith("http") else "https://" + url)
        domain = parsed.netloc.lower()
        
        # Remove www prefix
        if domain.startswith("www."):
            domain = domain[4:]
        
        # Check exact match or subdomain match
        for trusted in TRUSTED_DOMAINS:
            if domain == trusted or domain.endswith("." + trusted):
                return True
        return False
    except:
        return False


def analyze_with_ml(url: str):
    """Analyze URL using trained ML model for phishing detection."""
    
    # If model not trained yet, return placeholder
    if model is None:
        return {
            "risk_level": "Unknown",
            "confidence": 0.0,
            "prediction": "Model not trained",
            "error": "Run train_model.py first with a dataset"
        }
    
    try:
        # Check trusted domains first
        if is_trusted_domain(url):
            return {
                "risk_level": "Low",
                "confidence": 0.99,
                "prediction": "Benign",
                "note": "Known trusted domain"
            }
        
        features = extract_features(url)
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][prediction]

        if probability > 0.8:
            risk = "High"
        elif probability > 0.5:
            risk = "Medium"
        else:
            risk = "Low"

        return {
            "risk_level": risk,
            "confidence": round(probability, 2),
            "prediction": "Malicious" if prediction == 1 else "Benign",
        }
    except Exception as e:
        return {
            "risk_level": "Error",
            "confidence": 0.0,
            "prediction": "Analysis failed",
            "error": str(e)
        }
