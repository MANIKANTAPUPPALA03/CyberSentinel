import socket
import requests
from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def extract_basic_info(url: str):
    # Normalize URL
    url = normalize_url(url)

    parsed = urlparse(url)
    domain = parsed.netloc
    protocol = parsed.scheme

    # Resolve IP address
    try:
        ip_address = socket.gethostbyname(domain)
    except Exception:
        ip_address = "Unavailable"

    # IP Geolocation (free API)
    country = "Unknown"
    isp = "Unknown"

    if ip_address != "Unavailable":
        try:
            response = requests.get(f"https://ipinfo.io/{ip_address}/json", timeout=5)
            data = response.json()
            country = data.get("country", "Unknown")
            isp = data.get("org", "Unknown")
        except Exception:
            pass

    return {
        "url": url,
        "protocol": protocol,
        "domain": domain,
        "ip_address": ip_address,
        "country": country,
        "isp": isp
    }
