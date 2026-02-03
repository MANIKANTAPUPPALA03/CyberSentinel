import React from "react";
import { ReputationInfo } from "../types";

interface ReputationTabProps {
  data: ReputationInfo | null;
}

const ReputationTab: React.FC<ReputationTabProps> = ({ data }) => {
  if (!data) {
    return (
      <div className="text-slate-500 text-sm text-center py-8">
        Reputation analysis unavailable.
      </div>
    );
  }

  // Label colors
  const getLabelStyle = (label: string) => {
    switch (label) {
      case "Trusted":
        return "bg-green-500/20 text-green-400 border-green-500/50";
      case "Suspicious":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/50";
      case "Malicious":
        return "bg-red-500/20 text-red-400 border-red-500/50";
      default:
        return "bg-slate-500/20 text-slate-400 border-slate-500/50";
    }
  };

  // Score bar color
  const getScoreColor = (score: number) => {
    if (score >= 70) return "from-green-500 to-emerald-400";
    if (score >= 40) return "from-yellow-500 to-orange-400";
    return "from-red-500 to-rose-400";
  };

  const cardStyle = "bg-white/5 border border-white/10 p-5 rounded-xl transition-all duration-300 hover:bg-white/10 backdrop-blur-md";

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Main Reputation Card */}
      <div className={`${cardStyle} flex flex-col md:flex-row md:items-center md:justify-between gap-4`}>
        <div>
          <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block mb-2">
            Reputation Status
          </span>
          <span className={`inline-block px-4 py-2 rounded-lg text-lg font-bold border ${getLabelStyle(data.label)}`}>
            {data.label}
          </span>
        </div>

        <div className="flex-1 max-w-xs">
          <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block mb-2">
            Trust Score
          </span>
          <div className="flex items-center gap-3">
            <div className="flex-1 h-3 bg-slate-700 rounded-full overflow-hidden">
              <div
                className={`h-full bg-gradient-to-r ${getScoreColor(data.score)} rounded-full transition-all duration-700`}
                style={{ width: `${data.score}%` }}
              />
            </div>
            <span className="text-2xl font-bold text-slate-200">{data.score}</span>
          </div>
        </div>

        <div>
          <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block mb-2">
            Confidence
          </span>
          <span className="text-slate-200 text-lg font-medium">
            {Math.round(data.confidence * 100)}%
          </span>
        </div>
      </div>

      {/* Risk Factors */}
      <div className={cardStyle}>
        <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block mb-3">
          Analysis Factors
        </span>
        <div className="space-y-2">
          {data.risk_factors.length > 0 ? (
            data.risk_factors.map((factor, idx) => {
              const isPositive = factor.includes("enabled") ||
                factor.includes("Trusted") ||
                factor.includes("Benign") ||
                factor.includes("years") && !factor.includes("Very new") ||
                factor.includes("public") ||
                factor.includes("headers");

              return (
                <div
                  key={idx}
                  className={`flex items-center gap-2 p-2 rounded-lg ${isPositive
                      ? 'bg-green-500/10 border border-green-500/20'
                      : 'bg-red-500/10 border border-red-500/20'
                    }`}
                >
                  <span className={`text-lg ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                    {isPositive ? '✓' : '⚠'}
                  </span>
                  <span className={`text-sm ${isPositive ? 'text-green-300' : 'text-red-300'}`}>
                    {factor}
                  </span>
                </div>
              );
            })
          ) : (
            <span className="text-slate-500 text-sm italic">No specific factors detected</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReputationTab;
