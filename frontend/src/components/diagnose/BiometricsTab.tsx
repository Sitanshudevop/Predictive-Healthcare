import { useState } from "react";
import { HeartPulse, Loader2, Send, AlertCircle, CheckCircle, XCircle } from "lucide-react";
import api from "../../lib/api";


const MODELS = [
  { id: "diabetes", label: "Diabetes Risk", fields: [
    { name: "pregnancies", label: "Pregnancies", type: "number", placeholder: "0", min: 0 },
    { name: "glucose", label: "Glucose (mg/dL)", type: "number", placeholder: "120", min: 0 },
    { name: "blood_pressure", label: "Blood Pressure (mm Hg)", type: "number", placeholder: "80", min: 0 },
    { name: "skin_thickness", label: "Skin Thickness (mm)", type: "number", placeholder: "20", min: 0 },
    { name: "insulin", label: "Insulin (mu U/ml)", type: "number", placeholder: "80", min: 0 },
    { name: "bmi", label: "BMI", type: "number", placeholder: "25.0", min: 0, step: "0.1" },
    { name: "diabetes_pedigree_function", label: "Diabetes Pedigree Function", type: "number", placeholder: "0.5", min: 0, step: "0.01" },
    { name: "age", label: "Age", type: "number", placeholder: "30", min: 1 },
  ]},
  { id: "heart", label: "Heart Disease", fields: [
    { name: "age", label: "Age", type: "number", placeholder: "55" },
    { name: "sex", label: "Sex (0=F, 1=M)", type: "number", placeholder: "1" },
    { name: "cp", label: "Chest Pain Type (0-3)", type: "number", placeholder: "1" },
    { name: "trestbps", label: "Resting BP (mm Hg)", type: "number", placeholder: "130" },
    { name: "chol", label: "Cholesterol (mg/dL)", type: "number", placeholder: "250" },
    { name: "fbs", label: "Fasting Blood Sugar >120 (0/1)", type: "number", placeholder: "0" },
    { name: "restecg", label: "Rest ECG (0-2)", type: "number", placeholder: "0" },
    { name: "thalach", label: "Max Heart Rate", type: "number", placeholder: "150" },
    { name: "exang", label: "Exercise Angina (0/1)", type: "number", placeholder: "0" },
    { name: "oldpeak", label: "ST Depression", type: "number", placeholder: "1.0", step: "0.1" },
    { name: "slope", label: "ST Slope (0-2)", type: "number", placeholder: "1" },
    { name: "ca", label: "Major Vessels (0-3)", type: "number", placeholder: "0" },
    { name: "thal", label: "Thalassemia (1-3)", type: "number", placeholder: "2" },
  ]},
  { id: "breast_cancer", label: "Breast Cancer", fields: [
    { name: "mean_radius", label: "Mean Radius", type: "number", placeholder: "14.0", step: "0.01" },
    { name: "mean_texture", label: "Mean Texture", type: "number", placeholder: "19.0", step: "0.01" },
    { name: "mean_perimeter", label: "Mean Perimeter", type: "number", placeholder: "92.0", step: "0.01" },
    { name: "mean_area", label: "Mean Area", type: "number", placeholder: "650", step: "0.1" },
    { name: "mean_smoothness", label: "Mean Smoothness", type: "number", placeholder: "0.1", step: "0.001" },
  ]},
  { id: "liver", label: "Liver Disease", fields: [
    { name: "age", label: "Age", type: "number", placeholder: "45" },
    { name: "gender", label: "Gender (0=F, 1=M)", type: "number", placeholder: "1" },
    { name: "total_bilirubin", label: "Total Bilirubin", type: "number", placeholder: "0.7", step: "0.1" },
    { name: "direct_bilirubin", label: "Direct Bilirubin", type: "number", placeholder: "0.3", step: "0.1" },
    { name: "alkaline_phosphotase", label: "Alkaline Phosphotase", type: "number", placeholder: "200" },
    { name: "alamine_aminotransferase", label: "SGPT (ALT)", type: "number", placeholder: "25" },
    { name: "aspartate_aminotransferase", label: "SGOT (AST)", type: "number", placeholder: "30" },
    { name: "total_proteins", label: "Total Proteins", type: "number", placeholder: "6.8", step: "0.1" },
    { name: "albumin", label: "Albumin", type: "number", placeholder: "3.5", step: "0.1" },
    { name: "albumin_and_globulin_ratio", label: "A/G Ratio", type: "number", placeholder: "1.0", step: "0.01" },
  ]},
  { id: "kidney", label: "Kidney Disease", fields: [
    { name: "age", label: "Age", type: "number", placeholder: "50" },
    { name: "blood_pressure", label: "Blood Pressure", type: "number", placeholder: "80" },
    { name: "specific_gravity", label: "Specific Gravity", type: "number", placeholder: "1.020", step: "0.001" },
    { name: "albumin", label: "Albumin (0-5)", type: "number", placeholder: "0" },
    { name: "sugar", label: "Sugar (0-5)", type: "number", placeholder: "0" },
    { name: "red_blood_cells", label: "Red Blood Cells (0=abn, 1=norm)", type: "number", placeholder: "1" },
    { name: "pus_cell", label: "Pus Cell (0=abn, 1=norm)", type: "number", placeholder: "1" },
    { name: "pus_cell_clumps", label: "Pus Cell Clumps (0/1)", type: "number", placeholder: "0" },
    { name: "bacteria", label: "Bacteria (0/1)", type: "number", placeholder: "0" },
    { name: "blood_glucose_random", label: "Blood Glucose Random", type: "number", placeholder: "120" },
    { name: "blood_urea", label: "Blood Urea", type: "number", placeholder: "36" },
    { name: "serum_creatinine", label: "Serum Creatinine", type: "number", placeholder: "1.2", step: "0.1" },
    { name: "sodium", label: "Sodium", type: "number", placeholder: "140" },
    { name: "potassium", label: "Potassium", type: "number", placeholder: "4.5", step: "0.1" },
    { name: "hemoglobin", label: "Hemoglobin", type: "number", placeholder: "13.0", step: "0.1" },
    { name: "packed_cell_volume", label: "Packed Cell Volume", type: "number", placeholder: "44" },
    { name: "white_blood_cell_count", label: "WBC Count", type: "number", placeholder: "8000" },
    { name: "red_blood_cell_count", label: "RBC Count", type: "number", placeholder: "5.0", step: "0.1" },
    { name: "hypertension", label: "Hypertension (0/1)", type: "number", placeholder: "0" },
    { name: "diabetes_mellitus", label: "Diabetes (0/1)", type: "number", placeholder: "0" },
    { name: "coronary_artery_disease", label: "Coronary Artery Disease (0/1)", type: "number", placeholder: "0" },
    { name: "appetite", label: "Appetite (0=poor, 1=good)", type: "number", placeholder: "1" },
    { name: "pedal_edema", label: "Pedal Edema (0/1)", type: "number", placeholder: "0" },
    { name: "anemia", label: "Anemia (0/1)", type: "number", placeholder: "0" },
  ]},
  { id: "mental_health", label: "Mental Health Screen", fields: [
    { name: "phq9_total", label: "PHQ-9 Score (0-27)", type: "number", placeholder: "5", min: 0, max: 27 },
    { name: "gad7_total", label: "GAD-7 Score (0-21)", type: "number", placeholder: "3", min: 0, max: 21 },
    { name: "age", label: "Age", type: "number", placeholder: "25" },
    { name: "sleep_hours", label: "Sleep Hours/Night", type: "number", placeholder: "7", step: "0.5" },
    { name: "stress_level", label: "Stress Level (1-10)", type: "number", placeholder: "4", min: 1, max: 10 },
  ]},
];

