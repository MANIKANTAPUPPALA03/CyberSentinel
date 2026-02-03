import re
from urllib.parse import urlparse
import math


def entropy(string):
    """Calculate Shannon entropy of a string to detect randomness."""
    if not string:
        return 0
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return -sum(p * math.log2(p) for p in prob)


def extract_features(url: str):
    """Extract enhanced lexical features from URL for ML classification."""
    try:
        parsed = urlparse(url if url.startswith(("http://", "https://")) else "https://" + url)
        domain = parsed.netloc
        path = parsed.path
        
        # Suspicious TLDs commonly used in phishing
        suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".work", ".click", ".link", ".info", ".online"]
        
        # Trusted domains (less likely to be phishing)
        trusted_domains = ["google", "facebook", "microsoft", "apple", "amazon", "paypal", "netflix"]
        
        features = {
            # Basic counts
            "url_length": len(url),
            "domain_length": len(domain),
            "path_length": len(path),
            "num_dots": url.count("."),
            "num_hyphens": url.count("-"),
            "num_underscores": url.count("_"),
            "num_slashes": url.count("/"),
            "num_at": url.count("@"),
            "num_question": url.count("?"),
            "num_ampersand": url.count("&"),
            "num_equals": url.count("="),
            "num_digits": sum(c.isdigit() for c in url),
            "num_special": sum(not c.isalnum() for c in url),
            
            # Protocol
            "has_https": 1 if parsed.scheme == "https" else 0,
            "has_http": 1 if parsed.scheme == "http" else 0,
            
            # Domain analysis
            "has_ip": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
            "subdomain_count": domain.count("."),
            "is_suspicious_tld": 1 if any(url.lower().endswith(tld) for tld in suspicious_tlds) else 0,
            "has_trusted_domain": 1 if any(td in domain.lower() for td in trusted_domains) else 0,
            
            # Entropy (randomness detection)
            "url_entropy": entropy(url),
            "domain_entropy": entropy(domain),
            
            # Suspicious patterns
            "suspicious_words": sum(
                word in url.lower()
                for word in ["login", "verify", "bank", "secure", "account", "update", "signin", "confirm", "password", "credential", "wallet", "suspend"]
            ),
            "has_login_keyword": 1 if any(w in url.lower() for w in ["login", "signin", "log-in", "sign-in"]) else 0,
            "has_security_keyword": 1 if any(w in url.lower() for w in ["secure", "security", "verify", "confirm"]) else 0,
            
            # URL structure anomalies
            "double_slash_in_path": 1 if "//" in path else 0,
            "has_at_symbol": 1 if "@" in url else 0,
            "digit_ratio": sum(c.isdigit() for c in url) / max(len(url), 1),
            "letter_ratio": sum(c.isalpha() for c in url) / max(len(url), 1),
            
            # Length anomalies
            "is_long_url": 1 if len(url) > 75 else 0,
            "is_short_domain": 1 if len(domain) < 5 else 0,
        }

        return list(features.values())
    except Exception:
        # Return zeros if parsing fails
        return [0] * 30


# Feature names for reference
FEATURE_NAMES = [
    "url_length", "domain_length", "path_length", "num_dots", "num_hyphens",
    "num_underscores", "num_slashes", "num_at", "num_question", "num_ampersand",
    "num_equals", "num_digits", "num_special", "has_https", "has_http",
    "has_ip", "subdomain_count", "is_suspicious_tld", "has_trusted_domain",
    "url_entropy", "domain_entropy", "suspicious_words", "has_login_keyword",
    "has_security_keyword", "double_slash_in_path", "has_at_symbol",
    "digit_ratio", "letter_ratio", "is_long_url", "is_short_domain"
]
