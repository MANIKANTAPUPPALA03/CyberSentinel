
import React, { useState } from 'react';

interface URLInputProps {
  onAnalyze: (url: string) => void;
  isLoading: boolean;
}

const URLInput: React.FC<URLInputProps> = ({ onAnalyze, isLoading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onAnalyze(url.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-4 mb-8">
      <div className="relative group">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL (e.g., example.com)"
          className="w-full bg-slate-950/50 border border-slate-700 text-white px-4 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500/30 focus:border-green-500 transition-all placeholder:text-slate-600"
          required
        />
      </div>
      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-3 px-6 rounded-xl font-bold transition-all flex items-center justify-center gap-2 ${
          isLoading 
            ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
            : 'bg-green-600 hover:bg-green-500 text-white shadow-lg shadow-green-900/10 active:scale-95'
        }`}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin h-5 w-5 mr-3 border-b-2 border-white rounded-full" viewBox="0 0 24 24"></svg>
            Analyzing Systems...
          </>
        ) : (
          'Analyze Website'
        )}
      </button>
    </form>
  );
};

export default URLInput;
