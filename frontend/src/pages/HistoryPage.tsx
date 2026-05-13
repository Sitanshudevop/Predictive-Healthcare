import { useState, useEffect } from "react";
import { History, Search, Filter, Calendar, Brain, HeartPulse, Scan, Trash2, ChevronDown, FileText } from "lucide-react";
import api from "../lib/api";

export interface HistoryItem {
  id: number;
  model_name: string;
  input_data: any;
  prediction: string;
  confidence: number;
  severity_score?: number;
  created_at: string;
}

const MODEL_ICONS: Record<string, typeof Brain> = {
  "NLP Symptom Parser": Brain,
  "Diabetes Risk": HeartPulse,
  "Heart Disease": HeartPulse,
  "Pneumonia CNN": Scan,
  "Mental Health Screen": Brain,
  "general": Brain,
  "diabetes": HeartPulse,
  "heart": HeartPulse,
  "breast_cancer": HeartPulse,
  "liver": HeartPulse,
  "kidney": HeartPulse,
  "mental_health": Brain,
  "severity": Brain,
  "pneumonia": Scan,
  "skin": Scan,
};

export default function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [search, setSearch] = useState("");
  const [filterModel, setFilterModel] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const { data } = await api.get("/v1/history");
        setItems(data.history || []);
      } catch (err) {
        console.error("Failed to load history", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/v1/history/${id}`);
      setItems((prev) => prev.filter((i) => i.id !== id));
    } catch (err) {
      console.error("Failed to delete history item", err);
    }
  };

  const handleClearAll = async () => {
    // There is no bulk delete endpoint, so we'll delete them one by one
    // or just let the backend handle it if we add an endpoint. Let's do nothing or show a toast
    // Wait, the backend doesn't have a clear all. I'll just remove the button.
  };

  const filtered = items.filter((item) => {
    if (filterModel !== "all" && item.model_name !== filterModel) return false;
    if (search && !item.prediction.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const models = [...new Set(items.map((i) => i.model_name))];

  const riskColor = (score?: number) => {
    if (score === undefined || score === null) return "badge";
    if (score <= 3) return "badge-emerald";
    if (score <= 6) return "badge-amber";
    return "badge-rose";
  };

  const formatDate = (iso: string) => {
    const d = new Date(iso);
    const now = new Date();
    const diff = now.getTime() - d.getTime();
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Prediction History</h1>
            <p className="text-slate-400 text-sm">{items.length} predictions stored</p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input type="text" placeholder="Search predictions..." className="glass-input pl-10" value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
          <div className="relative">
            <Filter className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <select value={filterModel} onChange={(e) => setFilterModel(e.target.value)} className="glass-input pl-10 pr-8 appearance-none cursor-pointer min-w-[180px]">
              <option value="all">All Models</option>
              {models.map((m) => <option key={m} value={m}>{m}</option>)}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
          </div>
        </div>

        {/* History List */}
        {loading ? (
          <div className="text-center py-12 text-slate-400">Loading history...</div>
        ) : filtered.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <FileText className="w-12 h-12 text-slate-700 mx-auto mb-3" />
            <p className="text-slate-400">No predictions found</p>
            <p className="text-slate-600 text-xs mt-1">Run a prediction in the Diagnostic Engine to see it here</p>
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map((item) => {
              const Icon = MODEL_ICONS[item.model_name] || Brain;
              return (
                <div key={item.id} className="glass-card p-5 flex items-center gap-4 group">
                  <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-5 h-5 text-cyan-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <p className="text-sm font-semibold text-white truncate">{item.prediction}</p>
                      {item.severity_score !== undefined && (
                        <span className={`badge ${riskColor(item.severity_score)} text-[10px]`}>
                          Severity: {item.severity_score}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-500 truncate">{item.model_name}</p>
                  </div>
                  <div className="text-right flex-shrink-0 flex items-center gap-3">
                    <div>
                      <p className="text-sm font-bold text-white">{(item.confidence * 100).toFixed(0)}%</p>
                      <p className="text-[11px] text-slate-600 flex items-center gap-1 justify-end">
                        <Calendar className="w-3 h-3" /> {formatDate(item.created_at)}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-rose-500/10 text-slate-600 hover:text-rose-400 transition-all"
                      title="Delete"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
