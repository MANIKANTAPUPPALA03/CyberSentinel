
import React from 'react';

interface JsonViewerProps {
  data: any;
}

const JsonViewer: React.FC<JsonViewerProps> = ({ data }) => {
  return (
    <div className="mt-8 bg-slate-950 p-6 rounded-lg border border-slate-800 font-mono text-xs overflow-x-auto shadow-inner">
      <pre className="text-green-500/90 leading-relaxed">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
};

export default JsonViewer;
