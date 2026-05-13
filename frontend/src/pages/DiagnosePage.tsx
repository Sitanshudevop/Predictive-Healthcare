import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { Brain, HeartPulse, Scan, AlertTriangle } from "lucide-react";
import NLPTab from "../components/diagnose/NLPTab";
import BiometricsTab from "../components/diagnose/BiometricsTab";
import ImagingTab from "../components/diagnose/ImagingTab";

const TABS = [
  { id: "nlp", label: "NLP Symptom Parser", icon: Brain, desc: "Describe symptoms in natural language" },
  { id: "biometrics", label: "Biometric Analysis", icon: HeartPulse, desc: "Enter vitals for organ-specific models" },
  { id: "imaging", label: "Image Lab", icon: Scan, desc: "Upload X-ray or skin images" },
];

export default function DiagnosePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState(searchParams.get("tab") || "nlp");

  useEffect(() => {
    const t = searchParams.get("tab");
    if (t && TABS.find((tab) => tab.id === t)) setActiveTab(t);
  }, [searchParams]);

  const handleTabChange = (id: string) => {
    setActiveTab(id);
    setSearchParams({ tab: id });
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Diagnostic Engine</h1>
          <p className="text-slate-400 text-sm">AI-powered multi-model analysis across 11 specialized predictors</p>
        </div>

        {/* Tab Bar */}
        <div className="tab-bar mb-8 flex-wrap">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabChange(tab.id)}
              className={`tab-item flex items-center gap-2 ${activeTab === tab.id ? "active" : ""}`}
            >
              <tab.icon className="w-4 h-4" />
              <span className="hidden sm:inline">{tab.label}</span>
              <span className="sm:hidden">{tab.id.toUpperCase()}</span>
            </button>
          ))}
        </div>

        {/* Disclaimer Banner */}
        <div className="glass-panel p-3 mb-6 flex items-center gap-3 border-amber-500/15">
          <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0" />
          <p className="text-xs text-slate-500">
            <strong className="text-amber-400/80">Disclaimer:</strong> Results are AI-generated predictions for educational purposes only. Consult a healthcare professional for medical advice.
          </p>
        </div>

        {/* Tab Content */}
        <div className="min-h-[500px]">
          {activeTab === "nlp" && <NLPTab />}
          {activeTab === "biometrics" && <BiometricsTab />}
          {activeTab === "imaging" && <ImagingTab />}
        </div>
      </div>
    </div>
  );
}
