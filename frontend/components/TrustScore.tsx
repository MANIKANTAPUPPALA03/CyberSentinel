
import React from 'react';

interface TrustScoreProps {
  status: string;
  score: number;
}

const TrustScore: React.FC<TrustScoreProps> = ({ status, score }) => {
  const isSafe = score > 60;
  
  return (
    <div className="text-center space-y-2 mb-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <h2 className="text-2xl font-bold text-white flex items-center justify-center gap-2">
        Status: <span className={isSafe ? 'text-green-400' : 'text-red-400'}>{status}</span>
      </h2>
      <p className="text-slate-400 font-semibold tracking-wide uppercase text-xs">
        Overall Trust Score: {score}/100
      </p>
      <div className="w-full bg-slate-800/50 h-2.5 rounded-full mt-2 overflow-hidden border border-slate-700/30">
        <div 
          className={`h-full transition-all duration-1000 ease-out rounded-full ${isSafe ? 'bg-green-500' : 'bg-red-500'}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
};

export default TrustScore;
