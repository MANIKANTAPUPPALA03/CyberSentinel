import React, { useState } from "react";
import Header from "./components/Header";
import URLInput from "./components/URLInput";
import TrustScore from "./components/TrustScore";
import Tabs from "./components/Tabs";
import OverviewTab from "./components/OverviewTab";
import DomainTab from "./components/DomainTab";
import ReputationTab from "./components/ReputationTab";
import SecurityTab from "./components/SecurityTab";
import TechnicalTab from "./components/TechnicalTab";
import { AnalysisResult, TabType } from "./types";
import { analyzeUrl } from "./services/apiService";

const App: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>("Overview");
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (url: string) => {
    setLoading(true);
    setError(null);

    try {
      const data = await analyzeUrl(url);

      setResult({
        status: "Analyzed",
        trustScore: data.reputation?.score ?? 50,
        basic_info: data.basic_info,
        domain_info: data.domain_info,
        security_info: data.security_info,
        ml_analysis: data.ml_analysis,
        reputation: data.reputation,
        threat_intelligence: data.threat_intelligence,
        technical_info: data.technical_info,
        rawJson: data,
      });

      setActiveTab("Overview");
    } catch (err) {
      console.error(err);
      setError(
        "Analysis failed. The service could not reach the backend endpoint."
      );
    } finally {
      setLoading(false);
    }
  };

  const renderTabContent = () => {
    if (!result) return null;

    switch (activeTab) {
      case "Overview":
        return <OverviewTab data={result.basic_info} />;

      case "Domain":
        return <DomainTab data={result.domain_info} />;

      case "Security":
        return <SecurityTab data={result.security_info} mlData={result.ml_analysis} threatData={result.threat_intelligence} />;

      case "Reputation":
        return <ReputationTab data={result.reputation} />;

      case "Technical":
        return <TechnicalTab data={result.technical_info} />;

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen relative text-slate-200 flex flex-col items-center p-4 md:p-8">
      {/* Background */}
      <div
        className="fixed inset-0 z-0 bg-cover bg-center brightness-[0.15]"
        style={{
          backgroundImage:
            'url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b")',
        }}
      />

      <div className="w-full max-w-2xl bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-6 md:p-10 relative z-10">
        <Header />

        <URLInput onAnalyze={handleAnalyze} isLoading={loading} />

        {error && (
          <div className="mt-4 p-3 bg-red-950/40 border border-red-800/40 rounded-lg text-red-300 text-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-6 animate-in fade-in duration-500">
            <TrustScore
              status={result.status}
              score={result.trustScore}
            />

            <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

            <div className="mt-4 min-h-[260px]">{renderTabContent()}</div>
          </div>
        )}

        {!result && !loading && !error && (
          <div className="mt-10 text-center text-slate-500 text-sm">
            Enter a website URL to start analysis
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
