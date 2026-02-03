import ssl
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime

def extract_security_info(url: str):
    info = {
         "ssl": "Invalid/Missing",
         "https": False,
         "issuer": "Unknown",
         "expiry": "Unknown",
         "hsts": False,
         "headers": []
    }
    
    # URL Normalization
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        info["https"] = parsed.scheme == "https"
        
        # Valid host check
        if not domain:
             return info
    except:
        return info

    # SSL Check
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=3) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                info["ssl"] = "Valid"
                
                # Issuer
                # cert['issuer'] is tuple of tuples
                issuer_dict = {k: v for t in cert['issuer'] for k, v in t}
                info["issuer"] = issuer_dict.get('organizationName', 'Unknown')
                
                # Expiry
                not_after = cert['notAfter']
                dt = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                days = (dt - datetime.utcnow()).days
                info["expiry"] = f"{days} days"
    except ssl.SSLError:
        info["ssl"] = "Invalid (Cert Error)"
    except Exception:
        pass

    # Headers Check
    try:
        resp = requests.get(url, timeout=3)
        headers = resp.headers
        
        if headers.get("Strict-Transport-Security"):
            info["hsts"] = True
            info["headers"].append("HSTS")
            
        if headers.get("X-Frame-Options"):
             info["headers"].append("X-Frame")
             
        if headers.get("Content-Security-Policy"):
             info["headers"].append("CSP")
             
    except Exception:
        pass

    return info
