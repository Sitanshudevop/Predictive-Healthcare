import { Link } from "react-router-dom";
import {
  Brain, Shield, Activity, Zap, HeartPulse, Stethoscope,
  Microscope, Scan, BookOpen, Lock, ArrowRight, Sparkles
} from "lucide-react";

const FEATURES = [
  { icon: Brain, title: "11 ML Models", desc: "Disease prediction, organ risk, severity scoring, and NLP symptom extraction", color: "cyan" },
  { icon: Stethoscope, title: "NLP Symptom Parser", desc: "Describe symptoms naturally — AI extracts and maps to 132+ medical conditions", color: "violet" },
  { icon: Scan, title: "Medical Imaging", desc: "Chest X-ray pneumonia detection and skin lesion classification via deep learning", color: "emerald" },
  { icon: Shield, title: "Privacy First", desc: "No login required. Your health data stays local — predictions are processed in real-time", color: "rose" },
  { icon: HeartPulse, title: "Real-time Risk", desc: "Instant cardiovascular, diabetes, liver, and kidney disease risk assessment", color: "cyan" },
  { icon: BookOpen, title: "Disease Library", desc: "46 comprehensive disease profiles with symptoms, treatments, and red flags", color: "violet" },
];

const MODELS = [
  "General Disease", "Diabetes", "Heart Disease", "Breast Cancer", "Liver Disease",
  "Kidney Disease", "Pneumonia CNN", "Skin MobileNet", "Mental Health", "Severity Score", "NLP Extractor"
];

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Background orbs */}
      <div className="bg-orb w-[600px] h-[600px] bg-cyan-500 top-[-200px] left-[-100px]" />
      <div className="bg-orb w-[500px] h-[500px] bg-violet-500 bottom-[-100px] right-[-100px]" style={{ animationDelay: "2s" }} />
      <div className="bg-orb w-[300px] h-[300px] bg-emerald-500 top-[40%] right-[20%]" style={{ animationDelay: "4s", opacity: 0.08 }} />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 badge mb-8 animate-pulse-slow">
            <Sparkles className="w-3 h-3" />
            <span>Powered by 11 ML Models</span>
          </div>

          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.1] mb-6">
            <span className="text-white">Predictive</span>
            <br />
            <span className="bg-gradient-to-r from-cyan-400 via-cyan-300 to-violet-400 bg-clip-text text-transparent">
              Healthcare System
            </span>
          </h1>

          <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            AI-powered disease prediction, medical imaging analysis, and NLP symptom parsing.
            Get instant health risk assessments backed by machine learning.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link to="/dashboard" className="btn-primary flex items-center gap-2 text-base px-8 py-4">
              Get Started
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link to="/library" className="btn-ghost flex items-center gap-2 text-base px-8 py-4">
              <BookOpen className="w-4 h-4" />
              Explore Disease Library
            </Link>
          </div>

          {/* Model Pills */}
          <div className="flex flex-wrap items-center justify-center gap-2 max-w-3xl mx-auto mb-20">
            {MODELS.map((m) => (
              <span key={m} className="px-3 py-1.5 rounded-full text-xs font-medium bg-white/[0.04] border border-white/[0.06] text-slate-400 hover:text-cyan-400 hover:border-cyan-500/20 transition-all cursor-default">
                {m}
              </span>
            ))}
          </div>

          {/* Hero Visual — Glass Dashboard Preview */}
          <div className="relative max-w-4xl mx-auto">
            <div className="glass-card p-6 md:p-10">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                {[
                  { label: "Models Active", value: "11", icon: Brain, color: "text-cyan-400" },
                  { label: "Diseases Covered", value: "132+", icon: Stethoscope, color: "text-emerald-400" },
                  { label: "Accuracy Avg", value: "94.2%", icon: Activity, color: "text-violet-400" },
                  { label: "Response Time", value: "<200ms", icon: Zap, color: "text-amber-400" },
                ].map((stat) => (
                  <div key={stat.label} className="glass-panel p-4 text-center">
                    <stat.icon className={`w-5 h-5 ${stat.color} mx-auto mb-2`} />
                    <p className="text-2xl font-bold text-white">{stat.value}</p>
                    <p className="text-xs text-slate-500 mt-1">{stat.label}</p>
                  </div>
                ))}
              </div>
              {/* Simulated EKG line */}
              <div className="h-16 rounded-xl bg-slate-950/50 border border-white/[0.04] flex items-center justify-center overflow-hidden">
                <svg viewBox="0 0 400 50" className="w-full h-full opacity-40" preserveAspectRatio="none">
                  <polyline
                    fill="none"
                    stroke="#22d3ee"
                    strokeWidth="1.5"
                    points="0,25 30,25 40,25 50,10 55,40 60,25 70,25 100,25 130,25 140,25 150,8 155,42 160,25 170,25 200,25 230,25 240,25 250,10 255,40 260,25 270,25 300,25 330,25 340,25 350,10 355,40 360,25 370,25 400,25"
                  />
                </svg>
              </div>
            </div>
            {/* Glow behind card */}
            <div className="absolute inset-0 -z-10 blur-3xl opacity-20 bg-gradient-to-r from-cyan-500 via-transparent to-violet-500 rounded-3xl" />
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Enterprise-Grade Health Intelligence
            </h2>
            <p className="text-slate-400 max-w-xl mx-auto">
              Built for accuracy, designed for speed, engineered for privacy.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f, i) => {
              const colorMap: Record<string, string> = {
                cyan: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20",
                violet: "text-violet-400 bg-violet-500/10 border-violet-500/20",
                emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
                rose: "text-rose-400 bg-rose-500/10 border-rose-500/20",
              };
              const c = colorMap[f.color] || colorMap.cyan;
              return (
                <div key={i} className="glass-card p-6 group">
                  <div className={`w-10 h-10 rounded-xl border flex items-center justify-center mb-4 ${c}`}>
                    <f.icon className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-cyan-300 transition-colors">
                    {f.title}
                  </h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Medical Disclaimer */}
      <section className="relative py-16 px-6">
        <div className="max-w-3xl mx-auto">
          <div className="glass-panel p-8 border-amber-500/20 text-center">
            <Lock className="w-8 h-8 text-amber-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-amber-300 mb-3">Medical Disclaimer</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              This system is for <strong className="text-slate-300">educational and informational purposes only</strong>.
              It does not provide medical advice, diagnosis, or treatment. Always seek the advice of a qualified
              healthcare provider for any medical condition. Never disregard professional medical advice or delay
              seeking it because of information provided by this system.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/[0.04] py-8 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-slate-500 text-sm">
            <Activity className="w-4 h-4 text-cyan-500" />
            <span>Predictive Healthcare v1.0 — Academic Project</span>
          </div>
          <p className="text-xs text-slate-600">
            © {new Date().getFullYear()} Predictive Healthcare System. For educational use only.
          </p>
        </div>
      </footer>
    </div>
  );
}
