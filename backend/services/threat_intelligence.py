"""
Threat Intelligence Service
Real-time security checks using trusted threat-intelligence APIs.

Integrates:
- Google Safe Browsing API
- VirusTotal API
"""

import os
import requests
import hashlib
import base64
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# API Keys from environment
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY", "")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")


def check_google_safe_browsing(url: str) -> Dict[str, Any]:
    """
    Check URL against Google Safe Browsing API.
    Detects: malware, social engineering, unwanted software, potentially harmful apps.
    """
    if not GOOGLE_SAFE_BROWSING_API_KEY:
        return {
            "status": "Unavailable",
            "error": "API key not configured"
        }
    
    try:
        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
        
        payload = {
            "client": {
                "clientId": "cybersentinel",
                "clientVersion": "1.0.0"
            },
            "threatInfo": {
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        
        response = requests.post(api_url, json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            if "matches" in data and len(data["matches"]) > 0:
                # URL found in threat database
                threat_types = [m.get("threatType", "UNKNOWN") for m in data["matches"]]
                return {
                    "status": "Unsafe",
                    "threats": threat_types
                }
            else:
                return {
                    "status": "Safe"
                }
        else:
            return {
                "status": "Error",
                "error": f"API returned {response.status_code}"
            }
            
    except requests.Timeout:
        return {
            "status": "Timeout",
            "error": "API request timed out"
        }
    except Exception as e:
        return {
            "status": "Error",
            "error": str(e)
        }


def check_virustotal(url: str) -> Dict[str, Any]:
    """
    Check URL against VirusTotal API.
    Returns aggregated results from multiple security vendors.
    """
    if not VIRUSTOTAL_API_KEY:
        return {
            "status": "Unavailable",
            "error": "API key not configured"
        }
    
    try:
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        
        # URL must be base64 encoded (without padding) for VirusTotal
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        
        api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0)
            undetected = stats.get("undetected", 0)
            total = malicious + suspicious + harmless + undetected
            
            return {
                "status": "Checked",
                "malicious_count": malicious,
                "suspicious_count": suspicious,
                "harmless_count": harmless,
                "total_engines": total
            }
        elif response.status_code == 404:
            # URL not in VirusTotal database - submit for analysis
            return {
                "status": "Not Found",
                "note": "URL not previously scanned"
            }
        else:
            return {
                "status": "Error",
                "error": f"API returned {response.status_code}"
            }
            
    except requests.Timeout:
        return {
            "status": "Timeout",
            "error": "API request timed out"
        }
    except Exception as e:
        return {
            "status": "Error",
            "error": str(e)
        }


def get_threat_intelligence(url: str) -> Dict[str, Any]:
    """
    Main function to get threat intelligence from all sources.
    Combines results and determines final threat level.
    """
    
    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    # Query both APIs
    safe_browsing = check_google_safe_browsing(url)
    virus_total = check_virustotal(url)
    
    # Determine final threat level
    threat_level = "Low"
    
    # Check Google Safe Browsing result
    if safe_browsing.get("status") == "Unsafe":
        threat_level = "High"
    
    # Check VirusTotal result
    vt_malicious = virus_total.get("malicious_count", 0)
    vt_suspicious = virus_total.get("suspicious_count", 0)
    
    if vt_malicious >= 5:
        threat_level = "High"
    elif vt_malicious >= 1 or vt_suspicious >= 3:
        if threat_level != "High":
            threat_level = "Medium"
    
    return {
        "safe_browsing": safe_browsing,
        "virus_total": virus_total,
        "final_threat_level": threat_level
    }
