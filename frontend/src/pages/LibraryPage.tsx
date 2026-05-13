import { useState, useMemo } from "react";
import { BookOpen, Search, ChevronRight, AlertTriangle, Pill, Stethoscope, ShieldAlert, X, Heart } from "lucide-react";
import rawData from "../data/diseases.json";

interface OTCMed {
  category: string;
  examples: string[];
  disclaimer: string;
}

interface Disease {
  id: string;
  disease_name: string;
  icd10_code: string;
  description: string;
  common_symptoms: string[];
  rare_symptoms: string[];
  causes: string[];
  risk_factors: string[];
  complications: string[];
  prevention: string[];
  home_remedies: string[];
  otc_medications: OTCMed[];
  prescription_drug_categories: string[];
  recommended_specialist: string;
  severity_level: string;
  avg_recovery_time: string;
  when_to_see_doctor: string;
  red_flag_symptoms: string[];
}

export default function LibraryPage() {
  const diseases = rawData as Disease[];
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<Disease | null>(null);

  const filtered = useMemo(() => {
    if (!search.trim()) return diseases;
    const q = search.toLowerCase();
    return diseases.filter(
      (d) =>
        d.disease_name.toLowerCase().includes(q) ||
        d.common_symptoms.some((s) => s.toLowerCase().includes(q)) ||
        d.description.toLowerCase().includes(q)
    );
  }, [search, diseases]);

  const categories: Record<string, Disease[]> = useMemo(() => {
    const cats: Record<string, Disease[]> = {};
    filtered.forEach((d) => {
      const letter = d.disease_name[0].toUpperCase();
      if (!cats[letter]) cats[letter] = [];
      cats[letter].push(d);
    });
    return Object.fromEntries(Object.entries(cats).sort());
  }, [filtered]);

  const sevBadge = (level: string) => {
    if (level === "severe") return "badge badge-rose";
    if (level === "moderate") return "badge";
    return "badge badge-emerald";
  };

  return (
    <div className="min-h-screen pt-24 pb-12 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Disease Library</h1>
          <p className="text-slate-400 text-sm">
            {diseases.length} comprehensive disease profiles with symptoms, treatments, and red flags
          </p>
        </div>

        {/* Search */}
        <div className="relative mb-8 max-w-lg">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Search diseases, symptoms, or conditions..."
            className="glass-input pl-12 py-4 text-base"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* List */}
          <div className="lg:col-span-1 space-y-4 max-h-[70vh] overflow-y-auto pr-2">
            {Object.entries(categories).map(([letter, items]) => (
              <div key={letter}>
                <p className="text-xs font-bold text-cyan-400 mb-2 sticky top-0 bg-slate-950/90 backdrop-blur py-1">
                  {letter}
                </p>
                <div className="space-y-1">
                  {items.map((d) => (
                    <button
                      key={d.id}
                      onClick={() => setSelected(d)}
                      className={`w-full text-left px-4 py-3 rounded-xl text-sm transition-all flex items-center justify-between group ${
                        selected?.id === d.id
                          ? "bg-cyan-500/10 text-cyan-300 border border-cyan-500/20"
                          : "text-slate-300 hover:bg-white/[0.03] hover:text-white"
                      }`}
                    >
                      <span className="truncate">{d.disease_name}</span>
                      <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-slate-400 flex-shrink-0" />
                    </button>
                  ))}
                </div>
              </div>
            ))}
            {filtered.length === 0 && (
              <div className="text-center py-12">
                <BookOpen className="w-10 h-10 text-slate-700 mx-auto mb-3" />
                <p className="text-slate-500 text-sm">No diseases match your search</p>
              </div>
            )}
          </div>

          {/* Detail */}
          <div className="lg:col-span-2">
            {!selected ? (
              <div className="glass-card p-12 text-center h-full flex flex-col items-center justify-center min-h-[500px]">
                <BookOpen className="w-16 h-16 text-slate-700 mb-4" />
                <p className="text-slate-400">Select a disease from the list</p>
                <p className="text-xs text-slate-600 mt-1">Browse {diseases.length} conditions</p>
              </div>
            ) : (
              <div className="glass-card p-6 md:p-8 relative max-h-[75vh] overflow-y-auto">
                <button
                  onClick={() => setSelected(null)}
                  className="absolute top-4 right-4 p-2 rounded-lg hover:bg-white/[0.04] transition-colors lg:hidden"
                >
                  <X className="w-4 h-4 text-slate-400" />
                </button>

                <div className="flex flex-wrap items-center gap-3 mb-4">
                  <h2 className="text-2xl font-bold text-white">{selected.disease_name}</h2>
                  <span className="badge text-[10px]">{selected.icd10_code}</span>
                  <span className={`${sevBadge(selected.severity_level)} text-[10px]`}>
                    {selected.severity_level}
                  </span>
                </div>
                <p className="text-sm text-slate-400 leading-relaxed mb-6">{selected.description}</p>

                {/* Common Symptoms */}
                <div className="mb-6">
                  <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                    <Stethoscope className="w-4 h-4 text-cyan-400" /> Common Symptoms
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {selected.common_symptoms.map((s, i) => (
                      <span key={i} className="badge">{s}</span>
                    ))}
                  </div>
                  {selected.rare_symptoms.length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs text-slate-500 mb-2">Rare Symptoms</p>
                      <div className="flex flex-wrap gap-2">
                        {selected.rare_symptoms.map((s, i) => (
                          <span key={i} className="badge badge-violet text-[10px]">{s}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Causes & Risk Factors */}
                <div className="grid sm:grid-cols-2 gap-4 mb-6">
                  <div>
                    <h3 className="text-sm font-semibold text-white mb-2">Causes</h3>
                    <ul className="space-y-1.5">
                      {selected.causes.map((c, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-slate-400">
                          <span className="w-1.5 h-1.5 rounded-full bg-slate-600 mt-1.5 flex-shrink-0" />
                          {c}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white mb-2">Risk Factors</h3>
                    <ul className="space-y-1.5">
                      {selected.risk_factors.map((r, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-slate-400">
                          <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 flex-shrink-0" />
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Medications */}
                <div className="grid sm:grid-cols-2 gap-4 mb-6">
                  <div className="glass-panel p-4">
                    <h3 className="text-xs font-semibold text-emerald-400 mb-3 flex items-center gap-1.5">
                      <Pill className="w-3.5 h-3.5" /> OTC Medications
                    </h3>
                    <div className="space-y-3">
                      {selected.otc_medications.map((med, i) => (
                        <div key={i}>
                          <p className="text-xs text-slate-500 font-medium mb-1">{med.category}</p>
                          <ul className="space-y-0.5">
                            {med.examples.map((ex, j) => (
                              <li key={j} className="text-sm text-slate-300">• {ex}</li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="glass-panel p-4">
                    <h3 className="text-xs font-semibold text-violet-400 mb-3 flex items-center gap-1.5">
                      <Pill className="w-3.5 h-3.5" /> Prescription Categories
                    </h3>
                    <ul className="space-y-1">
                      {selected.prescription_drug_categories.map((m, i) => (
                        <li key={i} className="text-sm text-slate-300">• {m}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Home Remedies & Prevention */}
                <div className="grid sm:grid-cols-2 gap-4 mb-6">
                  <div className="glass-panel p-4">
                    <h3 className="text-xs font-semibold text-cyan-400 mb-2">
                      <Heart className="w-3.5 h-3.5 inline mr-1" />Home Remedies
                    </h3>
                    <ul className="space-y-1">
                      {selected.home_remedies.map((h, i) => (
                        <li key={i} className="text-sm text-slate-300">• {h}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="glass-panel p-4">
                    <h3 className="text-xs font-semibold text-cyan-400 mb-2">Prevention</h3>
                    <ul className="space-y-1">
                      {selected.prevention.map((p, i) => (
                        <li key={i} className="text-sm text-slate-300">• {p}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Red Flags */}
                {selected.red_flag_symptoms.length > 0 && (
                  <div className="glass-panel p-4 border border-rose-500/15 mb-6">
                    <h3 className="text-xs font-semibold text-rose-400 mb-2 flex items-center gap-1.5">
                      <ShieldAlert className="w-3.5 h-3.5" /> Red Flags — Seek Immediate Help
                    </h3>
                    <ul className="space-y-1.5">
                      {selected.red_flag_symptoms.map((r, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-rose-300/80">
                          <AlertTriangle className="w-3.5 h-3.5 text-rose-400 mt-0.5 flex-shrink-0" />
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* When to See Doctor */}
                <div className="glass-panel p-4 border border-amber-500/15 mb-6">
                  <h3 className="text-xs font-semibold text-amber-400 mb-2">When to See a Doctor</h3>
                  <p className="text-sm text-slate-300">{selected.when_to_see_doctor}</p>
                </div>

                {/* Footer info */}
                <div className="flex flex-wrap items-center gap-3 text-sm border-t border-white/[0.04] pt-4">
                  <span className="badge badge-violet">{selected.recommended_specialist}</span>
                  <span className="text-xs text-slate-600">Recovery: {selected.avg_recovery_time}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