interface PredResult {
  prediction: string | number;
  confidence: number;
  risk_level: string;
  model_name: string;
}

export default function BiometricsTab() {

  const [selectedModel, setSelectedModel] = useState(MODELS[0].id);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredResult | null>(null);
  const [error, setError] = useState("");

  const model = MODELS.find((m) => m.id === selectedModel)!;

  const handleChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePredict = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    // Build payload matching backend schema
    let payload: any;

    if (selectedModel === "mental_health") {
      // Backend expects phq9_scores (9 items), gad7_scores (7 items), age, sleep_hours, stress_level
      const phq9Total = parseInt(formData["phq9_total"] || "5");
      const gad7Total = parseInt(formData["gad7_total"] || "3");
      // Distribute total evenly across items
      const phq9Base = Math.floor(phq9Total / 9);
      const phq9Remainder = phq9Total % 9;
      const phq9Scores = Array(9).fill(phq9Base).map((v, i) => i < phq9Remainder ? v + 1 : v);
      const gad7Base = Math.floor(gad7Total / 7);
      const gad7Remainder = gad7Total % 7;
      const gad7Scores = Array(7).fill(gad7Base).map((v, i) => i < gad7Remainder ? v + 1 : v);
      payload = {
        phq9_scores: phq9Scores,
        gad7_scores: gad7Scores,
        age: parseInt(formData["age"] || "25"),
        sleep_hours: parseFloat(formData["sleep_hours"] || "7"),
        stress_level: parseInt(formData["stress_level"] || "4"),
      };
    } else if (selectedModel === "breast_cancer") {
      // Backend expects { features: [30 floats] }
      const features = model.fields.map((f) => parseFloat(formData[f.name] || f.placeholder || "0"));
      payload = { features };
    } else {
      // All other models: named fields
      payload = {} as Record<string, number>;
      for (const f of model.fields) {
        payload[f.name] = parseFloat(formData[f.name] || f.placeholder || "0");
      }
    }

    try {
      const { data } = await api.post(`/predict/${selectedModel}`, payload);
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const riskColors: Record<string, { bg: string; text: string; icon: typeof CheckCircle }> = {
    low: { bg: "bg-emerald-500/10 border-emerald-500/20", text: "text-emerald-400", icon: CheckCircle },
    moderate: { bg: "bg-amber-500/10 border-amber-500/20", text: "text-amber-400", icon: AlertCircle },
    high: { bg: "bg-rose-500/10 border-rose-500/20", text: "text-rose-400", icon: XCircle },
  };

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      {/* Model Selector */}
      <div className="glass-card p-5">
        <div className="flex items-center gap-2 mb-4">
          <HeartPulse className="w-5 h-5 text-violet-400" />
          <h2 className="text-sm font-semibold text-white">Select Model</h2>
        </div>
        <div className="space-y-1.5">
          {MODELS.map((m) => (
            <button
              key={m.id}
              onClick={() => { setSelectedModel(m.id); setResult(null); setFormData({}); }}
              className={`w-full text-left px-4 py-2.5 rounded-xl text-sm transition-all ${
                selectedModel === m.id
                  ? "bg-violet-500/10 text-violet-300 border border-violet-500/20"
                  : "text-slate-400 hover:bg-white/[0.03] hover:text-slate-200"
              }`}
            >
              {m.label}
              <span className="text-xs text-slate-600 ml-2">({m.fields.length} inputs)</span>
            </button>
          ))}
        </div>
      </div>

      {/* Input Form */}
      <div className="glass-card p-6">
        <h2 className="text-sm font-semibold text-white mb-4">{model.label} — Input Parameters</h2>
        <div className="grid grid-cols-2 gap-3 mb-5 max-h-[450px] overflow-y-auto pr-2">
          {model.fields.map((f) => (
            <div key={f.name}>
              <label className="text-[11px] text-slate-500 mb-1 block">{f.label}</label>
              <input
                type={f.type}
                placeholder={f.placeholder}
                step={f.step}
                min={f.min}
                max={f.max}
                value={formData[f.name] || ""}
                onChange={(e) => handleChange(f.name, e.target.value)}
                className="glass-input py-2 text-sm"
              />
            </div>
          ))}
        </div>
        <button
          onClick={handlePredict}
          disabled={loading}
          className="btn-primary w-full flex items-center justify-center gap-2"
        >
          {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Running Model...</> : <><Send className="w-4 h-4" /> Run Prediction</>}
        </button>
        {error && (
          <div className="mt-3 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-sm text-rose-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" /> {error}
          </div>
        )}
      </div>

      {/* Results */}
      <div className="glass-card p-6">
        <h2 className="text-sm font-semibold text-white mb-4">Prediction Result</h2>
        {!result && !loading && (
          <div className="flex flex-col items-center justify-center h-[400px] text-center">
            <HeartPulse className="w-16 h-16 text-slate-700 mb-4" />
            <p className="text-slate-500 text-sm">Fill in parameters and run prediction</p>
          </div>
        )}
        {loading && (
          <div className="flex flex-col items-center justify-center h-[400px]">
            <div className="w-16 h-16 rounded-2xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center mb-4 animate-pulse">
              <HeartPulse className="w-8 h-8 text-violet-400" />
            </div>
            <p className="text-violet-400 text-sm">Running {model.label} model...</p>
          </div>
        )}
        {result && (() => {
          const rc = riskColors[result.risk_level] || riskColors.moderate;
          const Icon = rc.icon;
          return (
            <div className="space-y-5">
              <div className={`p-5 rounded-xl border ${rc.bg}`}>
                <Icon className={`w-10 h-10 ${rc.text} mx-auto mb-3`} />
                <p className="text-center text-lg font-bold text-white">{String(result.prediction)}</p>
                <p className={`text-center text-sm ${rc.text} mt-1 capitalize`}>{result.risk_level} Risk</p>
              </div>
              <div className="glass-panel p-4">
                <p className="text-xs text-slate-500 mb-1">Confidence</p>
                <div className="flex items-center gap-3">
                  <p className="text-xl font-bold text-white">{(result.confidence * 100).toFixed(1)}%</p>
                  <div className="flex-1 h-2 rounded-full bg-slate-800">
                    <div className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-violet-500 transition-all duration-1000" style={{ width: `${result.confidence * 100}%` }} />
                  </div>
                </div>
              </div>
              <div className="glass-panel p-4">
                <p className="text-xs text-slate-500">Model Used</p>
                <p className="text-sm font-medium text-white">{result.model_name}</p>
              </div>
              <p className="text-[11px] text-slate-600 border-t border-white/[0.04] pt-3">
                AI prediction for educational purposes only. Consult a healthcare professional.
              </p>
            </div>
          );
        })()}
      </div>
    </div>
  );
}
