import React from 'react';
import { SecurityInfo, MLAnalysis, ThreatIntelligence } from '../types';

interface SecurityTabProps {
    data: SecurityInfo | null;
    mlData: MLAnalysis | null;
    threatData: ThreatIntelligence | null;
}

const SecurityTab: React.FC<SecurityTabProps> = ({ data, mlData, threatData }) => {
    if (!data && !mlData && !threatData) {
        return (
            <div className="text-slate-500 text-sm text-center py-8">
                Security analysis unavailable.
            </div>
        );
    }

    const cardStyle = "bg-white/5 border border-white/10 p-5 rounded-xl flex flex-col transition-all duration-300 hover:bg-white/10 hover:scale-[1.02] hover:border-white/20 backdrop-blur-md";
    const labelStyle = "text-slate-500 text-[10px] font-bold uppercase tracking-wider mb-2";
    const valueStyle = "text-slate-200 text-sm font-medium";

    // Risk/threat level colors
    const getRiskColor = (risk: string) => {
        switch (risk?.toLowerCase()) {
            case 'high': return 'text-red-400 bg-red-500/20 border-red-500/50';
            case 'medium': return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/50';
            case 'low': return 'text-green-400 bg-green-500/20 border-green-500/50';
            default: return 'text-slate-400 bg-slate-500/20 border-slate-500/50';
        }
    };

    const getPredictionColor = (pred: string) => {
        return pred === 'Benign' ? 'text-green-400' : 'text-red-400';
    };

    const getStatusColor = (status: string) => {
        switch (status?.toLowerCase()) {
            case 'safe':
            case 'checked':
                return 'text-green-400';
            case 'unsafe':
                return 'text-red-400';
            default:
                return 'text-yellow-400';
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Threat Intelligence Section - NEW */}
            {threatData && (
                <div className="mb-6">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                        <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                        Live Threat Intelligence
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Final Threat Level */}
                        <div className={`${cardStyle} border-l-4 ${getRiskColor(threatData.final_threat_level)}`}>
                            <span className={labelStyle}>Threat Level</span>
                            <span className={`text-lg font-bold ${getRiskColor(threatData.final_threat_level).split(' ')[0]}`}>
                                {threatData.final_threat_level}
                            </span>
                        </div>

                        {/* Google Safe Browsing */}
                        <div className={cardStyle}>
                            <span className={labelStyle}>Google Safe Browsing</span>
                            <span className={`${valueStyle} ${getStatusColor(threatData.safe_browsing?.status)}`}>
                                {threatData.safe_browsing?.status || 'Unknown'}
                            </span>
                            {threatData.safe_browsing?.threats && (
                                <span className="text-xs text-red-300 mt-1">
                                    {threatData.safe_browsing.threats.join(', ')}
                                </span>
                            )}
                        </div>

                        {/* VirusTotal */}
                        <div className={cardStyle}>
                            <span className={labelStyle}>VirusTotal</span>
                            {threatData.virus_total?.status === 'Checked' ? (
                                <div className="flex flex-col">
                                    <span className={valueStyle}>
                                        {threatData.virus_total.malicious_count || 0} / {threatData.virus_total.total_engines || 0} flagged
                                    </span>
                                    {(threatData.virus_total.malicious_count || 0) > 0 && (
                                        <span className="text-xs text-red-300 mt-1">
                                            {threatData.virus_total.malicious_count} malicious, {threatData.virus_total.suspicious_count || 0} suspicious
                                        </span>
                                    )}
                                </div>
                            ) : (
                                <span className={`${valueStyle} ${getStatusColor(threatData.virus_total?.status)}`}>
                                    {threatData.virus_total?.status || 'Unknown'}
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* ML Risk Analysis Section */}
            {mlData && (
                <div className="mb-6">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                        <span className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></span>
                        ML Risk Analysis
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className={`${cardStyle} border-l-4 ${getRiskColor(mlData.risk_level)}`}>
                            <span className={labelStyle}>Risk Level</span>
                            <span className={`text-lg font-bold ${getRiskColor(mlData.risk_level).split(' ')[0]}`}>
                                {mlData.risk_level}
                            </span>
                        </div>
                        <div className={cardStyle}>
                            <span className={labelStyle}>Prediction</span>
                            <span className={`${valueStyle} ${getPredictionColor(mlData.prediction)}`}>
                                {mlData.prediction}
                            </span>
                        </div>
                        <div className={cardStyle}>
                            <span className={labelStyle}>Confidence</span>
                            <div className="flex items-center gap-2">
                                <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-500"
                                        style={{ width: `${(mlData.confidence || 0) * 100}%` }}
                                    />
                                </div>
                                <span className={valueStyle}>{Math.round((mlData.confidence || 0) * 100)}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* SSL & Headers Section */}
            {data && (
                <>
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                        <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                        SSL & Headers
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className={cardStyle}>
                            <span className={labelStyle}>SSL Connection</span>
                            <div className="flex items-center gap-2">
                                <span className={`w-2 h-2 rounded-full ${data.ssl.includes('Valid') ? 'bg-green-500' : 'bg-red-500'}`} />
                                <span className={valueStyle}>{data.ssl}</span>
                            </div>
                        </div>

                        <div className={cardStyle}>
                            <span className={labelStyle}>Certificate Issuer</span>
                            <span className={valueStyle}>{data.issuer}</span>
                        </div>

                        <div className={cardStyle}>
                            <span className={labelStyle}>Expiry Status</span>
                            <span className={valueStyle}>{data.expiry}</span>
                        </div>

                        <div className={cardStyle}>
                            <span className={labelStyle}>HSTS Enforced</span>
                            <span className={valueStyle}>{data.hsts ? 'Yes' : 'No'}</span>
                        </div>

                        <div className={`col-span-1 md:col-span-2 ${cardStyle}`}>
                            <span className={labelStyle}>Secure Headers Detected</span>
                            <div className="flex gap-2 flex-wrap">
                                {data.headers.length > 0 ? (
                                    data.headers.map(h => (
                                        <span key={h} className="px-2 py-1 bg-slate-800 rounded-md text-xs font-mono text-blue-400 border border-slate-700">{h}</span>
                                    ))
                                ) : (
                                    <span className="text-slate-500 text-xs italic">No specific security headers found</span>
                                )}
                            </div>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default SecurityTab;
