import React from "react";
import { BasicInfo } from "../types";

interface OverviewTabProps {
  data: BasicInfo | null;
}

const OverviewTab: React.FC<OverviewTabProps> = ({ data }) => {
  if (!data) {
    return (
      <div className="text-slate-500 text-sm text-center py-8">
        No data available
      </div>
    );
  }

  const fields = [
    { label: "Domain", value: data.domain, color: "text-blue-400" },
    { label: "IP Address", value: data.ip_address, color: "text-slate-300" },
    { label: "Country", value: data.country, color: "text-slate-300" },
    { label: "ISP", value: data.isp, color: "text-slate-300" },
    { label: "Protocol", value: data.protocol.toUpperCase(), color: "text-green-400" },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="bg-slate-950/30 p-5 rounded-xl border border-slate-800/40 hover:border-slate-700 transition-colors">
        <p className="text-slate-400 text-sm leading-relaxed italic">
          Target domain{" "}
          <span className="text-blue-400 font-mono font-bold">{data.domain}</span>{" "}
          has been analyzed. The server is located in{" "}
          <span className="text-slate-300 font-semibold">{data.country}</span>{" "}
          and hosted by <span className="text-slate-300">{data.isp}</span>.
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {fields.map((field) => (
          <div
            key={field.label}
            className="bg-slate-950/40 p-3 rounded-lg border border-slate-800/30 text-center transition-all duration-300 hover:scale-[1.05] hover:border-slate-600 hover:bg-slate-900/50 cursor-default"
          >
            <p className="text-[10px] text-slate-600 font-bold uppercase mb-1">
              {field.label}
            </p>
            <p className={`text-xs font-semibold ${field.color} break-all`}>
              {field.value || "N/A"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default OverviewTab;
