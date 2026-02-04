"""
Technical Info Service
Extracts passive infrastructure details from URLs.

Gathers:
- Server header
- HTTPS status
- TLS version
- CDN detection
- Hosting provider
- IP address
"""

import ssl
import socket
import requests
from urllib.parse import urlparse
from typing import Dict, Any


# Common CDN signatures in headers or response
CDN_SIGNATURES = {
    "cloudflare": ["cloudflare", "cf-ray"],
    "akamai": ["akamai", "akamaized"],
    "fastly": ["fastly", "x-served-by"],
    "amazon cloudfront": ["cloudfront", "x-amz-cf"],
    "google cloud cdn": ["google", "x-goog"],
    "microsoft azure": ["azure", "x-azure"],
    "cloudflare": ["__cfduid"],
    "incapsula": ["incap_ses", "visid_incap"],
}

# Hosting detection based on IP ranges or server headers
HOSTING_SIGNATURES = {
    "Amazon AWS": ["amazonaws", "aws", "ec2"],
    "Google Cloud": ["google", "gcp", "appspot"],
    "Microsoft Azure": ["azure", "microsoft", "windows-azure"],
    "DigitalOcean": ["digitalocean"],
    "Cloudflare": ["cloudflare"],
    "Heroku": ["heroku"],
    "Vercel": ["vercel"],
    "Netlify": ["netlify"],
    "GitHub Pages": ["github.io", "github"],
}


def detect_cdn(headers: Dict[str, str], server: str) -> str:
    """Detect CDN from response headers."""
    headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
    all_values = " ".join(headers_lower.values()) + " " + " ".join(headers_lower.keys())
    
    for cdn_name, signatures in CDN_SIGNATURES.items():
        for sig in signatures:
            if sig in all_values or sig in server.lower():
                return cdn_name.title()
    
    return "None detected"


def detect_hosting(server: str, ip_address: str, headers: Dict[str, str]) -> str:
    """Detect hosting provider from server header and IP info."""
    combined = (server + " " + " ".join(headers.values())).lower()
    
    for host_name, signatures in HOSTING_SIGNATURES.items():
        for sig in signatures:
            if sig in combined:
                return host_name
    
    return "Unknown"


def get_tls_version(domain: str) -> str:
    """Get TLS version used by the server."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                return ssock.version() or "Unknown"
    except Exception:
        return "Unknown"


def extract_technical_info(url: str, basic_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract technical infrastructure details from URL.
    Uses passive inspection only - no scanning or intrusive methods.
    """
    
    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    parsed = urlparse(url)
    domain = parsed.netloc
    
    result = {
        "server": "Unknown",
        "https": parsed.scheme == "https",
        "tls_version": "Unknown",
        "cdn": "None detected",
        "hosting": "Unknown",
        "ip_address": basic_info.get("ip_address", "Unknown"),
    }
    
    try:
        # Make request to get headers
        response = requests.head(url, timeout=2, allow_redirects=True)
        headers = dict(response.headers)
        
        # Extract server header
        result["server"] = headers.get("Server", headers.get("server", "Unknown"))
        
        # Detect CDN from headers
        result["cdn"] = detect_cdn(headers, result["server"])
        
        # Detect hosting provider
        result["hosting"] = detect_hosting(result["server"], result["ip_address"], headers)
        
    except Exception as e:
        print(f"[Technical] Error fetching headers: {e}")
    
    # Get TLS version for HTTPS sites
    if result["https"]:
        result["tls_version"] = get_tls_version(domain)
    else:
        result["tls_version"] = "N/A (HTTP)"
    
    return result
