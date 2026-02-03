"""
Reputation Analysis Service
ML-assisted reputation classification using domain features.

Approach: Hybrid ML + Heuristic
- Uses features from basic_info and domain_info
- Runs lightweight scoring model
- Returns reputation label, score, confidence, and risk factors
"""

from datetime import datetime
from typing import Dict, List, Any


def analyze_reputation(basic_info: Dict, domain_info: Dict, security_info: Dict, ml_analysis: Dict) -> Dict[str, Any]:
    """
    Analyze website reputation using ML-assisted scoring.
    
    Uses multiple signals:
    - Domain age (older = more trusted)
    - SSL/HTTPS status
    - Known suspicious TLDs
    - ML prediction from url analysis
    - WHOIS privacy status
    """
    
    score = 50  # Start neutral
    risk_factors: List[str] = []
    positive_factors: List[str] = []
    
    # --- Feature 1: Domain Age Analysis ---
    domain_age = domain_info.get("domain_age_years")
    if domain_age is not None:
        if domain_age >= 5:
            score += 15
            positive_factors.append(f"Domain age: {domain_age:.1f} years (established)")
        elif domain_age >= 2:
            score += 8
            positive_factors.append(f"Domain age: {domain_age:.1f} years (moderate)")
        elif domain_age >= 0.5:
            score += 2
        else:
            score -= 15
            risk_factors.append(f"Very new domain: {domain_age:.2f} years")
    else:
        risk_factors.append("Domain age unknown")
    
    # --- Feature 2: HTTPS/SSL Analysis ---
    ssl_status = security_info.get("ssl", "")
    has_https = security_info.get("https", False)
    
    if "Valid" in ssl_status and has_https:
        score += 15
        positive_factors.append("HTTPS enabled with valid SSL")
    elif has_https:
        score += 5
        positive_factors.append("HTTPS enabled")
    else:
        score -= 20
        risk_factors.append("No HTTPS/SSL protection")
    
    # --- Feature 3: Security Headers ---
    headers = security_info.get("headers", [])
    if len(headers) >= 2:
        score += 10
        positive_factors.append(f"Security headers: {', '.join(headers)}")
    elif len(headers) == 1:
        score += 5
    else:
        risk_factors.append("Missing security headers")
    
    # --- Feature 4: HSTS ---
    if security_info.get("hsts"):
        score += 5
        positive_factors.append("HSTS enforced")
    
    # --- Feature 5: ML Prediction Integration ---
    ml_prediction = ml_analysis.get("prediction", "")
    ml_confidence = ml_analysis.get("confidence", 0)
    ml_risk = ml_analysis.get("risk_level", "")
    
    if ml_prediction == "Benign":
        ml_boost = int(ml_confidence * 20)  # Up to +20 for high confidence benign
        score += ml_boost
        if ml_confidence >= 0.8:
            positive_factors.append(f"ML classified as Benign ({int(ml_confidence*100)}% confidence)")
    elif ml_prediction == "Malicious":
        ml_penalty = int(ml_confidence * 30)  # Up to -30 for high confidence malicious
        score -= ml_penalty
        risk_factors.append(f"ML flagged as Malicious ({int(ml_confidence*100)}% confidence)")
    
    # --- Feature 6: Suspicious TLD Check ---
    domain = basic_info.get("domain", "").lower()
    suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".work", ".click", ".link", ".info", ".online", ".buzz"]
    trusted_tlds = [".gov", ".edu", ".org", ".com", ".net", ".io"]
    
    if any(domain.endswith(tld) for tld in suspicious_tlds):
        score -= 15
        risk_factors.append("Suspicious TLD detected")
    elif any(domain.endswith(tld) for tld in trusted_tlds[:3]):  # .gov, .edu, .org
        score += 10
        positive_factors.append("Trusted TLD")
    
    # --- Feature 7: WHOIS Privacy ---
    whois_privacy = domain_info.get("whois_privacy")
    if whois_privacy:
        score -= 5  # Slight penalty, not always bad
        risk_factors.append("WHOIS privacy enabled (owner hidden)")
    elif whois_privacy is False:
        score += 5
        positive_factors.append("WHOIS information public")
    
    # --- Feature 8: Known Domain Patterns ---
    trusted_domains = ["google", "microsoft", "apple", "amazon", "github", "facebook", "twitter", "linkedin"]
    if any(td in domain for td in trusted_domains):
        score += 20
        positive_factors.append("Known trusted domain")
    
    # --- Clamp Score ---
    score = max(0, min(100, score))
    
    # --- Determine Label ---
    if score >= 70:
        label = "Trusted"
    elif score >= 40:
        label = "Suspicious"
    else:
        label = "Malicious"
    
    # --- Calculate Confidence ---
    # Confidence based on how many factors we could analyze
    factors_analyzed = len(risk_factors) + len(positive_factors)
    confidence = min(0.95, 0.5 + (factors_analyzed * 0.05))
    
    # Combine factors for display (risk first, then positive)
    all_factors = risk_factors + positive_factors
    
    return {
        "label": label,
        "score": score,
        "confidence": round(confidence, 2),
        "risk_factors": all_factors[:6],  # Limit to 6 factors for UI
    }
