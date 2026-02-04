"""
Domain Info Service - WHOIS Lookup
Uses python-whois with fallback for Windows systems
"""

import whois
from datetime import datetime
import socket
import traceback
import os


def extract_domain_info(domain: str):
    """Extract domain registration info via WHOIS lookup."""
    
    # Clean domain (remove trailing slash, etc.)
    domain = domain.strip().lower()
    if domain.startswith("www."):
        domain = domain[4:]
    
    result = {
        "domain": domain,
        "creation_date": "Unknown",
        "expiration_date": "Unknown",
        "domain_age_years": None,
        "registrar": "Unknown",
        "whois_privacy": False,
    }
    
    # Skip WHOIS on Render to prevent timeout/blocking (Port 43 is blocked)
    if os.environ.get("RENDER"):
        print("[WHOIS] Skipping WHOIS on Render environment (Port 43 blocked)")
        return result
    
    try:
        print(f"[WHOIS] Looking up: {domain}")
        w = whois.whois(domain)
        print(f"[WHOIS] Raw response type: {type(w)}")
        
        if w is None:
            print("[WHOIS] Response is None")
            return result
        
        # Debug: print raw data
        print(f"[WHOIS] creation_date: {w.creation_date}")
        print(f"[WHOIS] registrar: {w.registrar}")
        
        # Extract creation date
        creation_date = w.creation_date
        if isinstance(creation_date, list) and len(creation_date) > 0:
            creation_date = creation_date[0]
        
        # Extract expiration date
        expiration_date = w.expiration_date
        if isinstance(expiration_date, list) and len(expiration_date) > 0:
            expiration_date = expiration_date[0]
        
        # Extract registrar
        registrar = w.registrar
        
        # Calculate domain age
        domain_age_years = None
        if creation_date:
            try:
                if isinstance(creation_date, datetime):
                    # datetime with timezone - convert to naive
                    if creation_date.tzinfo is not None:
                        creation_date = creation_date.replace(tzinfo=None)
                    domain_age_years = round(
                        (datetime.utcnow() - creation_date).days / 365, 2
                    )
                    result["creation_date"] = creation_date.strftime("%Y-%m-%d")
                else:
                    result["creation_date"] = str(creation_date)
            except Exception as e:
                print(f"[WHOIS] Date parsing error: {e}")
                result["creation_date"] = str(creation_date)
        
        if expiration_date:
            try:
                if isinstance(expiration_date, datetime):
                    if expiration_date.tzinfo is not None:
                        expiration_date = expiration_date.replace(tzinfo=None)
                    result["expiration_date"] = expiration_date.strftime("%Y-%m-%d")
                else:
                    result["expiration_date"] = str(expiration_date)
            except Exception as e:
                print(f"[WHOIS] Expiry parsing error: {e}")
                result["expiration_date"] = str(expiration_date)
        
        result["domain_age_years"] = domain_age_years
        result["registrar"] = registrar if registrar else "Unknown"
        
        # WHOIS privacy detection
        org = getattr(w, 'org', None) or getattr(w, 'name', None) or ""
        if org:
            privacy_keywords = ["privacy", "protect", "redacted", "proxy", "guard", "private"]
            result["whois_privacy"] = any(keyword in str(org).lower() for keyword in privacy_keywords)
        
        print(f"[WHOIS] Final result: {result}")
        return result
        
    except Exception as e:
        # Log error but return defaults
        print(f"[WHOIS] ERROR for {domain}: {e}")
        traceback.print_exc()
        return result
