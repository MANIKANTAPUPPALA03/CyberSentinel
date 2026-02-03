import React, { useState } from 'react';
import { DomainInfo } from '../types';

interface DomainTabProps {
  data: DomainInfo | null;
}

const DomainTab: React.FC<DomainTabProps> = ({ data }) => {
  const [copied, setCopied] = useState(false);

  if (!data) {
    return (
      <div className="text-slate-500 text-sm text-center py-8">
        Domain details unavailable.
      </div>
    );
  }

  const handleCopy = (text: string) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const domainFields = [
    { label: 'Registered Domain', value: data.domain },
    { label: 'Registrar', value: data.registrar },
    { label: 'Creation Date', value: data.creation_date },
    { label: 'Expiration', value: data.expiration_date },
    { label: 'Age (Years)', value: data.domain_age_years?.toString() || 'Unknown' },
    { label: 'Privacy Protection', value: data.whois_privacy ? 'Enabled' : 'Disabled', color: data.whois_privacy ? 'text-green-400' : 'text-slate-400' },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {domainFields.map((field) => (
          <div key={field.label} className="p-4 bg-slate-950/30 border border-slate-800/50 rounded-xl hover:bg-slate-900/30 hover:border-slate-600 transition-all duration-300">
            <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider block mb-1">{field.label}</span>
            <span className={`text-slate-200 font-mono text-sm ${field.color || ''}`}>{field.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DomainTab;
