import React from "react";
import { TechnicalInfo } from "../types";

interface TechnicalTabProps {
    data: TechnicalInfo | null;
}

const TechnicalTab: React.FC<TechnicalTabProps> = ({ data }) => {
    if (!data) {
        return (
            <div className="text-slate-500 text-sm text-center py-8">
                Technical information unavailable.
            </div>
        );
    }

    const cardStyle = "bg-white/5 border border-white/10 p-5 rounded-xl flex flex-col transition-all duration-300 hover:bg-white/10 hover:scale-[1.02] hover:border-white/20 backdrop-blur-md";
    const labelStyle = "text-slate-500 text-[10px] font-bold uppercase tracking-wider mb-2";
    const valueStyle = "text-slate-200 text-sm font-medium";

    return (
        <div className="space-y-4 animate-in fade-in duration-500">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                <span className="w-2 h-2 bg-cyan-500 rounded-full"></span>
                Infrastructure Details
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Server */}
                <div className={cardStyle}>
                    <span className={labelStyle}>Server</span>
                    <span className={valueStyle}>{data.server || "Unknown"}</span>
                </div>

                {/* HTTPS Status */}
                <div className={cardStyle}>
                    <span className={labelStyle}>HTTPS</span>
                    <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${data.https ? 'bg-green-500' : 'bg-red-500'}`} />
                        <span className={valueStyle}>{data.https ? "Enabled" : "Disabled"}</span>
                    </div>
                </div>

                {/* TLS Version */}
                <div className={cardStyle}>
                    <span className={labelStyle}>TLS Version</span>
                    <span className={`${valueStyle} ${data.tls_version?.includes('1.3') ? 'text-green-400' : data.tls_version?.includes('1.2') ? 'text-yellow-400' : 'text-slate-200'}`}>
                        {data.tls_version || "Unknown"}
                    </span>
                </div>

                {/* IP Address */}
                <div className={cardStyle}>
                    <span className={labelStyle}>IP Address</span>
                    <span className={`${valueStyle} font-mono`}>{data.ip_address || "Unknown"}</span>
                </div>

                {/* CDN */}
                <div className={cardStyle}>
                    <span className={labelStyle}>CDN</span>
                    <span className={`${valueStyle} ${data.cdn !== 'None detected' ? 'text-blue-400' : ''}`}>
                        {data.cdn || "None detected"}
                    </span>
                </div>

                {/* Hosting */}
                <div className={cardStyle}>
                    <span className={labelStyle}>Hosting Provider</span>
                    <span className={`${valueStyle} ${data.hosting !== 'Unknown' ? 'text-purple-400' : ''}`}>
                        {data.hosting || "Unknown"}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default TechnicalTab;
