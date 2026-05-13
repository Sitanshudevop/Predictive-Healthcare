import { useState, useRef } from "react";
import { Scan, Upload, Loader2, Image as ImageIcon, X, AlertCircle, CheckCircle } from "lucide-react";
import api from "../../lib/api";


const IMAGE_MODELS = [
  { id: "pneumonia", label: "Chest X-Ray — Pneumonia Detection", desc: "Upload a frontal chest X-ray image", accept: ".jpg,.jpeg,.png,.bmp,.webp" },
  { id: "skin", label: "Skin Lesion — Dermatology Classifier", desc: "Upload a dermoscopy or skin photo", accept: ".jpg,.jpeg,.png,.bmp,.webp" },
];

interface ImgResult {
  prediction: string;
  confidence: number;
  model_name: string;
  classes?: Record<string, number>;
}

export default function ImagingTab() {

  const [selectedModel, setSelectedModel] = useState(IMAGE_MODELS[0].id);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImgResult | null>(null);
  const [error, setError] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  const model = IMAGE_MODELS.find((m) => m.id === selectedModel)!;

  const handleFile = (f: File | null) => {
    if (!f) return;
    if (f.size > 5 * 1024 * 1024) { setError("File exceeds 5MB limit"); return; }
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError("");
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);



    try {
      const form = new FormData();
      form.append("file", file);
      const { data } = await api.post(`/predict/${selectedModel}`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Image analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const clear = () => { setFile(null); setPreview(null); setResult(null); setError(""); };

  return (
    <div className="grid lg:grid-cols-2 gap-6">
      {/* Upload Panel */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-2 mb-4">
          <Scan className="w-5 h-5 text-emerald-400" />
          <h2 className="text-lg font-semibold text-white">Image Lab</h2>
        </div>

        {/* Model selector */}
        <div className="flex gap-2 mb-5">
          {IMAGE_MODELS.map((m) => (
            <button
              key={m.id}
              onClick={() => { setSelectedModel(m.id); clear(); }}
              className={`flex-1 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                selectedModel === m.id
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                  : "text-slate-400 border border-white/[0.06] hover:border-white/[0.1]"
              }`}
            >
              {m.id === "pneumonia" ? "🫁 Chest X-Ray" : "🔬 Skin Lesion"}
            </button>
          ))}
        </div>

        <p className="text-xs text-slate-500 mb-4">{model.desc}</p>

        {/* Drop zone */}
        {!preview ? (
          <div
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
            onClick={() => fileRef.current?.click()}
            className="border-2 border-dashed border-white/[0.08] rounded-2xl h-64 flex flex-col items-center justify-center cursor-pointer hover:border-emerald-500/30 transition-colors"
          >
            <Upload className="w-10 h-10 text-slate-600 mb-3" />
            <p className="text-sm text-slate-400">Drop image here or click to upload</p>
            <p className="text-xs text-slate-600 mt-1">JPG, PNG, BMP, WebP — Max 5MB</p>
            <input ref={fileRef} type="file" accept={model.accept} className="hidden" onChange={(e) => handleFile(e.target.files?.[0] || null)} />
          </div>
        ) : (
          <div className="relative rounded-2xl overflow-hidden border border-white/[0.06]">
            <img src={preview} alt="Upload preview" className="w-full h-64 object-contain bg-black/50" />
            <button onClick={clear} className="absolute top-3 right-3 w-8 h-8 rounded-full bg-slate-900/80 flex items-center justify-center hover:bg-slate-800 transition-colors">
              <X className="w-4 h-4 text-white" />
            </button>
            <div className="absolute bottom-0 left-0 right-0 px-4 py-2 bg-gradient-to-t from-black/60 to-transparent">
              <p className="text-xs text-white/80 truncate">{file?.name}</p>
            </div>
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={!file || loading}
          className="btn-primary w-full mt-5 flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing Image...</> : <><Scan className="w-4 h-4" /> Run Analysis</>}
        </button>

        {error && (
          <div className="mt-3 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center gap-2 text-sm text-rose-300">
            <AlertCircle className="w-4 h-4 flex-shrink-0" /> {error}
          </div>
        )}
      </div>

      {/* Results Panel */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Analysis Result</h2>

        {!result && !loading && (
          <div className="flex flex-col items-center justify-center h-[400px] text-center">
            <ImageIcon className="w-16 h-16 text-slate-700 mb-4" />
            <p className="text-slate-500 text-sm">Upload an image and run analysis</p>
          </div>
        )}

        {loading && (
          <div className="flex flex-col items-center justify-center h-[400px]">
            <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-4 animate-pulse">
              <Scan className="w-8 h-8 text-emerald-400" />
            </div>
            <p className="text-emerald-400 text-sm">Processing image through CNN...</p>
            <p className="text-slate-600 text-xs mt-1">Preprocessing → Inference → Classification</p>
          </div>
        )}

        {result && (
          <div className="space-y-5">
            <div className="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-center">
              <CheckCircle className="w-10 h-10 text-emerald-400 mx-auto mb-3" />
              <p className="text-xl font-bold text-white">{result.prediction}</p>
              <p className="text-sm text-emerald-300 mt-1">{(result.confidence * 100).toFixed(1)}% confidence</p>
            </div>

            {/* Class probabilities */}
            {result.classes && (
              <div>
                <p className="text-xs font-medium text-slate-400 mb-3">Class Probabilities</p>
                <div className="space-y-2">
                  {Object.entries(result.classes).sort(([,a], [,b]) => b - a).map(([cls, prob]) => (
                    <div key={cls} className="flex items-center gap-3">
                      <span className="text-xs text-slate-400 w-20 truncate">{cls}</span>
                      <div className="flex-1 h-2 rounded-full bg-slate-800">
                        <div
                          className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-cyan-500 transition-all duration-1000"
                          style={{ width: `${prob * 100}%` }}
                        />
                      </div>
                      <span className="text-xs text-slate-400 w-12 text-right">{(prob * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="glass-panel p-4">
              <p className="text-xs text-slate-500">Model</p>
              <p className="text-sm font-medium text-white">{result.model_name}</p>
            </div>

            <p className="text-[11px] text-slate-600 border-t border-white/[0.04] pt-3">
              AI-generated prediction for educational purposes. Not a medical diagnosis.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
