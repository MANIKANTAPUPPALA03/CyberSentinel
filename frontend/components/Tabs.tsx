
import React from 'react';
import { TabType } from '../types';

interface TabsProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

const Tabs: React.FC<TabsProps> = ({ activeTab, setActiveTab }) => {
  const tabs: TabType[] = ['Overview', 'Security', 'Domain', 'Technical', 'Reputation'];

  return (
    <div className="w-full flex mb-6 border-b border-slate-800/60 pb-px">
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => setActiveTab(tab)}
          className={`flex-1 py-3 text-sm font-semibold transition-all relative group ${
            activeTab === tab
              ? 'text-white'
              : 'text-slate-500 hover:text-slate-300'
          }`}
        >
          {tab}
          <div className={`absolute bottom-0 left-0 right-0 h-0.5 transition-all duration-300 ${
            activeTab === tab 
              ? 'bg-green-500 scale-x-100' 
              : 'bg-slate-700 scale-x-0 group-hover:scale-x-50'
          }`} />
        </button>
      ))}
    </div>
  );
};

export default Tabs;
