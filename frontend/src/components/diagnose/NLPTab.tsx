import { useState } from "react";
import { Brain, Send, Loader2, Sparkles, AlertCircle, Pill, Stethoscope, Activity } from "lucide-react";
import api from "../../lib/api";


interface ExtractedSymptom {
  symptom: string;
  negated: boolean;
  duration: string | null;
  severity_hint: string | null;
}

interface NLPExtractResult {
  symptoms: ExtractedSymptom[];
  raw_text: string;
  disclaimer?: string;
}

interface PredictionResult {
  prediction: string;
  confidence: number;
  top_k: { disease: string; confidence: number }[];
  severity_score: number;
  recommendation: any;
  disclaimer: string;
  model_name: string;
}

interface CombinedResult {
  extracted_symptoms: string[];
  predicted_disease: string;
  confidence: number;
  severity_score: number;
  top_k: { disease: string; confidence: number }[];
  specialist: string;
  disclaimer: string;
}

export default function NLPTab() {

  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CombinedResult | null>(null);
  const [error, setError] = useState("");

  const EXAMPLE_PROMPTS = [
    "I've been having headaches, fever, and body aches for 3 days",
    "Persistent dry cough with chest tightness and shortness of breath",
    "Feeling very tired, increased thirst, frequent urination, blurred vision",
    "Skin rash with itching, joint pain, and mild fever",
  ];

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      // Step 1: Extract symptoms via NLP
      const { data: nlpData } = await api.post<NLPExtractResult>("/nlp/extract-symptoms", { text });
      const symptoms = nlpData.symptoms
        .filter((s) => !s.negated)
        .map((s) => s.symptom);

      if (symptoms.length === 0) {
        setError("No symptoms could be extracted. Try describing your symptoms more clearly.");
        setLoading(false);
        return;
      }

      // Step 2: Run general disease prediction with extracted symptoms
      let prediction: PredictionResult | null = null;
      try {
        const { data: predData } = await api.post<PredictionResult>("/predict/general", { symptoms });
        prediction = predData;
      } catch {
        // Prediction may fail if model isn't loaded — still show extracted symptoms
      }

      // Step 3: Get severity score
      let severityScore = 5.0;
      try {
        const { data: sevData } = await api.post<{ severity_score: number; urgency_level: string }>(
          "/predict/severity",
          { symptoms }
        );
        severityScore = sevData.severity_score;
      } catch {
        // Severity model may not be loaded
      }

      setResult({
        extracted_symptoms: symptoms,
        predicted_disease: prediction?.prediction || "Model not available",
        confidence: prediction?.confidence || 0,
        severity_score: severityScore,
        top_k: prediction?.top_k || [],
        specialist: prediction?.recommendation?.recommended_specialist || "General Physician",
        disclaimer: prediction?.disclaimer || nlpData.disclaimer || "⚠️ This is an academic project. Not medical advice.",
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (score: number) => {
    if (score <= 3) return { bg: "bg-emerald-500/10", text: "text-emerald-400", border: "border-emerald-500/20", label: "Low" };
    if (score <= 6) return { bg: "bg-amber-500/10", text: "text-amber-400", border: "border-amber-500/20", label: "Moderate" };
    return { bg: "bg-rose-500/10", text: "text-rose-400", border: "border-rose-500/20", label: "High" };
  };

  return (
    <div className="grid lg:grid-cols-2 gap-6">
      {/* Input Panel */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-2 mb-4">
          <Brain className="w-5 h-5 text-cyan-400" />
          <h2 className="text-lg font-semibold text-white">Symptom Description</h2>
        </div>
        <p className="text-xs text-slate-500 mb-4">
          Describe your symptoms in natural language. Our NLP engine will extract medical entities and run predictions.
        </p>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Example: I've been experiencing a persistent headache for the past 3 days, along with fever, fatigue, and muscle pain..."
          className="glass-input h-40 resize-none mb-4"
          style={{ minHeight: "160px" }}
        />

        {/* Example prompts */}
        <div className="mb-4">
          <p className="text-xs text-slate-600 mb-2">Quick examples:</p>
          <div className="flex flex-wrap gap-2">
            {EXAMPLE_PROMPTS.map((p, i) => (
              <button
                key={i}
                onClick={() => setText(p)}
                className="text-[11px] px-3 py-1.5 rounded-lg bg-white/[0.03] border border-white/[0.06] text-slate-400 hover:text-cyan-400 hover:border-cyan-500/20 transition-all"
              >
                {p.slice(0, 40)}...
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={!text.trim() || loading}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing...</>
          ) : (
            <><Send className="w-4 h-4" /> Analyze Symptoms</>
          )}
        </button>

        {error && (
          <div className="mt-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <p className="text-sm text-rose-300">{error}</p>
          </div>
        )}
      </div>

      {/* Results Panel */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-5 h-5 text-violet-400" />
          <h2 className="text-lg font-semibold text-white">Analysis Results</h2>
        </div>

        {!result && !loading && (
          <div className="flex flex-col items-center justify-center h-[400px] text-center">
            <Brain className="w-16 h-16 text-slate-700 mb-4" />
            <p className="text-slate-500 text-sm">Enter symptoms and click Analyze</p>
            <p className="text-slate-600 text-xs mt-1">Results will appear here</p>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center h-[400px]">
            <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-4 animate-pulse">
              <Brain className="w-8 h-8 text-cyan-400" />
            </div>
            <p className="text-cyan-400 text-sm font-medium">Processing NLP Pipeline...</p>
            <p className="text-slate-600 text-xs mt-1">Extracting symptoms → Predicting → Scoring</p>
          </div>
        )}

        {result && (
          <div className="space-y-5">
            {/* Extracted Symptoms */}
            <div>
              <p className="text-xs font-medium text-slate-400 mb-2">Extracted Symptoms</p>
              <div className="flex flex-wrap gap-2">
                {result.extracted_symptoms.map((s, i) => (
                  <span key={i} className="badge">{s}</span>
                ))}
              </div>
            </div>

            {/* Prediction */}
            <div className="glass-panel p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Stethoscope className="w-4 h-4 text-cyan-400" />
                  <p className="text-sm font-medium text-white">Predicted Condition</p>
                </div>
                <span className="text-xs text-slate-500">Confidence</span>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-xl font-bold text-cyan-300">{result.predicted_disease}</p>
                <div className="text-right">
                  <p className="text-lg font-bold text-white">{(result.confidence * 100).toFixed(1)}%</p>
                  {/* Confidence bar */}
                  <div className="w-24 h-1.5 rounded-full bg-slate-800 mt-1">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-cyan-400 transition-all duration-1000"
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Top-K Predictions */}
            {result.top_k.length > 1 && (
              <div>
                <p className="text-xs font-medium text-slate-400 mb-2">Differential Diagnosis</p>
                <div className="space-y-1">
                  {result.top_k.slice(0, 5).map((t, i) => (
                    <div key={i} className="flex items-center justify-between text-sm glass-panel px-3 py-2">
                      <span className="text-slate-300">{t.disease}</span>
                      <span className="text-xs text-slate-500">{(t.confidence * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Severity */}
            {(() => {
              const sev = getSeverityColor(result.severity_score);
              return (
                <div className={`glass-panel p-4 ${sev.border} border`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Activity className="w-4 h-4 text-amber-400" />
                      <p className="text-sm font-medium text-white">Severity Score</p>
                    </div>
                    <span className={`badge ${sev.bg} ${sev.text} border ${sev.border}`}>{sev.label} Risk</span>
                  </div>
                  <div className="mt-2 flex items-center gap-3">
                    <p className="text-2xl font-bold text-white">{result.severity_score.toFixed(1)}</p>
                    <span className="text-xs text-slate-500">/ 10</span>
                    <div className="flex-1 h-2 rounded-full bg-slate-800">
                      <div
                        className={`h-full rounded-full transition-all duration-1000 ${
                          result.severity_score <= 3 ? "bg-emerald-500" : result.severity_score <= 6 ? "bg-amber-500" : "bg-rose-500"
                        }`}
                        style={{ width: `${result.severity_score * 10}%` }}
                      />
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* Specialist */}
            <div className="flex items-center gap-3 glass-panel p-3">
              <Pill className="w-4 h-4 text-violet-400" />
              <div>
                <p className="text-xs text-slate-500">Recommended Specialist</p>
                <p className="text-sm font-medium text-violet-300">{result.specialist}</p>
              </div>
            </div>

            {/* Disclaimer */}
            <p className="text-[11px] text-slate-600 border-t border-white/[0.04] pt-3">
              {result.disclaimer}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
