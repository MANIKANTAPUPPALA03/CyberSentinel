from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.basic_info import extract_basic_info
from services.domain_info import extract_domain_info
from services.security_checks import extract_security_info
from services.ml_analysis import analyze_with_ml
from services.reputation_analysis import analyze_reputation
from services.threat_intelligence import get_threat_intelligence
from services.technical_info import extract_technical_info

app = FastAPI(
    title="CyberSentinel Backend",
    description="Complete URL Analysis: Basic + Domain + Security + ML + Reputation + Threat Intel + Technical",
    version="1.2"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/analyze-url")
def analyze_url(request: URLRequest):
    if not request.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    # Feature 1: Basic Info
    basic_info = extract_basic_info(request.url)
    
    # Feature 2: Domain Info (WHOIS)
    domain_info = extract_domain_info(basic_info["domain"])
    
    # Feature 3a: Security Info (SSL/Headers)
    security_info = extract_security_info(basic_info["url"])
    
    # Feature 3b: ML-based URL Risk Analysis
    ml_analysis = analyze_with_ml(basic_info["url"])
    
    # Feature 3c: Reputation Analysis (ML-assisted)
    reputation = analyze_reputation(basic_info, domain_info, security_info, ml_analysis)
    
    # Feature 4: Threat Intelligence (Live API checks)
    threat_intelligence = get_threat_intelligence(basic_info["url"])
    
    # Technical Info: Server, TLS, CDN, Hosting
    technical_info = extract_technical_info(basic_info["url"], basic_info)

    return {
        "basic_info": basic_info,
        "domain_info": domain_info,
        "security_info": security_info,
        "ml_analysis": ml_analysis,
        "reputation": reputation,
        "threat_intelligence": threat_intelligence,
        "technical_info": technical_info
    }
