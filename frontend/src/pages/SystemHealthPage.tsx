import { useState, useEffect } from "react";
import {
  BarChart3, Users, Activity, Brain, Server, HardDrive, Cpu,
  TrendingUp, AlertTriangle, Clock, Database, RefreshCw
} from "lucide-react";


interface SystemMetrics {
  total_users: number;
  total_predictions: number;
  active_models: number;
  uptime_hours: number;
  avg_response_ms: number;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  predictions_today: number;
  error_rate: number;
}

const MOCK_METRICS: SystemMetrics = {
  total_users: 42,
  total_predictions: 1284,
  active_models: 11,
  uptime_hours: 168.5,
  avg_response_ms: 187,
  cpu_usage: 34,
  memory_usage: 52,
  disk_usage: 28,
  predictions_today: 73,
  error_rate: 0.8,
};

const MODEL_ANALYTICS = [
  { name: "General Disease", calls: 312, accuracy: 96.2, avg_ms: 145, status: "healthy" },
  { name: "Diabetes Risk", calls: 198, accuracy: 93.8, avg_ms: 112, status: "healthy" },
  { name: "Heart Disease", calls: 176, accuracy: 91.5, avg_ms: 134, status: "healthy" },
  { name: "Breast Cancer", calls: 89, accuracy: 98.3, avg_ms: 98, status: "healthy" },
  { name: "Liver Disease", calls: 67, accuracy: 89.7, avg_ms: 120, status: "healthy" },
  { name: "Kidney Disease", calls: 54, accuracy: 95.1, avg_ms: 115, status: "healthy" },
  { name: "Pneumonia CNN", calls: 132, accuracy: 94.6, avg_ms: 890, status: "healthy" },
  { name: "Skin MobileNet", calls: 87, accuracy: 87.2, avg_ms: 1240, status: "warning" },
  { name: "Mental Health", calls: 95, accuracy: 92.7, avg_ms: 105, status: "healthy" },
  { name: "Severity Score", calls: 284, accuracy: 86.3, avg_ms: 78, status: "healthy" },
  { name: "NLP Extractor", calls: 390, accuracy: 99.0, avg_ms: 210, status: "healthy" },
];

export default function SystemHealthPage() {

  const [metrics, setMetrics] = useState<SystemMetrics>(MOCK_METRICS);
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = () => {
    setRefreshing(true);
    setTimeout(() => {
      setMetrics({ ...MOCK_METRICS, predictions_today: MOCK_METRICS.predictions_today + Math.floor(Math.random() * 5) });
      setRefreshing(false);
    }, 1000);
  };

  const UsageBar = ({ value, color }: { value: number; color: string }) => (
    <div className="w-full h-2 rounded-full bg-slate-800 mt-2">
      <div className={`h-full rounded-full transition-all duration-1000 ${color}`} style={{ width: `${value}%` }} />
    </div>
  );

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 md:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2 flex items-center gap-3" style={{ color: '#F4F4F5' }}>
              <Activity className="w-8 h-8 text-violet-400" />
              System Health Dashboard
            </h1>
            <p className="text-slate-400 text-sm">Real-time system monitoring, model analytics, and platform usage</p>
          </div>
          <button onClick={handleRefresh} className={`btn-ghost flex items-center gap-2 ${refreshing ? "opacity-50" : ""}`} disabled={refreshing}>
            <RefreshCw className={`w-4 h-4 ${refreshing ? "animate-spin" : ""}`} />
            Refresh
          </button>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
          {[
            { label: "Total Active Users", value: metrics.total_users, icon: Users, color: "text-cyan-400" },
            { label: "Predictions", value: metrics.total_predictions.toLocaleString(), icon: BarChart3, color: "text-emerald-400" },
            { label: "Today", value: metrics.predictions_today, icon: TrendingUp, color: "text-violet-400" },
            { label: "Avg Response", value: `${metrics.avg_response_ms}ms`, icon: Clock, color: "text-amber-400" },
            { label: "Error Rate", value: `${metrics.error_rate}%`, icon: AlertTriangle, color: "text-rose-400" },
          ].map((m, i) => (
            <div key={i} className="glass-card p-5">
              <m.icon className={`w-5 h-5 ${m.color} mb-3`} />
              <p className="text-2xl font-bold text-white">{m.value}</p>
              <p className="text-xs text-slate-500 mt-1">{m.label}</p>
            </div>
          ))}
        </div>

        {/* System Resources */}
        <div className="grid md:grid-cols-3 gap-4 mb-8">
          <div className="glass-card p-5">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2"><Cpu className="w-4 h-4 text-cyan-400" /><span className="text-sm text-white font-medium">CPU</span></div>
              <span className="text-sm font-bold text-white">{metrics.cpu_usage}%</span>
            </div>
            <UsageBar value={metrics.cpu_usage} color="bg-gradient-to-r from-cyan-500 to-cyan-400" />
          </div>
          <div className="glass-card p-5">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2"><Server className="w-4 h-4 text-violet-400" /><span className="text-sm text-white font-medium">Memory</span></div>
              <span className="text-sm font-bold text-white">{metrics.memory_usage}%</span>
            </div>
            <UsageBar value={metrics.memory_usage} color="bg-gradient-to-r from-violet-500 to-violet-400" />
          </div>
          <div className="glass-card p-5">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2"><HardDrive className="w-4 h-4 text-emerald-400" /><span className="text-sm text-white font-medium">Disk</span></div>
              <span className="text-sm font-bold text-white">{metrics.disk_usage}%</span>
            </div>
            <UsageBar value={metrics.disk_usage} color="bg-gradient-to-r from-emerald-500 to-emerald-400" />
          </div>
        </div>

        {/* Model Analytics Table */}
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Brain className="w-5 h-5 text-cyan-400" />
            Model Analytics
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/[0.06]">
                  <th className="text-left text-xs font-medium text-slate-500 pb-3 pr-4">Model</th>
                  <th className="text-right text-xs font-medium text-slate-500 pb-3 px-4">Calls</th>
                  <th className="text-right text-xs font-medium text-slate-500 pb-3 px-4">Accuracy</th>
                  <th className="text-right text-xs font-medium text-slate-500 pb-3 px-4">Avg Latency</th>
                  <th className="text-right text-xs font-medium text-slate-500 pb-3 pl-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {MODEL_ANALYTICS.map((m, i) => (
                  <tr key={i} className="border-b border-white/[0.03] hover:bg-white/[0.02] transition-colors">
                    <td className="py-3 pr-4">
                      <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${m.status === "healthy" ? "bg-emerald-400" : "bg-amber-400"} animate-pulse`} />
                        <span className="text-white font-medium">{m.name}</span>
                      </div>
                    </td>
                    <td className="text-right py-3 px-4 text-slate-300">{m.calls}</td>
                    <td className="text-right py-3 px-4">
                      <span className={`${m.accuracy >= 95 ? "text-emerald-400" : m.accuracy >= 90 ? "text-cyan-400" : "text-amber-400"}`}>
                        {m.accuracy}%
                      </span>
                    </td>
                    <td className="text-right py-3 px-4">
                      <span className={`${m.avg_ms < 200 ? "text-emerald-400" : m.avg_ms < 500 ? "text-amber-400" : "text-rose-400"}`}>
                        {m.avg_ms}ms
                      </span>
                    </td>
                    <td className="text-right py-3 pl-4">
                      <span className={`badge text-[10px] ${m.status === "healthy" ? "badge-emerald" : ""}`}>
                        {m.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
