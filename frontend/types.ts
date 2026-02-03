// Basic info from backend Feature 1
export interface BasicInfo {
  url: string;
  protocol: string;
  domain: string;
  ip_address: string;
  country: string;
  isp: string;
}

// Domain info from backend Feature 2
export interface DomainInfo {
  domain: string;
  creation_date: string;
  expiration_date: string;
  domain_age_years: number | null;
  registrar: string;
  whois_privacy: boolean | null;
}

// Security info from backend Feature 3
export interface SecurityInfo {
  ssl: string;
  https: boolean;
  issuer: string;
  expiry: string;
  hsts: boolean;
  headers: string[];
}

// ML Analysis from backend
export interface MLAnalysis {
  risk_level: string;
  confidence: number;
  prediction: string;
  error?: string;
  note?: string;
}

// Reputation Analysis from backend
export interface ReputationInfo {
  label: string;
  score: number;
  confidence: number;
  risk_factors: string[];
}

// Threat Intelligence from backend Feature 4
export interface SafeBrowsingResult {
  status: string;
  threats?: string[];
  error?: string;
}

export interface VirusTotalResult {
  status: string;
  malicious_count?: number;
  suspicious_count?: number;
  harmless_count?: number;
  total_engines?: number;
  error?: string;
  note?: string;
}

export interface ThreatIntelligence {
  safe_browsing: SafeBrowsingResult;
  virus_total: VirusTotalResult;
  final_threat_level: string;
}

// Technical Info from backend
export interface TechnicalInfo {
  server: string;
  https: boolean;
  tls_version: string;
  cdn: string;
  hosting: string;
  ip_address: string;
}

// Full analysis result
export interface AnalysisResult {
  status: string;
  trustScore: number;
  basic_info: BasicInfo | null;
  domain_info: DomainInfo | null;
  security_info: SecurityInfo | null;
  ml_analysis: MLAnalysis | null;
  reputation: ReputationInfo | null;
  threat_intelligence: ThreatIntelligence | null;
  technical_info: TechnicalInfo | null;
  rawJson: unknown;
}

export type TabType = 'Overview' | 'Security' | 'Domain' | 'Technical' | 'Reputation';
